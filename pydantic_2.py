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

# now we can create multiple patient objects with different data and insert them without worrying about type validation and data validation as pydantic will take care of it.
def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Updated patient pydantic data successfully ")

insert_patient(patient1)  
update_patient(patient1)  