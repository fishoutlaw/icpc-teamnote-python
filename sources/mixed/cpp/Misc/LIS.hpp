#pragma once
#include "../common.hpp"
// 엄격히 증가하는 최장 부분 수열 O(N log N).
namespace tn {
vector<ll> lis(const vector<ll>& values) {
    vector<ll> tails,result; vector<int> ends,previous(values.size(),-1);
    for (int i=0;i<int(values.size());i++) {
        int p=lower_bound(tails.begin(),tails.end(),values[i])-tails.begin();
        if (p) previous[i]=ends[p-1];
        if (p==int(tails.size())) tails.push_back(values[i]),ends.push_back(i);
        else tails[p]=values[i],ends[p]=i;
    }
    for (int i=ends.empty()?-1:ends.back();i!=-1;i=previous[i]) result.push_back(values[i]);
    reverse(result.begin(),result.end()); return result;
} // 같은 값도 허용하려면 upper_bound 사용.
}
