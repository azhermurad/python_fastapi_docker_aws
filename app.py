from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated, Literal
from pydantic import AfterValidator, BaseModel, Field
import pandas as pd
import pickle

app = FastAPI()


class Predict(BaseModel):
    DailyTimeSpentonSite: Annotated[
        float, Field(description="Time spend on site in minitue", examples=[68.95])
    ]
    Age: Annotated[int, Field(description="Age of the user", examples=[35])]
    AreaIncome: Annotated[
        float,
        Field(
            description="Avg. Income of geographical area of consumer",
            examples=[61833.90],
        ),
    ]
    DailyInternetUsage: Annotated[
        float,
        Field(
            description=" Usage': Avg. minutes a day consumer is on the internet",
            examples=[256.09],
        ),
    ]
    Gender: Annotated[Literal["male", "female"], Field(description="Gender")]


@app.post("/predict")
def predict(data: Predict):
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
    print(df.head())

    # load model using picke
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
        clicked_on_ad = model.predict(df)[0]
        res = "Clicked" if clicked_on_ad else "Not Clicked"
        print(clicked_on_ad)
    return JSONResponse(status_code=200, content={"data": f"{res}"})
