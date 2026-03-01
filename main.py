from fastapi import FastAPI,Path, HTTPException, Query
import json 
from pydantic import BaseModel,Field, computed_field
from typing import Annotated, Literal, Optional
from fastapi.responses import JSONResponse

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

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient in DB",example = 'P001')):
# def get_patient(patient_id: str):
    #load all data and return the patient with the given id
    data = load_data()
    if patient_id in data:
        return {"patient": data[patient_id]}
    raise HTTPException(status_code=404, detail="Patient not found")

class Patient(BaseModel):
    id: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    city: Annotated[str, Field(...)]
    age: Annotated[int, Field(..., gt=0, lt=100)]
    gender: Annotated[Literal["male", "female", "other"], Field(...)]
    height: Annotated[float, Field(...)]
    weight: Annotated[float, Field(..., gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


# CREATED PYDANTIC MODEL
    #NOW WE  WILL CRETAE ENDPOINTS TO PERFORM CRUD OPERATIONS ON THIS MODEL
    #   

@app.post('/create')
def create_patient(patient: Patient):
    # load existing data
    data = load_data()
   
    # checking if patient with same id already exists   
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
  
    # add new patient to data
    data[patient.id] = patient.model_dump(exclude = ['id'])#converting pydantic data to dictionary and excluding id field as it will be used as key in json 
    
    # save updated data back to file
    save_data(data)

    # return JSONResponse(status_code = 201, content={"message": "Patient created successfully"})

# from here we will work on update
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(...)]
    city: Annotated[Optional[str], Field(...)]
    age: Annotated[Optional[int], Field(..., gt=0, lt=100)]
    gender: Annotated[Optional[Literal["male", "female", "other"]], Field(...)]
    height: Annotated[Optional[float], Field(...)]
    weight: Annotated[Optional[float], Field(..., gt=0)]

# enddpoint building for update
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found.")
    # if exist in data
    existing_patient = data[patient_id] #well get the existing patient data and update it with the new data provided in request body
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    # model dump is to convert in dictionary and exclude unset is to exclude the fields which are not provided in request body
#    excluded those fields which client has not sent me

# extracting key value pair from updated patient info and updating existing patient data
# we r running loop in updated one but running in existing one
    for key, value in updated_patient_info.items():
        existing_patient[key] = value

# since if we change weight or height,we also have to chnage verdict & bmi     # 
    # existing_patient -> pydantic object -> updated bmi + verdict
    # -> pydantic object -> dictionary 
    patient_pydantic_ = Patient(id=patient_id, **existing_patient) #creating pydantic object of patient using existing patient data and id
    existing_patient = patient_pydantic_.model_dump(exclude = ['id']) #converting pydantic object to dictionary and excluding id field as it will be used as key in json
    
    # add updated patient data back to main data and save it
    data[patient_id] = existing_patient
    save_data(data)

    return JSONResponse(status_code = 201, content={"message": "Patient updated successfully", "patient": existing_patient})
