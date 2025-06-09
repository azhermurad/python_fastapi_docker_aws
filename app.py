from fastapi import FastAPI, Path, HTTPException, Query
from typing import Annotated
import json
from customtypes.patientTypes import PatientSorted
from pydantic import AfterValidator


app = FastAPI()


def load_json(path="patients.json"):
    with open(path, mode="r") as file:
        file = json.load(file)
        return file


@app.get("/")
def root():
    return "api is working!!!"


@app.get("/patients")
def get_patients():
    return load_json("patients.json")



# path parameters

@app.get("/patient/{patient_id}")
async def get_patient(
    patient_id: str = Path(..., description="ID of the patient", example="P001"),
    skip: int | None = None,
    limit: int = 10,
):
    patients = load_json("patients.json")
    if patients.get(patient_id):
        return {"Data": patients.get(patient_id)}

    raise HTTPException(status_code=404, detail="Patient Not Founded!!!")


def check_valid_order(order: str):
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="order should be asc or desc")
    return order


# sort the patient
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



