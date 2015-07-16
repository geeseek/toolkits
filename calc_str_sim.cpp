#include<iostream>
#include<string>
#include<vector>
#include<fstream>

using namespace std;

void longestCommonSubstring(const string& s1, const string& s2, string& comStr, int& pos1, int& pos2) {  
    int N = s1.size(), M = s2.size();  
    vector<vector<string> > mem(N+1, vector<string>(M+1, ""));  
    for (int i=0; i<N; ++i) {  
        for (int j=0; j<M; ++j) {  
            if (s1[i] == s2[j]) {  
                int len = mem[i][j].size();  
                if (mem[i][j] == s1.substr(i-len, len) && mem[i][j] == s2.substr(j-len, len)) {  
                    mem[i+1][j+1] = mem[i][j] + s1[i];  
                    continue;  
                }  
            }   
            mem[i+1][j+1] = mem[i+1][j].size()>=mem[i][j+1].size()? mem[i+1][j]: mem[i][j+1];  
        }  
    }  
    pos1 = N;
    pos2 = M;
    comStr = mem[N][M];
}  

int main(int argc, char** argv)
{
    ifstream dbstream;
    dbstream.open(argv[1]);
    vector<string> dbId;
    vector<string> dbname;
    string line = "";
    while (getline(dbstream, line))
    {
        size_t index = line.find_first_of(',');
        string id = line.substr(0, index);
        string name = line.substr(index + 1); 
        dbId.push_back(id);
        dbname.push_back(name);
    } 
    
    ifstream idcstream;
    idcstream.open(argv[2]);
    line = "";
    while (getline(idcstream, line))
    {
        size_t index = line.find_first_of(',');
        string id = line.substr(0, index);
        string name = line.substr(index + 1); 
        size_t len = dbId.size();
        for (size_t i = 0; i < len; ++i)
        {
            string comStr = "";
            int pos1 = 0;
            int pos2 = 0;
            longestCommonSubstring(name, dbname[i], comStr, pos1, pos2);
            double ratio1 = (double)comStr.size()/dbname[i].size();
            double ratio2 = (double)comStr.size()/name.size();
            double pos1ratio = (double)pos1 / dbname[i].size();
            double pos2ratio = (double)pos2 / name.size();
            double ratio = ratio1 * ratio2 * pos1ratio * pos2ratio;

            if (comStr.size() >= 6 &&  ratio >= 0.2
                                   && (double)comStr.size()/name.size() >= 0.2)
                cout << dbId[i] << "," << dbname[i] << "," << name << "," << comStr << "," << ratio << "," << id << endl;
        } 
    } 

}
