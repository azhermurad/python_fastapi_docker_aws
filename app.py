from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Annotated, Literal
import json
from customtypes.patientTypes import PatientSorted
from pydantic import AfterValidator, BaseModel, computed_field, Field


app = FastAPI()


def load_json(path="patients.json"):
    with open(path, mode="r") as file:
        file = json.load(file)
        return file


# ROOT API
@app.get("/")
def root():
    return "api is working!!!"


# GET ALL PATIENTS
@app.get("/patients")
def get_patients():
    return load_json("patients.json")


# GET PATIENT BY IT ID


@app.get("/patient/{patient_id}")
async def get_patient(
    patient_id: str = Path(..., description="ID of the patient", example="P001"),
):
    patients = load_json("patients.json")
    if patients.get(patient_id):
        return {"Data": patients.get(patient_id)}

    raise HTTPException(status_code=404, detail="Patient Not Founded!!!")


def check_valid_order(order: str):
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="order should be asc or desc")
    return order


# SORT PATIENTS
@app.get("/sort")
def sort_patient(
    sort_by: Annotated[
        PatientSorted | None,
        Query(description="sorted_by weight, heigth, bmi"),
    ] = None,
    order: Annotated[
        str,
        Query(description="sort in asc or desc order"),
        AfterValidator(check_valid_order),
    ] = "asc",
):
    data = load_json()
    if sort_by is None:
        return {"data": data}

    # this function is used for sort the patient by weight, height and bmi values
    is_reverse = True if order == "desc" else False
    data = dict(
        sorted(
            ((k, v) for k, v in data.items()),
            key=lambda x: x[1][sort_by],
            reverse=is_reverse,
        )
    )

    return {"data": data}


# POST METHOD: CREATE A PATIENT

#   "name": "Neha Sinha",
#         "city": "Kolkata",
#         "age": 30,
#         "gender": "female",
#         "height": 1.55,
#         "weight": 75,
#         "bmi": 31.22,
#         "verdict": "Obese"


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="name of the patent")]
    city: Annotated[str, Field(..., description="City name")]
    age: Annotated[int, Field(..., gt=0, lt=100, description="name of the patent")]
    gender: Annotated[
        Literal["male", "female", "other"],
        Field(description="gender should be male, female or other"),
    ]
    height: Annotated[float, Field(..., description="height of the patient", gt=0)]
    weight: Annotated[float, Field(..., description="weight of the patent", gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / self.height**2, 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif self.bmi < 30:
            return "normal"
        else:
            return "obese"


@app.post("/patient/")
def create_patient(patient: Patient):
    data = load_json()
    if not patient.id in data:
        filtered_data = patient.model_dump(exclude=["id"])
        data[patient.id] = filtered_data
        with open("patients.json", mode="w") as file:
            json.dump(data, file)
        return JSONResponse(status_code=201,content=load_json())
    else:
        raise HTTPException(status_code=400, detail="patient is already exist!!!")
    
