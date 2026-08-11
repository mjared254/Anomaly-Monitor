from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType


FEAT_DIR = Path.home() / "anomaly-monitor" / "data" / "features"

FEATURES = ["events_per_sec", "exec_ratio", "unique_comms", "max_files_per_proc",
            "max_chain_depth", "chain_homogeneity", "max_children_per_proc"]

def main():
	#Load the 454 windows, scale data, save as 32-bit
	df = pd.read_csv(FEAT_DIR / "windows.csv")

	scaler = StandardScaler()
	
	X = scaler.fit_transform(df[FEATURES]).astype(np.float32)
	#Create the Iso Forest Model
	small = IsolationForest(n_estimators=40, max_samples=128, contamination="auto",
		random_state=42)
	#feed only baseline to ISO Forest, selects only true values where label == "baseline"
	small.fit(X[(df.label == "baseline").values])
	#save the sklearn bundle for later, (deletes after function ends, this saves on disk)

	joblib.dump({"model": small, "scaler" : scaler, "features" : FEATURES}, FEAT_DIR / "model_small.joblib")

	initial_type = [("float_input", FloatTensorType([None, len(FEATURES)]))]

	onnx_model = convert_sklearn(
	small,
	initial_types = initial_type,
	target_opset = {"": 18, "ai.onnx.ml" : 3},
	options = {id(small): {"score_samples" : True}},
	)

	out = FEAT_DIR / "model_small.onnx"
	
	with open(out, "wb") as f:
		f.write(onnx_model.SerializeToString())
	print(f"wrote -> {out} ({out.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
	main()
