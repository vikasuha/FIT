#include <iostream>
#include <map>
#include <set>
#include <queue>
#include <string>
#include <fstream>
#include<list>
using namespace std;

class CQuines
{
    private:
     unsigned int lenght=0;
     unsigned int step=0; 
     map<unsigned int, set<unsigned int>> graph;
     set<unsigned int> visited;
     queue<pair<unsigned int,unsigned int>> my_queue;
    public:
     void ReadQuines ()
     {
        unsigned int i=0;
        string line1="",line2="", tmp="", line="";
        getline(cin,line);
        while(i<line.size())
        {
            if(line[i]==' '||line[i]=='\n')
            {
                lenght=atoi(tmp.c_str());
                tmp.clear();
            }
            else
                tmp+=line[i];
            i++;
        }
        step=atoi(tmp.c_str());
        getline(cin,line1);
        getline(cin,line2);
        i=0;
        set<unsigned int> set_tmp;
        set_tmp.clear();
        while(i<line1.size())
        {
            if(line1[i]!='x')
            {
                if(line1[i+1]!='x')
                    set_tmp.emplace(i+1);
                if(i!=0&&line1[i-1]!='x')
                    set_tmp.emplace(i-1);
                if(line2[i+step]!='x')
                {
                    unsigned int num=0;
                    if(i+step>=lenght)
                        num=2*lenght+1;
                    else
                        num=lenght+i+1+step;
                    set_tmp.emplace(num);
                }
                graph.emplace(make_pair(i,set_tmp));
                set_tmp.clear();
            }
            i++;
        }
        i=0;
        while(i<line2.size())
        {
            if(line2[i]!='x')
            {
                if(line2[i+1]!='x')
                    set_tmp.emplace(lenght+i+1+1);
                if(i!=0&&line2[i-1]!='x')
                    set_tmp.emplace(lenght+i);
                if(line1[i+step]!='x')
                {
                    unsigned int num=0;
                    if(i+step>=lenght)
                        num=lenght;
                    else
                        num=i+step;
                    set_tmp.emplace(num);
                }
                graph.emplace(make_pair(i+lenght+1,set_tmp));
                set_tmp.clear();
            }
            i++;
        }
        i=0;

     }
     
     int FindWay()
     {
        unsigned int cur=0, cur_step=0;
        my_queue.emplace(make_pair(cur,0));
        visited.emplace(cur);
        while(!my_queue.empty())
        {
            auto cur_elem=my_queue.front();
            cur = cur_elem.first;
            cur_step=cur_elem.second;
            my_queue.pop();
            if(cur==lenght||cur==2*lenght+1)
            {
                return cur_step;
            }
            if (cur % (lenght + 1) + step >= lenght)
            {
                return cur_step + 1;
            } 
            auto my_elem=graph[cur]; 
            for(auto j: my_elem)
            {
                if (visited.find(j)==visited.end()) 
                {
                    if(j%(lenght+1)>cur_step)
                    {
                        visited.emplace(j);
                        my_queue.emplace(make_pair(j,cur_step+1));
                    }
                }
            }
         }
         return -1;
     }

};


int main()
{
    CQuines my;
    my.ReadQuines();
    cout<<my.FindWay()<<endl;
    
    return 0;
}