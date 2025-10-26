# backend/app/domain/value_objects.py

from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime

# ----------------- VALUE OBJECTS -----------------

class Username(BaseModel):
    value: constr(strip_whitespace=True, min_length=3, max_length=50)

    @validator('value')
    def no_forbidden_chars(cls, v):
        if " " in v:
            raise ValueError("El nombre de usuario no puede contener espacios")
        return v

class Email(BaseModel):
    value: EmailStr

class Password(BaseModel):
    value: constr(min_length=8, max_length=128)

    @validator('value')
    def strong_password(cls, v):
        # Reglas de ejemplo: debe contener al menos un número y una letra
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe contener al menos un número")
        if not any(c.isalpha() for c in v):
            raise ValueError("La contraseña debe contener al menos una letra")
        return v

class RoleName(BaseModel):
    value: constr(strip_whitespace=True, min_length=3, max_length=50)

class IsActive(BaseModel):
    value: bool = True

class CreatedAt(BaseModel):
    value: datetime = datetime.utcnow()

class UpdatedAt(BaseModel):
    value: datetime = datetime.utcnow()

