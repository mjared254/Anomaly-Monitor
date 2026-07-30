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

    boot_epoch_ns = ((__u64)rt.tv_sec * 1000000000ULL + rt.tv_nsec)
                    - ((__u64)mono.tv_sec * 1000000000ULL + mono.tv_nsec);

    // bpf_ktime_get_ns() -> records in nanoseconds (MONOTONIC CLOCK)
    // We want to find the time the system booted.
    // Real Time - Mono (time system has been running).
}

// sanatizes the path, for any unwanted characters
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

static int event_handler(void *ctx, void * data, size_t len) {
    (void)ctx; void(len);

    const struct event *e = data;

    //Allocating memory
    char path[PATH_LEN * 2];

    //          dst array,  cap,   src -> reads the executable path
    json_escape(path, sizeof(path), e->path);

    printf("{\"ts\" :%llu, \"type\" :\"%s\", \"pid\" :%u, \"ppid\" :%u,"
           "\"uid\" :%u, \"comm\":\"%s\", \"path\" :\%s\"}\n",
           (unsigned long long)(boot_epoch_ns + e->ts_ns), // time system booted (ns) + the time an event happens after boot.
            e->type == EVT_EXEC ? "exec" : "open",
            e->pid, e->ppid, e->uid, e->comm, path);    
    return 0;
}

int main(void) {
    struct collector_bpf *skel = NULL;
    struct ring_buffer * rb = NULL;
    int err = 0;

    signal(SIGINT, on_signial);//listens for CTRL + C to terminate 
    signal(SIGTERM, on_signal);

    calc_boot();
    setvbuf(stdout, NULL, _IOLBF, 0); // Changes buffering mode, pointer and size for open file stream
    
    


}