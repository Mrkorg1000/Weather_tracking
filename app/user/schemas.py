from pydantic import BaseModel, EmailStr


class SchemaUserRegister(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class SchemaUserLogin(SchemaUserRegister):
    pass