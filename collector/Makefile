CLANG ?= clang
BPFTOOL ?= bpftool
CC ?= gcc

ARCH := $(shell uname -m | sed 's/x86_64/x86/; s/aarch64/arm64/')

BPF_CFLAGS	:=	-g	-O2	-target	bpf	-D__TARGET_ARCH_$(ARCH)	-I.

CFLAGS	:=	-g	-O2	-Wall

LDLIBS	:=	-lbpf	-lelf	-lz

.PHONY:	all	clean
all:	collector

vmlinux.h:
	$(BPFTOOL) btf dump file /sys/kernel/btf/vmlinux format c > $@

collector.bpf.o: collector.bpf.c vmlinux.h event.h
	$(CLANG) $(BPF_CFLAGS) -c $< -o $@

collector.skel.h: collector.bpf.o
	$(BPFTOOL) gen skeleton $< > $@

collector: collector.c collector.skel.h event.h
	$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)

clean:
	rm -f collector collector.bpf.o collector.skel.h vmlinux.h