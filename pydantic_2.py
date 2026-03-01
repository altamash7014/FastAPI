from pydantic import BaseModel, ValidationError, Field

class Patient(BaseModel):
    # doing typevalidation by defining dataype
    name: str
    age: int

def insert_patient(name,age):
    print(name)
    print(age)
    print("Inserted patient data successfully ")

patient_info = {"name": "Alice", "age": 30}

patient1 = Patient(**patient_info)

# now we will get a pydantic object 
def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted patient pydantic data successfully ")

insert_patient(patient1)    