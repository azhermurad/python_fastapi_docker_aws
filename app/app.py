from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import pandas as pd
from schema.predict_user import PredictUser
from model.predict import load_model

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"data": "Internet User Clicked On An Advertisement Tracker API"}


@app.post("/predict")
def predict(data: PredictUser):
    df = pd.DataFrame(
        [
            {
                "Daily Time Spent on Site": data.DailyTimeSpentonSite,
                "Age": data.Age,
                "Area Income": data.AreaIncome,
                "Daily Internet Usage": data.DailyInternetUsage,
                "Male": 1 if data.Gender == "male" else 0,
            }
        ]
    )
    res = load_model(df)

    return JSONResponse(status_code=200, content={"data": f"{res}"})
