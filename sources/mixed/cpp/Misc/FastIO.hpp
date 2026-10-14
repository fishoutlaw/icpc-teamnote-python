#pragma once
#include "../common.hpp"
// Based on code/Misc/FastIO.cpp (cgiosy). Prefer cin with sync disabled first.
// Optional buffered parser: signed ll including LLONG_MIN, O(bytes), 64 KiB buffer.
// Input must be valid decimal integers separated by whitespace, within ll range.
namespace tn {
struct FastInput {
    FILE* file; char buffer[1<<16]; size_t pos=0,size=0;
    explicit FastInput(FILE* f=stdin):file(f) {}
    int get() {
        if (pos==size) { size=fread(buffer,1,sizeof buffer,file); pos=0; if (!size) return EOF; }
        return (unsigned char)buffer[pos++];
    }
    bool read(ll& value) {
        int c; do { c=get(); } while (c!=EOF && c<=32);
        if (c==EOF) return false;
        bool negative=c=='-'; if (c=='-' || c=='+') c=get();
        u64 x=0; while ('0'<=c && c<='9') x=x*10+c-'0',c=get();
        value=negative?(x==(1ULL<<63)?LLONG_MIN:-ll(x)):ll(x); return true;
    }
};
// Standard alternative in main():
// ios::sync_with_stdio(false); cin.tie(nullptr);
// ll x; while (cin>>x) cout<<x<<'\n';
// Do not mix FastInput/fread and unsynchronized cin on the same stream.
}
