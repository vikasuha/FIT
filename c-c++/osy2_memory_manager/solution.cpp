#ifndef __PROGTEST__
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <pthread.h>
#include <semaphore.h>
#include "common.h"
using namespace std;
#endif /* __PROGTEST__ */

uint32_t* memory = NULL;

pthread_mutex_t page_mutex;
pthread_t threads[65];
bool used_thrs[65];
pthread_attr_t attr;

bool* free_pages = NULL;
uint32_t num_all_pages = 0;
uint32_t num_free_pages = 0;


class CImpCCPU : public CCPU {
public:
    CImpCCPU(uint8_t* memStart, uint32_t page_table_root, uint32_t num_proc_pages)
    : CCPU(memStart, page_table_root), num_proc_pages(num_proc_pages) 
    {};
    bool NewProcess(void * processArg, void (* entryPoint) (CCPU *, void *), bool copyMem);
    bool SetMemLimit(uint32_t pages);
    uint32_t GetMemLimit(void) const;

protected:
    uint32_t num_proc_pages = 0;
};

class param_for_create{
  public:
    uint32_t page_table_root;
    void* processArgs;
    void (* entryPoint) (CCPU*, void*);
    uint32_t num_proc_pages;
    CImpCCPU *new_cpu = new CImpCCPU ((uint8_t*)memory, page_table_root, num_proc_pages);
    
    param_for_create(uint32_t page_table_root, void* processArgs, void (* entryPoint) (CCPU*, void*), uint32_t num_proc_pages=0):
    page_table_root(page_table_root), processArgs(processArgs), entryPoint(entryPoint), num_proc_pages(num_proc_pages){}
    
    ~param_for_create(){
        delete new_cpu;
    }
};

void *createFunc (void *params) {
    param_for_create* new_params = (param_for_create*) params;
    new_params->entryPoint(new_params->new_cpu, new_params->processArgs);
    return NULL;
}

uint32_t GetFreePage() 
{
    uint32_t i;
    for (i = 0; i < num_all_pages; ++i)
        if (free_pages[i]) 
            break;
    num_free_pages--;
    free_pages[i] = false;
    return i;
}

uint32_t GetNULLFreePage()
{
  uint32_t new_page = GetFreePage();
  uint32_t page_add = new_page * 1024;

  for (uint32_t i = page_add; i < page_add + 1024; ++i)
      memory[i] = 0;
  return new_page;  
}

int GetFreeThread()
{
  int i = 0;
  for(i = 0;i<64;++i)
  {
    if(used_thrs[i]==false)
      break;
  }
  used_thrs[i] = true;
  return i;
}

uint32_t EditPage(uint32_t page_table_root, bool add)
{
    uint32_t new_page;
    page_table_root = page_table_root >> 2;
    uint32_t first_lvl;
    uint32_t limit = page_table_root + 1024;

    for (first_lvl = page_table_root; first_lvl < limit; first_lvl++)
        if (!(memory[first_lvl] & CCPU::BIT_PRESENT)) 
            break;

    if (first_lvl == page_table_root) {
        new_page = GetNULLFreePage();
        memory[first_lvl] = (new_page << 12) | 7;
    } 
    else 
        first_lvl--;
    
    uint32_t second_lvl = (memory[first_lvl] & CCPU::ADDR_MASK) >> 2;
    uint32_t second_lvl_last;
    limit = second_lvl + 1024;

    for (second_lvl_last = second_lvl; second_lvl_last < limit; ++second_lvl_last)
        if (!(memory[second_lvl_last] & CCPU::BIT_PRESENT)) 
            break;

    if(add)
    {
        if (second_lvl_last == limit) {
            new_page = GetFreePage();
            memory[first_lvl + 1] = (new_page << 12) | 7;
            second_lvl_last = new_page * 1024;
        }
        new_page = GetFreePage();
        memory[second_lvl_last] = (new_page << 12) | 7;
        return new_page << 12;
    }
    else
    {
        uint32_t page;
        second_lvl_last--;
        page = memory[second_lvl_last] >> 12;
        free_pages[page] = true;
        num_free_pages++;
        memory[second_lvl_last] = 0;

        if (second_lvl_last == second_lvl) {
            free_pages[memory[first_lvl] >> 12] = true;
            memory[first_lvl] = 0;
            num_free_pages++;
        }
        return page;
    }
}


uint32_t HardCopyMemory(uint32_t page_table_root) 
{
    uint32_t new_page_root = GetNULLFreePage();
    uint32_t first_lvl = 0;
    uint32_t second_lvl = 0;
    uint32_t mem_first_lvl = page_table_root;

    do
    {
        uint32_t new_second_lvl_table = GetFreePage();
        memory[(new_page_root << 10) + first_lvl] = (new_second_lvl_table << 12) | 7;
        uint32_t mem_second_lvl = (memory[mem_first_lvl] & CCPU::ADDR_MASK) >> 2;

        do
        {
            uint32_t new_page = GetFreePage();

            memcpy( &memory[new_page << 10], 
                    &memory[ (memory[mem_second_lvl] & CCPU::ADDR_MASK) >> 2], 
                    1024 * sizeof(uint32_t));

            memory[(new_second_lvl_table<<10) + second_lvl] = (new_page << CCPU::OFFSET_BITS) | 7;
            second_lvl++;
            mem_second_lvl++;

        } while (memory[mem_second_lvl] & 1);

        second_lvl = 0;
        first_lvl++;
        mem_first_lvl++;

    } while (memory[mem_first_lvl] & 1);

    return new_page_root<<12;
}


bool CImpCCPU::NewProcess(void * processArg, void (* entryPoint) (CCPU *, void *), bool copyMem) 
{         
    uint32_t mem = 0;
    uint32_t new_page_root;
    pthread_mutex_lock(&page_mutex);
    if (copyMem) 
    {
        new_page_root = HardCopyMemory(m_PageTableRoot);
        mem = num_proc_pages;
    } 
    else 
    {
        new_page_root = GetNULLFreePage();
        new_page_root = new_page_root << 12;
    }

    param_for_create* params = new param_for_create(new_page_root, processArg, entryPoint, mem);
    int index_thread = GetFreeThread();
    pthread_create(&threads[index_thread],&attr,createFunc,params); //TODO
    pthread_mutex_unlock(&page_mutex);
    return true;
}

uint32_t CImpCCPU::GetMemLimit(void) const 
{
    return num_proc_pages;
}

bool CImpCCPU::SetMemLimit(uint32_t pages)
{
    if (pages == num_proc_pages) return true;

    pthread_mutex_lock(&page_mutex);
    uint32_t diff = pages - num_proc_pages;
    bool add = (int32_t)diff > 0;
    diff = add ? diff : -diff;
    
    for (uint32_t i = 0; i < diff; i++)
        EditPage(m_PageTableRoot, add);


    num_proc_pages = pages;
    pthread_mutex_unlock(&page_mutex);
    return true;
}


void MemMgr(void* mem, uint32_t totalPages, void* processArg, void (* mainProcess) (CCPU *, void *)) 
{
    memory = (uint32_t*) mem;
    free_pages = new bool[totalPages];
    num_free_pages = num_all_pages = totalPages;

    pthread_mutex_init ( &page_mutex, NULL );
    pthread_attr_init ( &attr );
    pthread_attr_setdetachstate ( &attr, PTHREAD_CREATE_JOINABLE );
    pthread_mutex_lock(&page_mutex);

    for(uint32_t i = 0; i < num_all_pages; ++i)
        free_pages[i] = true;
    
    for(int i=0;i<65;i++){
        used_thrs[i] = false;
    }

    uint32_t page_table_root = GetNULLFreePage();
    page_table_root = page_table_root << 12;
    param_for_create* params = new param_for_create(page_table_root, processArg, mainProcess);
    pthread_mutex_unlock(&page_mutex);
    createFunc(params);

    void* ret = NULL;
    for(int i=0;i<65;i++){
        if(used_thrs[i] != false) {
            pthread_join(threads[i],&ret);
        }
    }
    delete [] free_pages;
}

