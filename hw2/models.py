import json

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not all(char.isalpha() for char in value.split()):
            raise ValueError("Имя должно состоять только из букв.")
        return value

    @model_validator(mode="after")
    def validate_age(self) -> "User":
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError(
                "Возраст занятого пользователя должен быть от 18 до 65"
            )
        return self
