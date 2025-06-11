from pydantic import (
    BaseModel,
    ValidationError,
    EmailStr,
    AnyUrl,
    Field,
    AfterValidator,
    field_validator,
)
from typing import List, Optional, Annotated


class Patient(BaseModel):
    name: str
    url: AnyUrl
    email: EmailStr
    age: int
    weight: float
    married: bool | None = False
    allergies: Annotated[list[str] | None, Field(default=None)]
    contact_details: dict[str, str | int]

    @field_validator("name")
    @classmethod
    def uppercase(cls, value):
        return value.upper()

    # field validator are used for the validation of the field
    @field_validator("email")
    @classmethod
    def is_even(cls, value: str) -> str:
        valid = ["hdfc.com", "icici.com"]
        email = value.split("@")[-1]
        if email not in valid:
            raise ValueError(f"{value} is not a valid email")
        return value


# create patient fucntion
def create_patient(data: Patient):
    print(data.name)
    print(data.age)
    print(data)


try:
    patient_info = {
        "name": "abcs",
        "age": "34",
        "email": "aa@icici.com",
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
