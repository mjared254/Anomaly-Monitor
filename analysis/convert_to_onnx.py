from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from skl2onnx import convert_sklearn #converts scikit-leasrn models to ONNX (IsolationForest Converter)
from skl2onnx.common.data_types import FloatTensorType

FEAT_DIR = Path.home() / "anomaly-monitor" / "data" / "features"

def main():
    #unpacking the bundle, bundle includes model, scaler and features
    bundle = joblib.load(FEAT_DIR / "model.joblib")

    model = bundle["model"]
    features = bundle["features"]

    n_features = len(features)
    #ONNX needs to know the SHAPE of the input
    # Model expects 32-bit floats, 		any numbers of rows, maximum number of rows

    #FP32 Onnx stores 32-bit floats, offers maximum baseline precison
    initial_type = [("float_input", FloatTensorType([None, n_features]))]

    onnx_model = convert_sklearn(
        model,
        initial_types = initial_type,
        target_opset = {"":18, "ai.onnx.ml": 3},
        options = {id(model): {"score_samples": True}},
    )
     
    out = FEAT_DIR / "model_fp32.onnx"
    with open(out, "wb") as f:
        f.write(onnx_model.SerializeToString())
    print(f"wrote -> {out} ({out.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()


