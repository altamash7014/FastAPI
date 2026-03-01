from fastapi import FastAPI,Path
import json 

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def home():
    return {"message": "Patient Management Sysytem API"}

@app.get('/about')
def about():
    return {"message": "A fully functional patient management system API built with FastAPI."}    

@app.get("/view")
def view_patients():
    data = load_data()
    return {"patients": data}

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient in DB",example = 'P001')):

# def get_patient(patient_id: str):
    #load all data and return the patient with the given id
    data = load_data()
    if patient_id in data:
        return {"patient": data[patient_id]}
    else: 
        return {"error": "Patient not found"}