#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_core_read.h>
#include <bpf/bpf_tracing.h>
#include "event.h"

char LICENSE[] SEC("license") = "Dual BSD/GPL";


//Ring Buffer Definition
struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 1 << 24); // CAPS AT 16MB
}   events SEC(".maps");

const volatile __u32 self_pid = 0; //So we dont trace our own process, this is set in the user space program

static __always_inline int // shows function body, not the function call, more optimal for performance
emit(void *ctx, __u32 type, const char *path_ptr){ // pointer to anything, typeof event, pointer to exec path -- >character (const).
    struct event *e;
    struct task_struct *task;
    
    // We don want to trace our own process, so we check if the current process ID is equal to self_pid. If it is, we return 0 and do not emit an event.
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (pid == self_pid) {
        return 0;
    }


    // allocates a block of memory inside the ring bugger matching the size of a struct event
    e = bpf_ringbuf_reserve(&events, sizeof(*e), 0); // e-> ring buff, sizeof(*e) number of bytes to reserve, flags arg -> 0

    task = (struct task_struct *)bpf_get_current_task();

    e->ts_ns = bpf_ktime_get_ns();

    e->pid = pid;
    e->ppid = BPF_CORE_READ(task,real_parent, tgid);
    e->uid = get_current_uid_gid();
    e->type = type;
    
    bpf_get_current_comm(&e->comm, sizeof(e->comm)); // What is the name of the current process?
    bpf_probe_read_user_str(&e->path, sizeof(e->path), path_ptr); 

    bpf_ringbuf_sumbit(e, 0);  //sends event to ring buffer
    
    return 0;

    SEC("tracepoint/syscalls/sys_enter_execve") // Create the Tracepoint

    int execve_handler(struct trace_event_raw_sys_enter *ctx) // What triggers eBPF program?
    { 
        return emit(ctx, EVT_EXEC, (const char *)ctx->args[0]);
    }

    SEC("tracepoint/syscalls/sys_enter_openat") // Create Another Tracepoint

    int open_handler(struct trace_event_raw_sys_enter * ctx)

    {
        return emit(ctx, EVT_OPEN, (const char *)ctx->args[1]);
    }



}

#endif