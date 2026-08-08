## Behavioral Anomaly Detector ##


An on-device Behavioral Anomaly Detection System. It leanrns what normal machine activity looks like by actively observing a Linux Kerel using eBPF. Following the training phase, My Detection model will be compressed and deployed onto a _Android Phone Device->Samsung Ultra S21 (2021)_ to measure the quatization costs of accuracy versus what it buys it latency, power and memory.

### Goal ###

Most security monitoring data is processed and analyzed on the cloud. Although this has been the common practice, constraints like latency, memeory and power proves to be inefficient for edge devices. Using kernel technologies like eBPF I will collect raw kernel data to train a lightweight detection model using synthetic anomalies, so the analysis occurs natively (on device) within a real device's power, thermal, and memory constraints.

For this project I will use the Samsung Galaxy S21 Ultra 5G (2021-release). *** The Phone is not doing the detection itself, I am using this device as my edge deployment target and benchmark rig. *** The device will be used to measure the accuracy versus efficiency tradeoff of compressing an anomaly-detection model for edge deployment, validated on real mobile hardware under sustained load. I will "stress the device" running the model continuously until the device reaches higher temperatures to measure how performance degrades to show the difference between a benchmark number compared to a number that holds up when scaled. 


## Test Device Specifications

### Samsung Galaxy S21 Ultra 5G (2021) — Exynos 2100 Variant

**SoC**
- Processor: Samsung Exynos 2100 (5nm EUV)
- CPU: Octa-core ARM Cortex architecture
  - 1x Cortex-X1 @ 2.9 GHz
  - 3x Cortex-A78 @ 2.8 GHz
  - 4x Cortex-A55 @ 2.2 GHz
- GPU: ARM Mali-G78 MP14
- NPU: Dual-core AI accelerator

**Memory**
- RAM: 12GB LPDDR5
- Memory bandwidth: Up to 51.2 GB/s
- Storage: UFS 3.1
- Storage option: 128GB

**Power**
- Battery: 5000 mAh
- Battery energy: ~19.4 Wh
- Charging:
  - 25W wired charging
  - 15W wireless charging

**Software Environment**
- Architecture: ARM64 (aarch64)
- Kernel: Linux-based Android kernel
- Target use: eBPF process monitoring and anomaly detection experiments

### Tech Stack

- **C** -> (userspace collector) collects raw kernel data from RingBuff Map Type
- **Python -> Pandas** -> (analysis and quantization)
- **eBPF** -> (kernel-side event collection)
- **libbpf + CO-RE** -> (precompiled, Compile Once Run Everywhere workflow)
- **bpftool** -> (generates vmlinux.h and skeleton headers)
- **Clang/LLVM** -> (build compiles the BPF C to bytecode)
- **Scikit-learn** -> Isolation Forest highly efficient ML algorithm for anomaly detection


## Project Structure ## 

<img width="1063" height="504" alt="anomaly-monitor-structure (1)" src="https://github.com/user-attachments/assets/e5c321d7-7539-4e44-b453-591042c159d3" />

