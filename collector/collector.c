#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <unistd.h>
#include <bpf/libbpf.h>
#include "collector.skel.h"
#include "event.h"

static volatile sig_atomic_t stop; //Flag Variable 

static __u64 boot_epoch_ns; 

static void on_signal(int sig) {(void)sig; stop = 1;} // listens for CTRL+C to end program safely.

static void calc_boot(void) {
    struct timespec rt, mono; // timespec struct, stores timestamp
    clock_gettime(CLOCK_REALTIME, &rt);
    clock_gettime(CLOCK_MONOTONIC, &mono);
    //            what clock to access, where to store?

    boot_epoch_ns = ((__u64)rt.tv_sec * 1000000000Ull + rt.tv_sec)
                    - ((__u64)mono.tv_sec * 1000000000 + mono.tv_sec);

    // bpf_ktime_get_ns() -> records in nanoseconds (MONOTONIC CLOCK)
    // Combined both MONO and RT CLOCK to map kernel event times to real timestamps
}

static void json_escape(char *dst, size_t cap, const char *src) {
    size_t j = 0;
    for(size_t i = 0; src[i] && j + 2 < cap; i++) {
        unsigned char c = (unsigned char)src[i];
        if (c == '"' || c == '\\') {dst[j++] = '\\'; dst[j++] = c; }
        // JSON Escaper, prevents special characters from break JSON Data Structure
        else if(c >= 0x20)  {dst[j++] = c;}

        // "Hello "World""" --> a case where JSON ESC is needed
        // Program detects strings ends at "Hello" and leaves World outside invalid
        //Here whenever a = is detected we add a \ to dst and c which is src[i]

        
    }
    dst[j] = '\0';
}