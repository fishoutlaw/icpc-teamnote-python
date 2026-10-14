#include "../mixed/cpp/Graph1/Dijkstra.hpp"
#include "../mixed/cpp/Graph1/Floyd.hpp"
#include "../mixed/cpp/Graph1/Bellman.hpp"
#include "../mixed/cpp/Graph1/Kruskal.hpp"
#include "../mixed/cpp/DataStructure/SegmentTree.hpp"
#include "../mixed/cpp/DataStructure/SegmentTreeLazy.hpp"
#include "../mixed/cpp/DataStructure/PersistentSegmentTree.hpp"
#include "../mixed/cpp/DataStructure/ConvexHullTrick.hpp"
#include "../mixed/cpp/Graph2/SCC.hpp"
#include "../mixed/cpp/Graph2/BCC.hpp"
#include "../mixed/cpp/Graph2/Dinic.hpp"
#include "../mixed/cpp/Graph2/MCMF.hpp"
#include "../mixed/cpp/Graph2/Hopcroft.hpp"
#include "../mixed/cpp/Graph2/LCA.hpp"
#include "../mixed/cpp/Graph2/HLD.hpp"
#include "../mixed/cpp/Math/ChineseRemainderTheorem.hpp"
#include "../mixed/cpp/Math/LinearSieve.hpp"
#include "../mixed/cpp/Math/MillerRabin-PollardRho.hpp"
#include "../mixed/cpp/Math/Matrix.hpp"
#include "../mixed/cpp/Math/Convolution.hpp"
#include "../mixed/cpp/String/Hashing.hpp"
#include "../mixed/cpp/String/KMP.hpp"
#include "../mixed/cpp/String/Z.hpp"
#include "../mixed/cpp/String/Manacher.hpp"
#include "../mixed/cpp/String/SuffixArray.hpp"
#include "../mixed/cpp/Geometry/Template.hpp"
#include "../mixed/cpp/Geometry/PolarSort.hpp"
#include "../mixed/cpp/Geometry/SegmentIntersection.hpp"
#include "../mixed/cpp/Geometry/PointInPolygon.hpp"
#include "../mixed/cpp/Geometry/ConvexHull.hpp"
#include "../mixed/cpp/Geometry/Calipers.hpp"
#include "../mixed/cpp/Geometry/PointInConvexPolygon.hpp"
#include "../mixed/cpp/Misc/LIS.hpp"
#include "../mixed/cpp/Misc/FastIO.hpp"
using namespace tn;
template<class T> vector<T> read_vector(int n) { vector<T> a(n); for (auto& x:a) cin>>x; return a; }
template<class T> void print_vector(const vector<T>& a) { cout<<a.size()<<' '; for (auto x:a) cout<<x<<' '; }
void print128(i128 n) {
    if (n<0) { cout<<'-'; n=-n; }
    string s; do { s+=char('0'+n%10); n/=10; } while (n);
    reverse(s.begin(),s.end()); cout<<s;
}
void fraction(i128 n,i128 d) {
    i128 a=n<0?-n:n,b=d; while (b) { i128 r=a%b; a=b;b=r; }
    print128(n/a); cout<<'/'; print128(d/a); cout<<' ';
}
void distances(const vector<ll>& a) {
    for (ll x:a) { if (x==INF) cout<<"X "; else cout<<x<<' '; }
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    string op;
    while (cin>>op) {
        if (op=="dist") {
            int n,m,s,t; cin>>n>>m>>s>>t;
            vector<tuple<int,int,ll>> e; vector<vector<pair<int,ll>>> g(n);
            for (int i=0,u,v;i<m;i++) { ll w; cin>>u>>v>>w;e.push_back({u,v,w});g[u].push_back({v,w}); }
            auto [d,p]=dijkstra(g,s); distances(d); print_vector(restore_path(p,s,t));
            auto f=floyd_warshall(n,e); for (auto& row:f) distances(row);
        } else if (op=="bell") {
            int n,m,s; cin>>n>>m>>s; vector<tuple<int,int,ll>> e;
            for (int i=0,u,v;i<m;i++) { ll w;cin>>u>>v>>w;e.push_back({u,v,w}); }
            auto d=bellman_ford(n,e,s); if (d) distances(*d); else cout<<"NEG";
        } else if (op=="mst") {
            int n,m; cin>>n>>m; vector<tuple<ll,int,int>> e;
            for (int i=0,u,v;i<m;i++) { ll w; cin>>w>>u>>v;e.push_back({w,u,v}); }
            auto [cost,chosen]=kruskal(n,e); cout<<cost<<' '<<chosen.size();
        } else if (op=="seg") {
            int n,q; cin>>n>>q; auto a=read_vector<ll>(n); SegmentTree st(a);
            while (q--) { int type,l,r;ll x;cin>>type>>l;
                if (type==0) { cin>>x;st.set(l,x); } else { cin>>r;cout<<st.sum(l,r)<<' '; } }
        } else if (op=="lazy") {
            int n,q; cin>>n>>q; LazySegmentTree st(n);
            while (q--) { int type,l,r;ll x;cin>>type>>l>>r;
                if (type==0) { cin>>x;st.add(l,r,x); } else cout<<st.sum(l,r)<<' '; }
        } else if (op=="pst") {
            int n,m,q;cin>>n>>m>>q; PersistentSegmentTree st(n);
            for (int i=0,x;i<m;i++) {cin>>x;st.insert(i,x);}
            while (q--) {int l,r,k;cin>>l>>r>>k;cout<<st.kth(l,r,k)<<' ';}
        } else if (op=="cht") {
            int n,q;cin>>n>>q;vector<pair<ll,ll>> lines(n);LiChao lc(-100,100);MonotoneCHT mono;
            for (auto& [a,b]:lines) {cin>>a>>b;lc.add(a,b);} sort(lines.begin(),lines.end());
            for (auto [a,b]:lines) mono.add(a,b);
            while(q--) {ll x;cin>>x;cout<<mono.query(x).first<<' '<<lc.query(x)<<' ';}
        } else if (op=="scc") {
            int n,m;cin>>n>>m;vector<vector<int>> g(n);
            for(int i=0,u,v;i<m;i++){cin>>u>>v;g[u].push_back(v);}
            auto [c,groups]=strongly_connected_components(g);
            for(int u=0;u<n;u++){for(int v=0;v<n;v++)cout<<(c[u]==c[v])<<' ';
                for(int v:g[u])assert(c[u]<=c[v]);}
        } else if (op=="bcc") {
            int n,m;cin>>n>>m;vector<pair<int,int>> e(m);for(auto& [u,v]:e)cin>>u>>v;
            auto out=biconnected_components(n,e);int cuts=0;u64 bridges=0;
            for(int v:out.cuts)cuts|=1<<v;for(int i:out.bridges)bridges|=1ULL<<i;
            vector<int> masks;for(auto& g:out.groups){int mask=0;for(int v:g)mask|=1<<v;masks.push_back(mask);}
            sort(masks.begin(),masks.end());cout<<cuts<<' '<<bridges<<' ';print_vector(masks);
        } else if (op=="flow") {
            int n,m;cin>>n>>m;Dinic flow(n);vector<tuple<int,int,ll>> edges;
            for(int i=0,u,v;i<m;i++){ll c;cin>>u>>v>>c;flow.add_edge(u,v,c);edges.push_back({u,v,c});}
            ll answer=flow.max_flow(0,n-1);auto [a,b]=flow.min_cut(0);set<int> side(a.begin(),a.end());
            ll cut=0;for(auto [u,v,c]:edges)if(side.count(u)&&!side.count(v))cut+=c;
            assert(cut==answer);cout<<answer<<' '<<flow.max_flow(0,n-1);
        } else if (op=="cost") {
            int n,m;ll limit;cin>>n>>m>>limit;MinCostFlow flow(n);
            for(int i=0,u,v;i<m;i++){ll c,w;cin>>u>>v>>c>>w;flow.add_edge(u,v,c,w);}
            try {auto [f,c]=flow.run(0,n-1,limit);cout<<f<<' '<<c;}
            catch(const invalid_argument&){cout<<"NEG";}
        } else if (op=="match") {
            int n,m,k;cin>>n>>m>>k;vector<vector<int>> g(n);
            for(int i=0,u,v;i<k;i++){cin>>u>>v;g[u].push_back(v);}auto out=hopcroft_karp(g,m);
            int size=0;for(int v=0;v<n;v++)if(out.left[v]!=-1){++size;assert(out.right[out.left[v]]==v);}
            set<int>a(out.cover_left.begin(),out.cover_left.end()),b(out.cover_right.begin(),out.cover_right.end());
            assert(int(a.size()+b.size())==size);for(int v=0;v<n;v++)for(int u:g[v])assert(a.count(v)||b.count(u));
            cout<<size;
        } else if (op=="tree") {
            int n,q;cin>>n>>q;vector<vector<int>> g(n);
            for(int i=1,u,v;i<n;i++){cin>>u>>v;g[u].push_back(v);g[v].push_back(u);}
            LCA lca(g);HLD hld(g);vector<ll>a(n);for(int v=0;v<n;v++)a[hld.pos[v]]=v+1;SegmentTree st(a);
            while(q--){int u,v;cin>>u>>v;ll sum=0,esum=0;
                for(auto [l,r]:hld.path_ranges(u,v))sum+=st.sum(l,r);
                for(auto [l,r]:hld.path_ranges(u,v,true))esum+=st.sum(l,r);
                auto [l,r]=hld.subtree_range(u);cout<<lca.query(u,v)<<' '<<sum<<' '<<esum<<' '<<st.sum(l,r)<<' ';}
        } else if (op=="crt") {
            int n;cin>>n;vector<pair<ll,ll>> e(n);for(auto& [a,m]:e)cin>>a>>m;
            auto out=crt(e);if(out)cout<<out->first<<' '<<out->second;else cout<<"NONE";
        } else if (op=="sieve") {
            int n;cin>>n;LinearSieve s(n);print_vector(s.primes);
            for(int i=0;i<=n;i++)cout<<s.spf[i]<<' '<<s.phi[i]<<' '<<s.mu[i]<<' '<<s.tau[i]<<' '<<s.sigma[i]<<' ';
        } else if (op=="prime") {
            u64 n;cin>>n;cout<<is_prime64(n)<<' ';auto f=factorize64(n);cout<<f.size()<<' ';
            for(auto [p,e]:f)cout<<p<<' '<<e<<' ';
        } else if (op=="matrix") {
            int n,m;ll mod;cin>>n>>m>>mod;vector<vector<ll>>a(n);for(auto& row:a)row=read_vector<ll>(m);
            auto out=gauss(a,ModOps{mod});cout<<out.rank<<' ';
            if(out.determinant)cout<<*out.determinant<<' ';else cout<<"NONE ";
            for(auto& row:out.rref)for(ll x:row)cout<<x<<' ';
            if(out.inverse){cout<<"INV ";for(auto& row:*out.inverse)for(ll x:row)cout<<x<<' ';}else cout<<"NONE";
        } else if (op=="real") {
            vector<vector<long double>> a{{0,2,1},{1,0,3},{4,1,8}};auto out=gauss(a,RealOps{});
            assert(out.rank==3 && out.inverse);assert(abs(*out.determinant-9)<1e-10L);
            for(int i=0;i<3;i++)for(int j=0;j<3;j++){long double x=0;
                for(int k=0;k<3;k++)x+=a[i][k]*(*out.inverse)[k][j];assert(abs(x-(i==j))<1e-10L);}
            cout<<"OK";
        } else if (op=="conv") {
            int n,m;ll mod;cin>>n>>m>>mod;auto a=read_vector<ll>(n),b=read_vector<ll>(m);
            print_vector(multiply_mod(a,b,mod));print_vector(multiply_fft(a,b));
        } else if (op=="bitconv") {
            int n;char kind;cin>>n>>kind;auto a=read_vector<ll>(n),b=read_vector<ll>(n);
            print_vector(bitwise_convolution(a,b,kind));
        } else if (op=="strings") {
            string s,p;cin>>quoted(s)>>quoted(p);print_vector(kmp(s,p));print_vector(z_function(s));
            print_vector(manacher(s));auto [sa,lcp]=suffix_array(s);print_vector(sa);print_vector(lcp);
            Hashing h(s);for(int l=0;l<=int(s.size());l++)for(int r=l;r<=int(s.size());r++)cout<<h.get(l,r)<<' ';
        } else if (op=="geometry") {
            int n,q;cin>>n>>q;vector<Point>p(n);for(auto& [x,y]:p)cin>>x>>y;
            auto h=convex_hull(p);cout<<h.size()<<' ';for(auto [x,y]:h)cout<<x<<' '<<y<<' ';
            auto far=calipers(h);if(far)print128(distance_squared(far->first,far->second));else cout<<"NONE";cout<<' ';
            auto sorted=polar_sort(p);for(auto [x,y]:sorted)cout<<x<<' '<<y<<' ';
            while(q--){Point x;cin>>x.first>>x.second;cout<<point_in_polygon(h,x)<<' '<<point_in_convex_polygon(h,x)<<' ';}
            assert(dot({1,2},{3,4})==11 && cross({1,2},{3,4})==-2);
        } else if (op=="intersection") {
            Point a,b,c,d;cin>>a.first>>a.second>>b.first>>b.second>>c.first>>c.second>>d.first>>d.second;
            auto out=segment_intersection(a,b,c,d);cout<<out.kind<<' ';
            if(out.kind==1){fraction(out.xnum,out.den);fraction(out.ynum,out.den);}
        } else if (op=="lis") {
            int n;cin>>n;print_vector(lis(read_vector<ll>(n)));
        } else if (op=="io") {
            string s;cin>>quoted(s);FILE* f=tmpfile();assert(f);fwrite(s.data(),1,s.size(),f);rewind(f);
            FastInput input(f);vector<ll> out;ll x;while(input.read(x))out.push_back(x);print_vector(out);fclose(f);
        } else { cerr<<"Unknown operation "<<op;return 2; }
        cout<<'\n';
    }
}
