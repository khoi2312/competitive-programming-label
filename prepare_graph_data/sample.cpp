using namespace std;
long GCD(long a,long b)
{
    if(b==0)return a;

    return GCD(b,a%b);
}
long long bigMod(long long b,long long p, long long m)
{

    if(b == 1)
        return b;
    if(p == 0 )return 1;
    if( p == 1)return b;
    if(p%2 == 0)
    {
        long long temp = bigMod(b,p/2,m);
        return (temp*temp)%m;
    }
    else
        return (b * bigMod(b,p-1,m))%m;
}


long long modInverse(long long a,long long m)
{


    return bigMod(a,m-2,m);

}
int inp[404][404];
int mark[404];

struct info{

    int u,v,w;


};


bool comp(info a,info b){

    if(a.w>b.w)return true;

    return false;
}

int ans[404];


int main()
{
    vector<info>pq;
    int n;
    cin>>n;

    for(int i = 2; i<=2*n;i++){

        for(int j = 1; j<i;j++){

            int a = ({ long tt2; scanf("%ld",&tt2); tt2;});
            info tmp;
            tmp.u = i;
            tmp.v = j;
            tmp.w = a;
            pq.push_back(tmp);
        }
    }


    sort(pq.begin(),pq.end(),comp);

    for(int i=0;i<pq.size();i++){

        if(ans[pq[i].u] == 0 && ans[pq[i].v]== 0){

            ans[pq[i].u] = pq[i].v;
            ans[pq[i].v] = pq[i].u;
        }
    }

    for(int i=1;i<=2*n;i++)
    {

        if(i!= 1)cout<<" ";

        cout<<ans[i];
    }
    cout<<endl;
    return 0;
}