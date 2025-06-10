from pydantic import BaseModel, ValidationError, EmailStr, AnyUrl, Field, AfterValidator
from typing import List, Optional, Annotated


class Patient(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=4,
            description="usefull in api documentation",
            title="name of the patient",
        ),
        AfterValidator(lambda v: v.upper()),  # uppercase the name of the patient
    ]
    url: AnyUrl
    email: EmailStr
    age: int
    weight: Annotated[float, Field(gt=0, lt=50, strict=True)]
    married: bool | None = False
    allergies: Annotated[list[str] | None, Field(default=None)]
    contact_details: dict[str, str | int]


# create patient fucntion
def create_patient(data: Patient):
    print(data.name)
    print(data.age)
    print(data)


try:
    patient_info = {
        "name": "abcs",
        "age": "34",
        "email": "aa@gmail.com",
        "url": "https://docs.pydantic",
        # "married":True,
        "weight": 3,
        # "allergies": [12],
        "contact_details": {"phone": 12},
    }
    patient1 = Patient(**patient_info)
    create_patient(patient1)
except ValidationError as e:
    print(e.errors())
