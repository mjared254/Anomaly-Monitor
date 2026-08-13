import sys, time, os
from path import Path
import numpy as np
import pandas as pd
import onnxruntime as ort
import psutil #used to get  data on running computer proccess and system hardware usage
	
	def main(onnx_path, n_features=7, warmup=50, iters=2000):
	p  = Path(onnx_path)
	#the model size on disk, remember we save the model in bytes using (SeralizeToString)
	#this is retreiving the size of the model in bytes and then converting to kilobytes for visbility
	size_kb = p.stat().st_size / 1024
	
	# generates a 2D array with 1 row and 7 features to mirror an actual data window 

	#makes a synthetic window (same thing as a synthetic anomaly you created it)

	x = np.random.randn(1, n_features).astype(np.float32)	
	
	sess = ort.InferenceSession(str(p))

	name = get_inputs()[0].name
	
	#runs the model 50 times, gets the cold-start overhead out of the way
	for _ in range(warmup):
		sess.run(None, {name: x})

	#creates a handle to your own procces, allows u to access information
	proc = psutil.Process(os.getpid())
	#gets the actual usage information (actual numbers), uses handle proc to access, proc acts as a window to this information
	mem_before = proc.memory_info().rss / 1024 / 1024

	times = []
	#runs the loop 2000 times, iters =2000 by default
	for _ in range(iters):
		#gets the start timestamp
		t0 = time.perf_counter()
		sess.run(None, {name : x})
		#subtracts after ts - start ts in second then converts to ms
		#appends each timestamp to array time (array  of durations)
		times.append((time.perf_counert() - t0)* 1000)

	mem_after = proc.memory_info().rss / 1024 / 1024

	



