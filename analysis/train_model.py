import pathlib as Path
import pandas as pd
import sklearn.ensemble import IsolationForest
import sklearn.preprocessing import StandardScaler

FEATURES = ["events_per_sec", "exec_ratio", "unique_comms", "max_files_per_proc",
            "max_chain_depth"]

CSV = Path.home() / "anomaly-monitor" / "data" / "features" / "windows.csv"

def main():
    #reads the csv file
    df = pd.read_csv(CSV)
    
    #Do this when you have different value types 100 vs 1.0
    #Empty Scalar Object
    scaler = StandardScaler()

    #fit calculates the mean and deviation for all 5 features
    #transform applies the formula value - mean / std_dev for each row giving each a scaled value
    #X is what we will feed our Isolation Forest
    X = scaler.fit_transform(df[FEATURES])

    baseline_mask = (df.label == "baseline").values
    model = IsolationForest(n_estimators=200, contamination="auto", random_state=42)
    
    #Numpy automatically filters out the true values.
    #fit reads the data and learns from and stores it in my Isolation Forest Object
    model.fit(X[baseline_mask])
