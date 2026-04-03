import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Company System", layout="wide")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.success("Login successful ")
            st.rerun()
        else:
            st.error("Invalid credentials !")

    st.stop()
st.title("Company Management System")
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Employees",
        "Projects",
        "Apply",
        "Approve",
        "Work Log"
    ]
)

if menu == "Dashboard":
    st.header("Dashboard")
    res = requests.get(f"{BASE_URL}/dashboard").json()
    col1, col2, col3 = st.columns(3)
    col1.metric("Employees", res["total_employees"])
    col2.metric("Projects", res["total_projects"])
    col3.metric("Applications", res["total_applications"])
elif menu == "Employees":
    st.header("Employees")
    name = st.text_input("Name")
    email = st.text_input("Email")
    skills = st.text_input("Skills")

    if st.button("Add Employee"):
        res = requests.post(f"{BASE_URL}/add_employee", json={
            "name": name,
            "email": email,
            "skills": skills
        })
        st.write(res.json())
    data = requests.get(f"{BASE_URL}/employees").json()
    df = pd.DataFrame(data)
    st.dataframe(df)

elif menu == "Projects":
    st.header("Projects")
    name = st.text_input("Project Name")
    desc = st.text_area("Description")
    skills = st.text_input("Skills")
    team = st.number_input("Team Size", min_value=1)
    deadline = st.text_input("Deadline")

    if st.button("Create Project"):
        res = requests.post(f"{BASE_URL}/create_project", json={
            "name": name,
            "description": desc,
            "skills_required": skills,
            "team_size": team,
            "deadline": deadline
        })
        st.write(res.json())

    data = requests.get(f"{BASE_URL}/projects").json()
    df = pd.DataFrame(data)
    st.dataframe(df)
    
elif menu == "Apply":
    st.header("Apply to Project")
    employees = requests.get(f"{BASE_URL}/employees").json()
    projects = requests.get(f"{BASE_URL}/projects").json()
    emp_dict = {f"{e['name']} (ID {e['id']})": e["id"] for e in employees}
    proj_dict = {f"{p['name']} (ID {p['id']})": p["id"] for p in projects}
    emp_choice = st.selectbox("Select Employee", list(emp_dict.keys()))
    proj_choice = st.selectbox("Select Project", list(proj_dict.keys()))

    if st.button("Apply"):
        res = requests.post(f"{BASE_URL}/apply", json={
            "employee_id": emp_dict[emp_choice],
            "project_id": proj_dict[proj_choice]
        })
        st.write(res.json())
        
elif menu == "Approve":
    st.header("Approve Applications")
    app_id = st.number_input("Application ID", min_value=1)
    action = st.selectbox("Action", ["accept", "reject"])
    if st.button("Submit"):
        res = requests.post(f"{BASE_URL}/approve", json={
            "application_id": app_id,
            "action": action
        })
        st.write(res.json())
        
elif menu == "Work Log":
    st.header("Work Log")
    employees = requests.get(f"{BASE_URL}/employees").json()
    projects = requests.get(f"{BASE_URL}/projects").json()
    emp_dict = {f"{e['name']} (ID {e['id']})": e["id"] for e in employees}
    proj_dict = {f"{p['name']} (ID {p['id']})": p["id"] for p in projects}
    emp_choice = st.selectbox("Employee", list(emp_dict.keys()))
    proj_choice = st.selectbox("Project", list(proj_dict.keys()))
    date = st.text_input("Date")
    hours = st.number_input("Hours", min_value=1)
    task = st.text_area("Task")
    if st.button("Submit Work"):
        res = requests.post(f"{BASE_URL}/add_worklog", json={
            "employee_id": emp_dict[emp_choice],
            "project_id": proj_dict[proj_choice],
            "date": date,
            "hours": hours,
            "task": task
        })
        st.write(res.json())
