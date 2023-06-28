from fastapi import HTTPException
from app.database import SessionLocal
from app.measurements.models import Measurement
from app.measurements.schemas import MeasurementCreate, MeasurementUpdate
from typing import List

class MeasurementService:
    def __init__(self):
        self.db = SessionLocal()

    async def create_measurement(self, patient_id: int, measurement_data: MeasurementCreate) -> Measurement:
        measurement = Measurement(
            owner_id=patient_id,
            health_measurement=measurement_data.health_measurement,
            value=measurement_data.value
        )
        self.db.add(measurement)
        self.db.commit()
        self.db.refresh(measurement)
        return measurement

    async def get_measurements(self, patient_id: int) -> List[Measurement]:
        measurements = self.db.query(Measurement).filter(Measurement.owner_id == patient_id).all()
        return measurements

    async def get_measurement(self, measurement_id: int) -> Measurement:
        measurement = self.db.query(Measurement).filter(Measurement.id == measurement_id).first()
        if not measurement:
            raise HTTPException(status_code=404, detail="Measurement not found")
        return measurement

    async def update_measurement(self, measurement_id: int, measurement_data: MeasurementUpdate) -> Measurement:
        measurement = await self.get_measurement(measurement_id=measurement_id)  # Corrigir a chamada com argumento nomeado
        for field, value in measurement_data.dict(exclude_unset=True).items():
            setattr(measurement, field, value)
        self.db.commit()
        self.db.refresh(measurement)
        return measurement



    async def delete_measurement(self, measurement_id: int) -> Measurement:
        measurement = self.get_measurement(measurement_id)
        self.db.delete(measurement)
        self.db.commit()
        return measurement

    async def get_patient_measurements(self, patient_id: int) -> List[Measurement]:
        measurements = self.db.query(Measurement).filter(Measurement.owner_id == patient_id).all()
        return measurements
