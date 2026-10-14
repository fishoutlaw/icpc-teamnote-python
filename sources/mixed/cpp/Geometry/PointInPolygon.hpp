#pragma once
#include "Template.hpp"
// Based on code/Geometry/PointInPolygon.cpp. Simple polygon, O(N), O(1) space.
namespace tn {
bool point_in_polygon(const vector<Point>& points,Point p) {
    int n=points.size(),winding=0;
    for (int i=0;i<n;i++) {
        Point a=points[i],b=points[(i+1)%n]; i128 c=orient(a,b,p);
        if (on_segment(a,b,p)) return true;
        if (a.second<=p.second && p.second<b.second && c>0) ++winding;
        if (b.second<=p.second && p.second<a.second && c<0) --winding;
    }
    return winding!=0; // boundary included
}
}
