from pathlib import Path
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

FEATURES = ["events_per_sec", "exec_ratio", "unique_comms", "max_files_per_proc",
            "max_chain_depth", "chain_homogeneity", "max_children_per_proc"]

CSV = Path.home() / "anomaly-monitor" / "data" / "features" / "windows.csv"

def main():
    #reads the csv file
    df = pd.read_csv(CSV)
    
    #Do this when you have different value types 100 vs 1.0
    #Empty Scalar Object that holds means and std_dev, used to standarize data
    scaler = StandardScaler()

    #fit calculates the mean and deviation for all 5 features
    #transform applies the formula value - mean / std_dev for each row giving each a scaled value
    #X is what we will feed our Isolation Forest
    X = scaler.fit_transform(df[FEATURES])

    baseline_mask = (df.label == "baseline").values
    model = IsolationForest(n_estimators=200, contamination="auto", random_state=42)
    
    #Numpy automatically filters out the true values.
    #fit reads the data and learns from it and stores it in my Isolation Forest Object
    model.fit(X[baseline_mask])

    #creates new column, scores everything higer = anomlous (-)
    df["anomaly-score"] = -model.score_samples(X)

    print("=== mean anomaly score by session (higher = more anomlous) === \n")

    #groupby label and session, grab the anomaly-score and prefromm find the mean and max
    summary = (df.groupby(["label", "session"])
    ["anomaly-score"].agg(["mean", "max"]).round(3)
                    .sort_values("mean", ascending=False))
                                        #highest to lowest instead of lowest to highest
    print(summary)

    by_sess = df.groupby(["label", "session"]) ["anomaly-score"].mean()
    worst_anomaly = by_sess["anomaly"].min()
    best_baseline = by_sess["baseline"].max()

    print(f"\n lowest anomaly session mean: {worst_anomaly:.3f}")
    print(f"\n highest baseline session mean: {best_baseline:.3f}")

    if worst_anomaly > best_baseline:
        print("SEPARATION ACHIEVED: every anomaly outscores every baseline")
    else:
        print("OVERLAP: at least one anomaly hides among the baselines")

def save_model():
    #libary for saving python objects to disk then loading them back
    #saves to disk, not memory
    import joblib
    df = pd.read_csv(CSV)

    scaler = StandardScaler()
    X = scaler.fit_transform(df[FEATURES])

    model = IsolationForest(n_estimators=200, contamination="auto", random_state=42)

    model.fit(X[(df.label == "baseline").values])

    out = CSV.parent / "model.joblib"
    #converts the live objects into bytes written to a file, load this with joblib.load()
    #saves all three things at once
    joblib.dump({"model": model, "scaler": scaler, "features": FEATURES}, out)

    print(f"saved -> {out}")


if __name__ == "__main__":
    main()
    save_model()