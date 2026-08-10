from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from skl2onnx import convert_sklearn #converts scikit-leasrn models to ONNX (IsolationForest Converter)
from skl2onnx.common.data_types import FloatTensorType

FEAT_DIR = Path.home() / "anomaly-monitor" / "data" / "features"

def main():

    bundle = joblib.load(FEAT_DIR / "model.joblib")

    model = bundle["model"]
    features = bundle["features"]

    n_features = len(features)  


