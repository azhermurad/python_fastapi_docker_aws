from pydantic import BaseModel, ValidationError, EmailStr, AnyUrl
from typing import List,Optional


class Patient(BaseModel):
    name: str
    url: AnyUrl  
    email: EmailStr
    age: int
    weight: float
    married: bool | None = False
    allergies: Optional[list[str] | None ] = None
    contact_details: dict[str, str | int]


# create patient fucntion
def create_patient(data: Patient):
    print(data.name)
    print(data.age)
    print(data)


try:
    patient_info = {
        "name": "abc",
        "age": "34",
        "email":"aa@gmail.com",
        "url": "https://docs.pydantic",
        # "married":True,
        "weight": 40.2,
        # "allergies": [12],
        "contact_details": {"phone": 12},
    }
    patient1 = Patient(**patient_info)
    create_patient(patient1)
except ValidationError as e:
    print(e.errors())
