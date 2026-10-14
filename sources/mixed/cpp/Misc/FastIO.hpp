#pragma once
#include "../common.hpp"
// 빠른 정수 입력. 먼저 동기화를 끈 cin 사용을 고려한다.
// 64KiB 버퍼 정수 입력, LLONG_MIN 포함. 시간 O(입력 크기).
// 공백으로 구분한 ll 범위의 올바른 십진 정수만 입력한다.
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
// 표준 입력은 동기화를 끈 cin으로 대체할 수 있다.
// 같은 입력에서 FastInput/fread와 비동기 cin을 혼용하지 않는다.
}
