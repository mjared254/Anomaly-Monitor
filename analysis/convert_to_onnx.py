from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from skl2onnx import convert_sklearn #converts scikit-leasrn models to ONNX (IsolationForest Converter)
from skl2onnx.common.data_types import FloatTensorType

FEAT_DIR = Path.home() / "anomaly-monitor" / "data" / "features"


#Converts my Isolation Forest to ONNX (static graph) in bytes to enable phone's runtime to execute

def main():
    #unpacking the bundle, bundle includes model, scaler and features
    bundle = joblib.load(FEAT_DIR / "model.joblib")

    model = bundle["model"]
    features = bundle["features"]

    n_features = len(features)
    #ONNX needs to know the SHAPE of the input
    # Model expects 32-bit floats, 		any numbers of rows, maximum number of rows

    #FloatTensorType dictates the format of the data going in, not storing anything yet
    #Our input is called "float_input" and its a float tensor of shape (any rows, 7 columns, as 32-bit floats)
    initial_type = [("float_input", FloatTensorType([None, n_features]))]


    #Converts my model to ONNX (static graph)
    onnx_model = convert_sklearn(
        model,
        initial_types = initial_type,  #-> ONNX is a static graph, it cannot figure out the input shape on its own
        target_opset = {"":18, "ai.onnx.ml": 3},
        options = {id(model): {"score_samples": True}},
    )

    #Writes ONNX static graph to disk
    out = FEAT_DIR / "model_fp32.onnx"
    with open(out, "wb") as f:
        #saves bytes on disk to be accessed later
        f.write(onnx_model.SerializeToString()) #-> turns the in-memory graph in to bytes
    print(f"wrote -> {out} ({out.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()


