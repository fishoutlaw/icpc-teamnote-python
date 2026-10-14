#pragma once
#include "Template.hpp"
// 단조 체인으로 볼록 껍질을 구한다. O(N log N).
namespace tn {
vector<Point> convex_hull(vector<Point> p) {
    sort(p.begin(),p.end()); p.erase(unique(p.begin(),p.end()),p.end());
    if (p.size()<2) return p;
    auto chain=[](const vector<Point>& points) {
        vector<Point> out;
        for (Point x:points) {
            while (out.size()>1 && orient(out[out.size()-2],out.back(),x)<=0) out.pop_back();
            out.push_back(x);
        }
        return out;
    };
    auto a=chain(p); reverse(p.begin(),p.end()); auto b=chain(p);
    a.pop_back(); b.pop_back(); a.insert(a.end(),b.begin(),b.end()); return a;
} // 반시계 껍질, 끝점 중복 없음. 일직선 입력은 양 끝점만 남긴다.
}
