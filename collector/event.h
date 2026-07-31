#ifndef __EVENT_H
#define __EVENT_H

#ifndef __VMLINUX_H__ //avoids redefinition of types when compiling in kernel space
#include <linux/types.h>
#endif 

// PRE-PROCCESSOR DIRECTIVES (runs before C Compiler)
#define TASK_COMM_LEN 16 //CONSTANT MAX SIZE OF PROCESS NAME -> 16
#define PATH_LEN 128 //CONSTANT MAX SIZE OF PATH STRING -> 128
#endif

#define EVT_EXEC 0 //0 -> A Program Execution Event
#define EVT_OPEN 1 //1 -> A File Open Event

struct event {
    __u64 ts_ns; //64-bit unsigned integer to store the time of the event in nanoseconds

    __u32 pid; //32-bit unsigned integer to store the process ID of the event

    __u32 ppid; //32-bit unsigned integer to store the parent process ID of the event

    __u32 uid; //32-bit unsigned integer to store the user ID of the event

    __u32 type; //32-bit unsigned integer to store the type of the event (execution or file open)

    char comm[TASK_COMM_LEN];
    char path[PATH_LEN];
};

//#endif