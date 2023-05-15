using namespace std;
int cei (int num) {
    if(num%2 != 0) return ((num/2) + 1);
    return num/2;
}
int main(){
    int t;
    cin>>t;
    while(t--)
    {
        int n;
        cin>>n;
        int a[n+1], b[n], tm[n];
        for(int i=0;i<n;i++)cin>>a[i]>>b[i];
        a[n] = 10000;
        for(int i=0;i<n;i++)cin>>tm[i];
        int  arr = a[0] + tm[0];
        int time = a[1] - b[0];
        if(b[0] - arr <= cei((b[0] - a[0]))) b[0] = arr +  cei((b[0] - a[0]));
        for(int i=1;i<n;i++) {
            arr = time + tm[i] + b[i-1];
            time = a[i+1] - b[i];
            if(b[i] - arr <= cei((b[i] - a[i]))) b[i] = arr +  cei((b[i] - a[i]));
        }
        cout<<arr<<endl;
    }
    return 0;
}