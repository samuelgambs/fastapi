import unittest
from app.main import app
# from m.models import Patient, Measurement
from app.patients.models import Patient
from app.measurements.models import Measurement
# from schemas import PatientCreate, MeasurementCreate
from app.patients.schemas import PatientCreate
from app.measurements.schemas import MeasurementCreate
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from database import SessionLocal
import csv

client = TestClient(app)


class TestPatient(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db = SessionLocal()

    def tearDown(self):
        # Limpar o banco de dados após cada teste
        self.db.rollback()
        self.db.close()

    def test_create_patient(self):
        # Limpar o banco de dados antes de cada teste
        self.db.query(Patient).delete()
        self.db.query(Measurement).delete()
        self.db.commit()

        patient = PatientCreate(
            first_name="John",
            last_name="Doe",
            age=42,
            condition="Healthy"
        )
        response = self.client.post("/api/v1/patient/", json=patient.dict())
        assert response.status_code == 200
        assert response.json()["first_name"] == "John"
        assert response.json()["last_name"] == "Doe"
        assert response.json()["age"] == 42
        assert response.json()["condition"] == "Healthy"
        assert response.json()["id"] == 1

    def test_read_patient(self):
        response = client.get("api/v1/patient/1")
        assert response.status_code == 200
        assert response.json()["first_name"] == "John"
        assert response.json()["last_name"] == "Doe"
        assert response.json()["age"] == 42
        assert response.json()["condition"] == "Healthy"
        assert response.json()["id"] == 1

    def test_read_patients(self):
        response = client.get("api/v1/patient/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["first_name"] == "John"
        assert response.json()[0]["last_name"] == "Doe"
        assert response.json()[0]["age"] == 42
        assert response.json()[0]["condition"] == "Healthy"
        assert response.json()[0]["id"] == 1

    def test_create_measurement(self):
        measurement = MeasurementCreate(
            health_measurement="Blood Pressure",
            value="120/80"
        )
        response = self.client.post("api/v1/patient/1/measurements/", json=measurement.dict())
        assert response.status_code == 200
        assert response.json()["health_measurement"] == "Blood Pressure"
        assert response.json()["value"] == "120/80"
        assert response.json()["owner_id"] == 1
        assert response.json()["id"] == 1

    def load_test_data(self):
        # Limpar o banco de dados antes de cada teste
        self.db.query(Patient).delete()
        self.db.query(Measurement).delete()
        self.db.commit()

        with open('data/patients.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                patient = PatientCreate(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    age=int(row['age']),
                    condition=row['condition']
                )
                response = self.client.post("api/v1/patient/", json=patient.dict())
                assert response.status_code == 200
