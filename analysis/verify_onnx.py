from pathlib import Path
import joblib
import pandas as pd
import numpy as np
import onnxruntime as ort

FEAT_DIR = Path.home() / "anomaly-monitor" / "data" / "features"

def main():
	bundle = joblib.load(FEAT_DIR / "model.joblib")
	#Unloads the bundles elements	
	model, scaler, features = bundle["model"], bundle["scaler"], bundle["features"]

	df = pd.read_csv(FEAT_DIR / "windows.csv")
	#scale the values but save them as 32-bit floats (onnx expects 32-bit)
	X = scaler.transform(df[features]).astype(np.float32)
	#-, higher = anomalous instead of higher = normal
	#evluates my Isolation Forest, nothing new yet
	sklearn_scores = -model.score_samples(X)
	

	#initializes a model 
	sess = ort.InferenceSession(str(FEAT_DIR / "model_fp32.onnx"))

	#what inputs do you have , defined in previous as initial_type get the name.
	input_name = sess.get_inputs()[0].name
	
	#return everything the model produces, hands the scaled data to input slot
	onnx_out = sess.run(None, {input_name: X})
	#take the scores, put them into a numpy array to preform math on it 
	onnx_scores = -np.asarray(onnx_out[-1].ravel())	

	max_diff = np.max(np.abs(sklearn_scores - onnx_scores))

	print(f"max score differenc: {max_diff:.2e}")

	if max_diff < 1e-4:
		print("PASS: ONNX model matches sklearn -- safe to benchmark")
	else:
		print("FAIL: scores diverge -- do NOT benchmark; conversion is wrong")

if __name__ == "__main__":
	main()

