from fastapi import APIRouter, HTTPException
from typing import List

from app.patients import schemas, services
from app.measurements import schemas as measurement_schemas

router = APIRouter()


@router.post("/", response_model=schemas.Patient)
async def create_patient(patient: schemas.PatientCreate) -> schemas.Patient:
    created_patient = await services.PatientService().create_patient(patient)
    return created_patient


@router.get("/{patient_id}", response_model=schemas.Patient)
async def get_patient(patient_id: int) -> schemas.Patient:
    patient = await services.PatientService().get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.get("/", response_model=List[schemas.Patient])
async def get_all_patients() -> List[schemas.Patient]:
    patients = await services.PatientService().get_all_patients()
    return patients


@router.put("/{patient_id}", response_model=schemas.Patient)
async def update_patient(patient_id: int, patient: schemas.PatientUpdate) -> schemas.Patient:
    updated_patient = await services.PatientService().update_patient(patient_id, patient)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient


@router.delete("/{patient_id}")
async def delete_patient(patient_id: int):
    deleted_patient = await services.PatientService().delete_patient(patient_id)
    if not deleted_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}

@router.post("/{patient_id}/measurements", response_model=measurement_schemas.Measurement)
async def create_patient_measurement(patient_id: int, measurement: measurement_schemas.MeasurementCreate) -> measurement_schemas.Measurement:
    created_measurement = await services.PatientService().create_patient_measurement(patient_id, measurement)
    return created_measurement
