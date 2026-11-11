from pydantic import BaseModel, Field, EmailStr, ConfigDict

class CustomerCreate(BaseModel):
    name : str = Field(min_length=1, max_length=100)
    email : EmailStr = Field(min_length=5, max_length=100)

class CustomerUpdate(BaseModel):
    name : str | None = Field(default=None, min_length=1)
    email : str | None = Field(default=None, min_length=5)

class CustomerOut(BaseModel):
    id : int
    name : str
    email : EmailStr

    model_config = ConfigDict(from_attributes=True) # allows pudantic to read sqlachemy model attributes

