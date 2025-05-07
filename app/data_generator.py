from faker import Faker
import os
import random
from datetime import datetime, timedelta
from app.database import Session
from app.models import Employee 

fake = Faker()

def calculate_success_score(employee):

    retention_weight = 0.4
    promotion_weight = 0.3
    performance_weight = 0.3
    
    retention_norm = min(employee.years_with_current_company / 50, 1.0)
    
    promotions = random.randint(0, int(employee.years_with_current_company/5))
    promotion_norm = promotions / 5
    
    performance = random.triangular(3, 5, 4.5)
    performance_norm = (performance - 1) / 4
    
    composite = (
        (retention_norm * retention_weight) +
        (promotion_norm * promotion_weight) +
        (performance_norm * performance_weight)
    )
    return round(composite * 9 + 1)  # Scale to 1-10

def generate_employees(num=5000):
    session = Session()
    
    for _ in range(num):
        emp = Employee(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            dob=fake.date_of_birth(minimum_age=18, maximum_age=65),
            role=fake.job(),
            years_experience=random.randint(0, 40),
            number_previous_employers=random.randint(0, 10),
            different_industries_worked_in=random.randint(1, 5),
            has_changed_job_role_past_5_years=random.choice([True, False]),
            has_leadership_experience=random.choice([True, False]),
            largest_company_size_worked_at=random.choice([10, 50, 200, 1000, 5000, 10000]),
            has_entrepreneur_experience=random.choice([True, False]),
            military_experience=random.choice([True, False]),
            volunteer_experience=random.choice([True, False]),
            previous_internship_experience=random.choice([True, False]),
            years_with_current_company=random.randint(0, 20),
            tenure_previous_jobs=random.randint(0, 40),
            active_employee=random.choice([True, False])
        )
        emp.tenure_previous_jobs = emp.years_experience - random.randint(0, emp.years_experience)
        emp.success_score = calculate_success_score(emp)
        session.add(emp)
    
    session.commit()

def reset_database():
    from sqlalchemy import create_engine
    from app.models import Base  # Ensure this import
    
    engine = create_engine(os.getenv('DATABASE_URL'))
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)