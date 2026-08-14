## Behavioral Anomaly Detector System  ##


An on-device Behavioral Anomaly Detection System. It learns what normal machine activity looks like by actively observing a Linux Kernel using eBPF. Following the training phase, My lightweight detection model was compressed and deployed onto a **_Android Phone Device->Samsung Ultra S21 (2021)_** to measure what compression costs of accuracy versus what it buys it latency, power and memory.

### Goal ###

Most security monitoring data is processed and analyzed on the cloud. Although this has been the common practice, constraints like latency, memory and power proves to be inefficient for edge devices. Using kernel technologies like eBPF I will collect raw kernel data to train a lightweight detection model using synthetic anomalies, so the analysis occurs natively (on device) within a real device's power, thermal, and memory constraints.

For this project I will use the Samsung Galaxy S21 Ultra 5G (2021-release). **The Phone is not doing the detection itself, I am using this device as my edge deployment target and benchmark rig.** The device will be used to measure the accuracy versus efficiency tradeoff of compressing an anomaly-detection model for edge deployment, validated on real mobile hardware under sustained load. I will stressed the device by running the compressed model continuously until the device reaches higher temperatures to measure how performance degrades to show the difference between a benchmark number compared to a number that holds up when scaled. 

### Results ### Development Journal/Files -> [docs/Anomaly-Project-Journal.pdf](docs/Anomaly-Project-Journal.pdf)
 
My trained Isolation Forest model was converted to ONNX and verified conversion score-to-score against my original model on my VM before moving further with benchmarking on device, This ensured both my models were consistent to prevent any inconsistencies further on. My analysis following the Performance Test between model_fp32.onnx and model_small.onnx aimed to benchmark the costs in accuracy, latency and memory through ensemble compression reducing the number of decision trees from 200 to 40. As a result Compression cut model size by 84% and the inference latency by 5x on both x86 and ARM ,at a cost of 1.4% ranking fidelity. I found that my compressed model still ranks windows in nearly the same collective order as the full model, I found this by evaluating my Original Model (no conversion) and Compressed model to determine if both models rank windows in same order as Higher = more anomalous, Lower = normal. I used the scipy.stats module to determine ranking fidelity across both models and generated a correlation coefficient between -1 and 1, my compressed model generated a coefficient of 0.986 across 454 windows against 1.0 which lands it slightly below 1.0 denoting a slight 1.4% change in ranking fidelity signifying nearly the same collective order.

Under sustained load the Exynos 2100 held roughly ~2.31ms p50 for four passes before thermal throttling to ~3.02ms denoting a 30% degradation sustained across the remaining passes before recovering. As as a result this shows that a single-pass benchmark understates real-world edge latency on hardware, as single-pass does not present any sustain load instead may catch some of cold-overhead. To minimize the collection of cold-overhead I ran 50 warmup iterations to create some sort of thermal throttling, this enabled me to catch useful data rather than collecting cold device data that serves no use.

### Limitations ###
My initial goal was to quantize my model to measure the quantization costs of accuracy versus what it buys in latency, power and memory. Due to my model selection (Isolation Forest) this was not attainable due to quantization targets neural networks and does not apply to tree ensemble which has comparison thresholds rather than weights and matrices. This facilitated ensemble compression as Isolation Forest is tree like structure
made up of decision trees, my reducing the number of trees we can basically preform the same operations as quantization.

The Detection Model was only able to detect 1/3 synthetic anomalies at session level. Feature-level separation was achieved but Isolation Forest averages isolation across all seven dimensions where the anomalies have to be different enough across several axis. For my case anomalies were only extreme (different) across one axis resulting in dimensional dilution where my baseline-data become more prevalent or anomalous than my synthetic anomalies themselves. The bottleneck is model selection, not feature design. Moreover, my model was trained on baseline-data (normal machine activity) and evaluated using my anomalies where the model was recongizing my synthetic anomalous scripts rather than general anomalous structure.


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

<img width="1234" height="1468" alt="project-structure (1)" src="https://github.com/user-attachments/assets/f307f616-6ebb-4e32-b5ed-ad190acf2501" />

