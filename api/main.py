import numpy as np
import pandas as pd

from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel, validator
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .ml.model import Model, get_model, n_features


class PredictRequest(BaseModel):
    data: List[List[float]]

    @validator("data")
    @classmethod
    def check_dimensionality(cls, data_points):
        for point in data_points:
            if len(point) != n_features:
                raise ValueError(f"Each data point must contain {n_features} features")

        return data_points


class PredictResponse(BaseModel):
    data: List[float]

class StatusResponse(BaseModel):
    status: str

app = FastAPI()


@app.post("/predict", response_model=PredictResponse)
def predict(model_input: PredictRequest, model: Model = Depends(get_model)):
    X = np.array(model_input.data)
    y_pred = model.predict(X)
    result = PredictResponse(data=y_pred.tolist())

    return result

@app.get("/api/status")
def predict():
    return StatusResponse(status='ok!')


@app.post("/predict_csv")
def predict_csv(csv_file: UploadFile = File(...), model: Model = Depends(get_model)):
    try:
        df = pd.read_csv(csv_file.file).astype(float)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Unable to process file"
        ) from e

    _, df_n_features = df.shape
    if df_n_features != n_features:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Each data point must contain {n_features} features",
        )

    y_pred = model.predict(df.to_numpy().reshape(-1, n_features))
    result = PredictResponse(data=y_pred.tolist())

    return result
