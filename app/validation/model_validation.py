from models import Session

def validate_employee(emp_id):
    session = Session()
    emp = session.query(Employee).get(emp_id)
    if not emp:
        return {"error": "Employee not found"}
    if emp.success_score < 1 or emp.success_score > 10:
        return {"error": "Invalid success score"}
    return None