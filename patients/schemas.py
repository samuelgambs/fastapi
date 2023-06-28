from pydantic import BaseModel

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    condition: str
    


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: int

    measurements: list = []

    class Config:
        orm_mode = True


class PatientUpdate(PatientBase):
    pass
