from pydantic import BaseModel


class MeasurementBase(BaseModel):
    health_measurement: str
    value: str | None = None


class MeasurementCreate(MeasurementBase):
    pass


class Measurement(MeasurementBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class MeasurementUpdate(MeasurementBase):
    pass
