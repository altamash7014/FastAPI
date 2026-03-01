from pydantic import BaseModel, ValidationError, Field
from typing import Optional,List, Dict

class Patient(BaseModel):
    # doing typevalidation by defining dataype
    name: str
    age: int
    weight : float
    married: bool = False # we can also define default values for the fields
    allergies: Optional[list[str]] = None # we can also define optional fields which can be None
    contact_details: dict[str, str] # we can also define list of specific datatypes like list of strings or list of integers
    

def insert_patient(name,age):
    print(name)
    print(age)
   

    print("Inserted patient data successfully ")
    # canging here will be reflected in every fxn where we are using this data as we are using the same variable name and value 

patient_info = {"name": "Alice", "age": 30, "married": True, "weight": 65.5, "allergies": ["pollen", "dust"], "contact_details": {"email": "alice@example.com"}}

patient1 = Patient(**patient_info)

# now we will get a pydantic object 
def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print("Inserted patient pydantic data successfully ")

# now we can create multiple patient objects with different data and insert them without worrying about type validation and data validation as pydantic will take care of it.
def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.weight)
    print(patient.allergies)
    print(patient.contact_details)
    print("Updated patient pydantic data successfully ")

insert_patient(patient1)  
update_patient(patient1)  