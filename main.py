from fastapi import FastAPI, Path, HTTPException, Query
import json 

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/patients")
def get_patients():
    data = load_data()
    return data

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient is required", example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort by 'name' or 'age'"), order: str = Query("asc", description="Order of sorting: 'asc' or 'desc'")):

    sort_variables = ["height", "weight", "bmi"]

    if sort_by not in sort_variables:
        raise HTTPException(status_code=400, detail=f"Invalid sort variable. Choose from {sort_variables}.")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Choose 'asc' or 'desc'.")
    
    data = load_data()
    sort_order = True if order == "desc" else False
    patients = list(data.values())
    patients.sort(key=lambda x: x[sort_by], reverse= sort_order)
    return patients 