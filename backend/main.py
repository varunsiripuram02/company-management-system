from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import SessionLocal, engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class EmployeeCreate(BaseModel):
    name: str
    email: str
    skills: str


class ProjectCreate(BaseModel):
    name: str
    description: str
    skills_required: str
    team_size: int
    deadline: str


class ApplyRequest(BaseModel):
    employee_id: int
    project_id: int


class ApprovalRequest(BaseModel):
    application_id: int
    action: str


class WorkLogCreate(BaseModel):
    employee_id: int
    project_id: int
    date: str
    hours: int
    task: str

@app.get("/")
def home():
    return {"message": "Backend running "}

@app.post("/add_employee")
def add_employee(emp: EmployeeCreate):
    db = SessionLocal()

    existing = db.query(models.Employee).filter(models.Employee.email == emp.email).first()
    if existing:
        db.close()
        return {"error": "Email already exists "}

    new_emp = models.Employee(
        name=emp.name,
        email=emp.email,
        skills=emp.skills,
        status="probation",
        role="employee"
    )

    db.add(new_emp)
    db.commit()
    db.close()

    return {"message": "Employee added successfully "}

@app.post("/create_project")
def create_project(project: ProjectCreate):
    db = SessionLocal()

    existing = db.query(models.Project).filter(models.Project.name == project.name).first()
    if existing:
        db.close()
        return {"error": "Project already exists "}

    new_project = models.Project(
        name=project.name,
        description=project.description,
        skills_required=project.skills_required,
        team_size=project.team_size,
        deadline=project.deadline,
        status="open",
        techlead_id=1
    )

    db.add(new_project)
    db.commit()
    db.close()

    return {"message": "Project created successfully "}

@app.post("/apply")
def apply_to_project(req: ApplyRequest):
    db = SessionLocal()

    employee = db.query(models.Employee).filter(models.Employee.id == req.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    project = db.query(models.Project).filter(models.Project.id == req.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    percent, missing = models.skill_match(employee.skills, project.skills_required)

    application = models.Application(
        employee_id=req.employee_id,
        project_id=req.project_id,
        match_percentage=int(percent),
        status="pending"
    )

    db.add(application)
    db.commit()
    db.close()

    return {
        "message": "Applied successfully",
        "match_percentage": percent,
        "missing_skills": missing
    }

@app.post("/approve")
def approve_application(req: ApprovalRequest):
    db = SessionLocal()

    application = db.query(models.Application).filter(models.Application.id == req.application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    employee = db.query(models.Employee).filter(models.Employee.id == application.employee_id).first()

    if req.action.lower() == "accept":
        application.status = "accepted"
        employee.status = "assigned"

    elif req.action.lower() == "reject":
        application.status = "rejected"

    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    db.commit()
    db.close()

    return {"message": f"Application {req.action}ed successfully "}

@app.post("/add_worklog")
def add_worklog(log: WorkLogCreate):
    db = SessionLocal()

    employee = db.query(models.Employee).filter(models.Employee.id == log.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    project = db.query(models.Project).filter(models.Project.id == log.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    work = models.WorkLog(
        employee_id=log.employee_id,
        project_id=log.project_id,
        date=log.date,
        hours=log.hours,
        task=log.task
    )

    db.add(work)
    db.commit()
    db.close()

    return {"message": "Work log added successfully "}
@app.get("/employees")
def get_employees():
    db = SessionLocal()
    employees = db.query(models.Employee).all()
    db.close()
    return employees

@app.get("/projects")
def get_projects():
    db = SessionLocal()
    projects = db.query(models.Project).all()
    db.close()
    return projects

@app.get("/dashboard")
def dashboard():
    db = SessionLocal()

    total_emp = db.query(models.Employee).count()
    total_proj = db.query(models.Project).count()
    total_apps = db.query(models.Application).count()

    db.close()

    return {
        "total_employees": total_emp,
        "total_projects": total_proj,
        "total_applications": total_apps
    }
