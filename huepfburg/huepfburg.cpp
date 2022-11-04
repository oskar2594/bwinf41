#include <iostream>
#include <map>
#include <set>
#include <utility>
#include <vector>
#include <algorithm>

using namespace std;

int main()
{
    int n_nodes, n_edges;
    cin >> n_nodes >> n_edges;
    vector<set<int>> edges;

    set<int> current_nodes_1;
    set<int> current_nodes_2;
    set<int> old_nodes_1;
    set<int> old_nodes_2;
    set<pair<int, int>> visited_pairs;
    map<int, int> single_origins_1;
    map<int, int> single_origins_2;
    map<pair<int, int>, pair<int, int>> pair_origins;

    int start_node, end_node;
    for (int i = 0; i < n_nodes; i++)
        edges.push_back(set<int>());
    for (int i = 0; i < n_edges; i++)
    {
        cin >> start_node >> end_node;
        edges.at(start_node - 1).insert(end_node - 1);
    }
    pair_origins[make_pair(0, 1)] = make_pair(-1, -1);
    visited_pairs.insert(make_pair(0, 1));
    current_nodes_1.insert(0);
    current_nodes_2.insert(1);
    bool new_pairs;
    while (true)
    {
        old_nodes_1 = set<int>(current_nodes_1.begin(), current_nodes_1.end());
        old_nodes_2 = set<int>(current_nodes_2.begin(), current_nodes_2.end());
        current_nodes_1.clear();
        current_nodes_2.clear();
        single_origins_1.clear();
        single_origins_2.clear();
        for (auto old_node : old_nodes_1)
        {
            for (auto new_node : edges.at(old_node))
            {
                current_nodes_1.insert(new_node);
                single_origins_1[new_node] = old_node;
            }
        }

        for (auto old_node : old_nodes_2)
        {
            for (auto new_node : edges.at(old_node))
            {
                current_nodes_2.insert(new_node);
                single_origins_2[new_node] = old_node;
            }
        }
        new_pairs = false;
        for (auto node_1 : current_nodes_1)
        {
            for (auto node_2 : current_nodes_2)
            {
                if (visited_pairs.count(make_pair(node_1, node_2)) == 0)
                {
                    new_pairs = true;
                    visited_pairs.insert(make_pair(node_1, node_2));
                    pair_origins[make_pair(node_1, node_2)] = make_pair(single_origins_1[node_1], single_origins_2[node_2]);
                }
                if (node_1 == node_2)
                {
                    cout << "Moeglich:"
                         << "\n";
                    vector<int> path1;
                    vector<int> path2;
                    pair<int, int> pos = make_pair(node_1, node_2);
                    while (pos.first != -1)
                    {
                        path1.push_back(pos.first);
                        path2.push_back(pos.second);
                        pos = pair_origins[pos];
                    }
                    reverse(path1.begin(), path1.end());
                    reverse(path2.begin(), path2.end());
                    cout << "Pfad 1: ";
                    for (auto node : path1)
                        cout << node + 1 << " ";
                    cout << "\nPfad 2: ";
                    for (auto node : path2)
                        cout << node + 1 << " ";
                    return 0;
                }
            }
        }
        if (new_pairs == false)
        {
            cout << "unmoeglich"
                 << "\n";
            return 0;
        }
    }
}