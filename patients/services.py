from http.client import HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal

from app.patients.models import Patient
from app.patients.schemas import PatientCreate, PatientUpdate
from typing import List
from app.measurements.schemas import MeasurementCreate, MeasurementBase
from app.measurements.models import Measurement


class PatientService:
    def __init__(self):
        self.db = SessionLocal()

    async def create_patient(self, patient_data: PatientCreate) -> Patient:
        patient = Patient(first_name=patient_data.first_name, last_name=patient_data.last_name,
                          age=patient_data.age, condition=patient_data.condition)
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    async def get_patient(self, patient_id: int) -> Patient:
        patient = self.db.query(Patient).filter(
            Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient

    async def get_all_patients(self) -> List[Patient]:
        patients = self.db.query(Patient).all()
        return patients

    async def update_patient(self, patient_id: int, patient_data: PatientUpdate) -> Patient:
        patient = await self.get_patient(patient_id)
        for field, value in patient_data.dict(exclude_unset=True).items():
            setattr(patient, field, value)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    async def delete_patient(self, patient_id: int) -> Patient:
        patient = await self.get_patient(patient_id)
        self.db.delete(patient)
        self.db.commit()
        return patient

    async def get_patient_measurements(self, patient_id: int) -> List[Patient]:
        measurements = self.db.query(Patient).filter(
            Patient.owner_id == patient_id).all()
        return measurements

    async def create_patient_measurement(self, patient_id: int, measurement_data: MeasurementCreate) -> Measurement:
        measurement = Measurement(
            owner_id=patient_id,
            health_measurement=measurement_data.health_measurement,
            value=measurement_data.value
        )
        self.db.add(measurement)
        self.db.commit()
        self.db.refresh(measurement)
        return measurement