from typing import Annotated, Literal
from pydantic import BaseModel, Field


class PredictUser(BaseModel):
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
