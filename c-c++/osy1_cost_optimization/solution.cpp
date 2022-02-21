#ifndef __PROGTEST__
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <climits>
#include <cfloat>
#include <cassert>
#include <cmath>
#include <iostream>
#include <iomanip>
#include <algorithm>
#include <numeric>
#include <string>
#include <vector>
#include <array>
#include <iterator>
#include <set>
#include <list>
#include <map>
#include <unordered_set>
#include <unordered_map>
#include <queue>
#include <stack>
#include <deque>
#include <memory>
#include <functional>
#include <thread>
#include <mutex>
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <pthread.h>
#include <semaphore.h>
#include "progtest_solver.h"
#include "sample_tester.h"
using namespace std;
#endif /* __PROGTEST__ */ 

class CCargoPlanner
{
  public:
    static int               SeqSolver                     ( const vector<CCargo> & cargo,
                                                             int               maxWeight,
                                                             int               maxVolume,
                                                             vector<CCargo>  & load );
    void                     Start                         ( int               sales,
                                                             int               workers );
    void                     Stop                          ( void );

    void                     Customer                      ( ACustomer         customer );
    void                     Ship                          ( AShip             ship );
    void                     ManageWorkingThread           ( int i);
    void                     ManageSalesThread             ( int i);
    
    vector<thread>   threads_sales;
    vector<thread>   threads_worked;
    vector<ACustomer> my_customers;
    list <AShip> my_ships;
    queue <pair<AShip, vector<CCargo>>> queue_ship_cargos;

    mutex work_ships;
    mutex work_worked;

    condition_variable check_ship;
    condition_variable check_worked;

    atomic<bool> last_ship = false;
    atomic<bool> finish_sales = false;
};

int CCargoPlanner::SeqSolver(const vector<CCargo> & cargo,int maxWeight, int maxVolume, vector<CCargo> & load )
{
    return ProgtestSolver(cargo, maxWeight, maxVolume, load);
}


void CCargoPlanner::ManageSalesThread(int i)
{
  while(1)
  {
    unique_lock<mutex>  locker ( work_ships );
    vector<CCargo> all_cargo;
    if(!my_ships.empty())
    {
      auto ship = my_ships.front();
      my_ships.pop_front();
      string dest = ship->Destination();
      locker.unlock();
      for(auto customer:my_customers)
      {
        vector<CCargo> cur_cargo;
        customer->Quote(dest, cur_cargo);
        all_cargo.insert(all_cargo.end(), cur_cargo.begin(), cur_cargo.end());
      }
      
      // cout<<ship->Destination()<<endl;
      // for(auto cargo:all_cargo)
      // {
      //   cout<<cargo.m_Volume<<endl;
      // }
      
      unique_lock <mutex> locker (work_worked);
      queue_ship_cargos.push((make_pair(ship, all_cargo)));
      check_worked.notify_one();
      // locker.unlock();

    }
    else if (!last_ship)
    {
      check_ship.wait(locker);
    }
    else
    {
      break;
    } 
  }

}

void CCargoPlanner::ManageWorkingThread(int i)
{
  while(1)
  {
    unique_lock<mutex>  locker ( work_worked );
    if(!queue_ship_cargos.empty())
    {
      auto pair = queue_ship_cargos.front();
      queue_ship_cargos.pop();
      locker.unlock();
      vector<CCargo> vec_load;

      ProgtestSolver(pair.second, pair.first->MaxWeight(), pair.first->MaxVolume(), vec_load);
      
      pair.first->Load(vec_load);
    }
    else if (!finish_sales)
    {
      check_worked.wait(locker);
    }
    else
    {
      break;
    }
  }
}
void CCargoPlanner::Start ( int sales, int workers)
{
  for(int i=0; i<sales; i++)
  {
    threads_sales.push_back(thread(&CCargoPlanner::ManageSalesThread, this, i));
  }
  for (int i = 0; i < workers; i++)
  {
    threads_worked.push_back(thread(&CCargoPlanner::ManageWorkingThread, this, i));
  }
}

void CCargoPlanner::Stop (void)
{
  last_ship = true;
  check_ship.notify_all();
  for(thread& thr_sales: threads_sales)
  {
    thr_sales.join();
  }
  
  finish_sales = true;
  check_worked.notify_all();
  for(thread& thr_worked: threads_worked)
  {
    thr_worked.join();
  }
}

void CCargoPlanner::Customer ( ACustomer customer)
{
  my_customers.push_back(customer);
}

void CCargoPlanner::Ship (AShip ship)
{
  my_ships.push_back(ship);
  check_ship.notify_one();
}

// TODO: CCargoPlanner implementation goes here
//-------------------------------------------------------------------------------------------------
#ifndef __PROGTEST__
int                main                                    ( void )
{
  CCargoPlanner  test;
  vector<AShipTest> ships;
  vector<ACustomerTest> customers { make_shared<CCustomerTest> (), make_shared<CCustomerTest> () };
  
  ships . push_back ( g_TestExtra[0] . PrepareTest ( "New York", customers ) );
  ships . push_back ( g_TestExtra[1] . PrepareTest ( "Barcelona", customers ) );
  ships . push_back ( g_TestExtra[2] . PrepareTest ( "Kobe", customers ) );
  ships . push_back ( g_TestExtra[8] . PrepareTest ( "Perth", customers ) );
  // add more ships here
  
  for ( auto x : customers )
    test . Customer ( x );
  
  test . Start ( 3, 2 );
  
  for ( auto x : ships )
    test . Ship ( x );

  test . Stop  ();

  for ( auto x : ships )
    cout << x -> Destination () << ": " << ( x -> Validate () ? "ok" : "fail" ) << endl;
  return 0;  
}
#endif /* __PROGTEST__ */ 
