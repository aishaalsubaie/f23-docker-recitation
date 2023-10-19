from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Recitation hours dictionary
RECITATION_HOURS = {"a": "09:00~09:50", "b": "10:00~10:50", "c": "11:00~11:50", "d": "12:00~12:50"}
# Microservice link
MICROSERVICE_LINK = "https://whos-my-ta.fly.dev/section_id/"

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/section_info/{section_id}")
def get_section_info(section_id: str):

    if section_id is None:
        raise HTTPException(status_code=404, detail="Missing section id")

    section_id = section_id.lower()

    response = requests.get(MICROSERVICE_LINK + section_id)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Section not found")

    data = response.json()
    ta_name_list = data.get("ta_names", [])  # Get the TA names, or an empty list if not available

    if section_id in RECITATION_HOURS:
        # Construct the response JSON
        response_data = {
            "section": section_id,
            "start_time": RECITATION_HOURS[section_id].split("~")[0],  
            "end_time": RECITATION_HOURS[section_id].split("~")[1],    
            "ta": [f"{ta['fname']} {ta['lname']}" for ta in ta_name_list], 
            "recitation time": RECITATION_HOURS[section_id]
        }
        return response_data
    else:
        raise HTTPException(status_code=404, detail="Invalid section id")
