from pydantic import (
    BaseModel,
    ValidationError,
    Field,
    model_validator
)
from typing import List, Optional, Annotated


class User(BaseModel):
    name: str = Field(max_length=24)
    password: str
    password_repeat: str
    
    
    # the model validator is validation on the model
    @model_validator(mode="after")
    def check_password_match(model):
        print("sssssss",model.name)
        if model.password != model.password_repeat:
            raise ValueError("password and password_repeat should be match!!")
        return model
        
    
    
def create_user(user:User):
    print(user.name)
    print(user.password)
    print(user.password_repeat)
    

try:
    data = {
        "name":"Azher ali",
        "password":"124",
        "password_repeat":"1234"
    }
    user = User(**data)
    create_user(user)
except ValidationError as e:
    print(e.errors())