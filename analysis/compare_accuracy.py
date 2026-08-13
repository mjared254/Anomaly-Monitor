from pathlib import Path
import joblib
import numpy as np
import pandas as pd

#compares the accuracy between my original model and compressed variant
#used spearmanr to take the anomaly score generated from Isolation Forest (from scaled values)
#speamanr compares how both models rank sessions, returning a correlationn coefficent from -1 to 1

FEAT_DIR = Path.home() / "anomaly-monitor" / "data" / "features"

# we take in a bundle_name -> model
def scores_for(bundle_name, df):
	#unloading the bundle in more compact form
	b = joblib.load(FEAT_DIR / bundle_name)
	
	X = b["scaler"].transform(df[b["features"]]).astype(np.float32)
	
	return -b["model"].score_samples(X)


def main():
	df = pd.read_csv(FEAT_DIR / "windows.csv")
	#creates df for each model, calls the functio scores_for to unload , scale and score.
	df["full"] = scores_for("model.joblib", df) 
	df["small"] = scores_for("model_small.joblib",df)
		#bucket rows by label and sessions, only keep full and small columns
		#finds the mean from each bucket, adding each rows scaler and dividing by the # of values
	summary = (df.groupby(["label", "session"])[["full", "small"]]
                 .mean().round(3).sort_values("full", ascending=False))
	print(summary)

	
	from scipy.stats import spearmanr

	rho = spearmanr(df["full"], df["small"]).correlation

	print(f"\n rannking correlation (full vs small): {rho:.3f}")

	print("1.00 = compression preserved ordering; <0.9 = meaningful drift")

if __name__ == "__main__":
	main()
