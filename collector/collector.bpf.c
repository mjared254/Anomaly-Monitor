#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_core_read.h>
#include <bpf/bpf_tracing.h>
#include "event.h"

char LICENSE[] SEC("license") = "Dual BSD/GPL";

struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 1 << 24);
} events SEC(".maps");

const volatile __u32 self_pid = 0;

static __always_inline int
emit(void *ctx, __u32 type, const char *path_ptr)
{
    struct event *e;
    struct task_struct *task;
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (pid == self_pid)
        return 0;

    e = bpf_ringbuf_reserve(&events, sizeof(*e), 0);
    if (!e)
        return 0;

    task = (struct task_struct *)bpf_get_current_task();

    e->ts_ns = bpf_ktime_get_ns();
    e->pid   = pid;
    e->ppid  = BPF_CORE_READ(task, real_parent, tgid);
    e->uid   = bpf_get_current_uid_gid();
    e->type  = type;

    bpf_get_current_comm(&e->comm, sizeof(e->comm));
    bpf_probe_read_user_str(&e->path, sizeof(e->path), path_ptr);

    bpf_ringbuf_submit(e, 0);
    return 0;
}

SEC("tracepoint/syscalls/sys_enter_execve")
int handle_execve(struct trace_event_raw_sys_enter *ctx)
{
    return emit(ctx, EVT_EXEC, (const char *)ctx->args[0]);
}

SEC("tracepoint/syscalls/sys_enter_openat")
int handle_openat(struct trace_event_raw_sys_enter *ctx)
{
    return emit(ctx, EVT_OPEN, (const char *)ctx->args[1]);
}
