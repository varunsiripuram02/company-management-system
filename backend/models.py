from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    skills = Column(String)
    status = Column(String)
    role = Column(String)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    skills_required = Column(String)
    team_size = Column(Integer)
    deadline = Column(String)
    status = Column(String)
    techlead_id = Column(Integer)

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    match_percentage = Column(Integer)
    status = Column(String)

class WorkLog(Base):
    __tablename__ = "worklogs"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer)
    project_id = Column(Integer)
    date = Column(String)
    hours = Column(Integer)
    task = Column(String)

def skill_match(employee_skills, project_skills):
    emp = set([s.strip().lower() for s in employee_skills.split(",")])
    proj = set([s.strip().lower() for s in project_skills.split(",")])

    match = emp.intersection(proj)
    percentage = (len(match) / len(proj)) * 100 if len(proj) > 0 else 0

    missing = proj - emp

    return percentage, list(missing)
