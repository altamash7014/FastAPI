from fastapi import FastAPI,Path, HTTPException, Query
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
    raise HTTPException(status_code=404, detail="Patient not found")


# applying query parameters
@app.get('/sort')
def sort_patients(sort_by: str = Query(...,description = 'Sort on the basis of height,weight or bmi'),order : str = Query('asc',description = 'Sort in ascending or descending order (asc/desc)')):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Bad request. Invalid sort field. Valid fields are: {valid_fields}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Bad request. Invalid sort order. Valid orders are: 'asc' or 'desc'")
    
    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)
    return {"sorted_patients": sorted_data}

