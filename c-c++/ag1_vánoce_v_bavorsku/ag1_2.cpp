#include<iostream> 
#include<climits> 
#include <vector> 
#include<map>
#include<set>
#include<queue>

#include <bits/stdc++.h> 
using namespace std; 

struct pair_hash {
	template <class T1, class T2>
	std::size_t operator() (const std::pair<T1, T2> &pair) const {
		return std::hash<T1>()(pair.first) ^ std::hash<T2>()(pair.second);
	}
};


class CRivers
{
    public:
        void Read();
        pair<int, std::unordered_map<int, int>> SearchMin(unsigned int cur_node, unsigned int tabu_beer, set <unsigned int> visited);
        //void CRivers(){};

    private:
        unsigned int count_rest;
        unsigned int count_beer;
        unsigned int min_cost=INT_MAX;
        set <pair<unsigned int, unsigned int>> map_beer;
        map <unsigned int, unsigned int> map_rest;
        map <unsigned int, set <unsigned int> > rest_depenses;
        map <int, int> restaurace_beer;
        unordered_map<pair<int, int>, pair<int, unordered_map<int, int>>, pair_hash> map_data;

        //map <int> rest;



};


pair<int, std::unordered_map<int, int>> CRivers :: SearchMin(unsigned int cur_node, unsigned int tabu_beer, set <unsigned int> visited)
{
    unsigned int min_cost = INT32_MAX;
    unordered_map<int, int> min_map = {};
    visited.emplace(cur_node);
    bool cont=true;
    for(auto i: map_beer)
    {  
        if(tabu_beer==i.second){continue;}
            unsigned int cost = 0;
            unordered_map<int, int> cur_map = {};
            if(map_data.count({cur_node, i.second}) == 0)
            {
                if(!cont) {continue;}
                cost=i.first*map_rest[cur_node];
                
                for( auto k: rest_depenses[cur_node])
                {
                    if(visited.count(k) == 0)
                    {
                        auto res = SearchMin(k, i.second, visited);
                        cost +=res.first;
                        cur_map.insert(res.second.begin(), res.second.end());
                        
                    }
                    //cout<< i.first<<" "<< map_beer[i.second]<<endl;
                }
                map_data[{cur_node, i.second}]={cost, cur_map};                    
            }
            else
            {
                auto res = map_data[{cur_node, i.second}];
                cost = res.first;
                //cout<< i.first<<" "<< map_beer[i.second]<<endl;
                cur_map = res.second;
            }

            if (cost < min_cost) 
            {
                min_cost = cost;
                min_map = cur_map;
                //cout<< i.first<<" "<< map_beer[i.second]<<endl;
                min_map[cur_node] = i.second;
            }
            else
            {
                cont=false;
            }
    }
    return {min_cost, min_map};
}

void CRivers :: Read()
{
    cin>>count_rest>>count_beer;
    for (unsigned int i=1; i<=count_beer;i++)
    {
         int tmp;
         cin>>tmp;
         map_beer.emplace(tmp, i);
    }

    for(unsigned int i=1; i<=count_rest; i++)
    {
        int tmp;
        cin>>tmp;
        map_rest.emplace(i, tmp);
    }

    unsigned int first;
    unsigned int second;
    while(cin>>first>>second)
    {
        rest_depenses[first].insert(second);
        rest_depenses[second].insert(first);
    }

    set <unsigned int> visited;
    auto res =SearchMin(1, 0, visited);
    cout<<res.first<<endl;
    for(auto i: map_rest)
    {
        cout<<res.second[i.first]<<" ";
    }
    cout<<endl;
    
}




int main()
{
    CRivers new_rivers = CRivers();
    new_rivers.Read();

    return 0;
}