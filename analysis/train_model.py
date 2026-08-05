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
    #turns raw value into a scalar. to mesure devation
    scalar = StandardScaler()

    #calculates the mean and deviation for all 5 features
    #X is what we will feed our Isolation Forest
    X = scaler.fit_transform(df[FEATURES])

    baseline_mask = (df.label == "baseline").values
