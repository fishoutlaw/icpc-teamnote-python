#pragma once
#include "Template.hpp"
// Based on code/Geometry/ConvexHull.cpp. Monotone chain O(N log N), O(N) space.
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
} // strict CCW hull, no duplicate endpoint; collinear input gives 2 endpoints
}
