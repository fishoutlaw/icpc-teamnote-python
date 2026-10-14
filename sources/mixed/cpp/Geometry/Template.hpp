#pragma once
#include "../common.hpp"
// 정수 좌표의 절댓값은 10^9 이하.
// i128로 정확한 방향 판정 O(1). 거리는 제곱값이다.
namespace tn {
using Point=pair<ll,ll>;
Point add(Point a,Point b) { return {a.first+b.first,a.second+b.second}; }
Point sub(Point a,Point b) { return {a.first-b.first,a.second-b.second}; }
i128 dot(Point a,Point b) { return i128(a.first)*b.first+i128(a.second)*b.second; }
i128 cross(Point a,Point b) { return i128(a.first)*b.second-i128(a.second)*b.first; }
i128 orient(Point a,Point b,Point c) { return cross(sub(b,a),sub(c,a)); }
int sign(i128 x) { return (x>0)-(x<0); }
int ccw(Point a,Point b,Point c) { return sign(orient(a,b,c)); }
i128 distance_squared(Point a,Point b) { return dot(sub(a,b),sub(a,b)); }
bool on_segment(Point a,Point b,Point p) { return orient(a,b,p)==0 && min(a,b)<=p && p<=max(a,b); }
}
