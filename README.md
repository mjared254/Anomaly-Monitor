## Behavioral Anomaly Detector ##


A behavioral anomaly detector that learns what normal activity looks like on a machine by actively watching the Linux Kernel. Following the training phase, the detection model will be compressed and deployed onto a _Android Phone Device->Samsung Ultra S21 (2021)_ to prove it is successful on a edge devices power and memory constraints.

### Goal ###

Most security monitoring data is processed and analyzed on the cloud. Although this has been the common practice, constraints like latency, privacy and battery power proves to be inefficient for edge devices. Using kernel technologies like eBPF I will collect raw kernel data to train a lightweight detection model so the analysis occurs natively (on device) ensuring efficiency and privacy.

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
- RAM: 12GB / 16GB LPDDR5
- Memory bandwidth: Up to 51.2 GB/s
- Storage: UFS 3.1
- Storage options: 128GB, 256GB, 512GB

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

## Project Structure ## 

<img width="1063" height="504" alt="anomaly-monitor-structure (1)" src="https://github.com/user-attachments/assets/e5c321d7-7539-4e44-b453-591042c159d3" />

