from pydantic import (
    BaseModel,
    ValidationError,
    Field,
    computed_field
)
from typing import List, Optional, Annotated

# nested model in the pydantic 
class Address(BaseModel):
    country: str
    city: str
    pin: int


class User(BaseModel):
    name: str = Field(max_length=24)
    password: str
    password_repeat: str
    address: Address
    
    
    
    @computed_field
    @property
    def full_name(self)->str:
        return self.name + " added"
    
  
    
    
def create_user(user:User):
    print(user.name)
    print(user.password)
    print(user.password_repeat)
    print(user.address.city)
    

try:
    
    address = Address(**{"country":"pakistan","city":"islamabad","pin":19182})
    data = {
        "name":"Azher ali",
        "password":"1234",
        "password_repeat":"1234",
        "address": address
    }
    user = User(**data)
    create_user(user)
    
    print(user.model_dump(),"model dump to create user")
except ValidationError as e:
    print(e.errors())