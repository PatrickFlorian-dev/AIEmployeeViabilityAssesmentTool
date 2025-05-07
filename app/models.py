from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey, Float
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(DateTime)
    role = Column(String)
    years_experience = Column(Integer)
    number_previous_employers = Column(Integer)
    different_industries_worked_in = Column(Integer)
    has_changed_job_role_past_5_years = Column(Boolean)
    has_leadership_experience = Column(Boolean)
    largest_company_size_worked_at = Column(Integer)
    has_entrepreneur_experience = Column(Boolean)
    military_experience = Column(Boolean)
    volunteer_experience = Column(Boolean)
    previous_internship_experience = Column(Boolean)
    years_with_current_company = Column(Integer)
    tenure_previous_jobs = Column(Integer)
    active_employee = Column(Boolean)

class ModelRun(Base):
    __tablename__ = 'model_runs'
    id = Column(Integer, primary_key=True)
    run_date = Column(DateTime, default=datetime.utcnow)
    model_type = Column(String)
    hyperparameters = Column(JSON)  # {epochs: 50, layers: [64,32]}
    metrics = Column(JSON)          # {"mae": 1.2, "accuracy": 0.85}
    errors = Column(JSON)
    is_overfitted = Column(Boolean)

class ModelEvaluation(Base):
    __tablename__ = 'model_evaluations'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    model_run_id = Column(Integer, ForeignKey('model_runs.id'))
    success_score = Column(Integer)
    confidence = Column(Float)

