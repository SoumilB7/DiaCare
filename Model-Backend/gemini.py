import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


def parse_data(textual_data):
    format = """
    {
    "Pregnancies" : int 
    "Glucose" : int
    "BloodPressure" : int
    "SkinThickness" : int 
    "Insulin" : int
    "BMI" : int
    "DiabetesPedigreeFunction" : int
    "Age" : int
    }
    """
    prompt = f"Parse the following values from this trascript of the form : {textual_data}. The file should be in the format {format}. DO NOT PRINT ANYTHING ELSE not even the json code block string:"
    response = model.generate_content(prompt)
    jsonobj = response.text
    jsonobj = jsonobj.removeprefix("```json\n")
    jsonobj = jsonobj.removesuffix("```\n")
    final_dict = json.loads(jsonobj)
    return final_dict

def fallback_diagnosis(textual_data):
    fallback_format = {
        "Diabetes-type" : "(No Diabetes or Type 1 Diabetes or Type 2 Diabetes)",
    }
    prompt = f"Parse the following values from this trascript of the form : {textual_data}. The file should be in the format {fallback_format}. DO NOT PRINT ANYTHING ELSE not even the json code block string:"
    response = model.generate_content(prompt)
    jsonobj = response.text
    jsonobj = jsonobj.removeprefix("```json\n")
    jsonobj = jsonobj.removesuffix("```\n")
    print("Model output fallback : ",jsonobj)
    final_dict = json.loads(jsonobj)
    return final_dict

def diagnosiser(type,info):
    format = """
    {
    "Diet" = "--",
    "Medications" = "--",
    "Additional_info" = "--",
    }
    """
    prompt = f"""I want you to act as a diabetic expert doctor and analyze the following patients conditions, Diabetes Type = {type}, personal information = {info} and after this i want you to provide him perfect diet, medications, additional information about physical activity and changes in day to day life to make conditions better. \n Absolutely follow the following format while making the diagnosis : {format} (do not give anything else)
    Keep in mind you are operating in India, provide the diet which is indianized, has indian foods and also is economical for the patient. Also provide the exercises which donot require heavy equipment. Provide very very specific answers dont give generalized options."""
    response = model.generate_content(prompt)
    jsonobj = response.text
    jsonobj = jsonobj.removeprefix("```json\n")
    jsonobj = jsonobj.removesuffix("```\n")
    print("Diagnosis on day to day life : ",jsonobj)
    final_dict = json.loads(jsonobj)
    doctor_concisation = doctor_report(type,info)
    final = {
        "user":final_dict,
        "doctor":doctor_concisation
    }
    return final


def doctor_report(type,info):
    format = """
    {
    "Concise_diagnosis" = "--",
    }
    """
    prompt = f"""As an endocrinologist, provide a concise analysis for a patient with {type} diabetes. Patient context: {info}
    Please provide:
    1. Key findings (2-3 sentences)
    2. Recommended medication plan (primary and alternatives)
    3. Next steps (prioritized list of 2-3 immediate actions)
    4. Additional tests required, if any
    Keep all sections brief and actionable, focusing on critical information only.
    Keep the output only in the format and nothing else : {format}"""    
    response = model.generate_content(prompt)
    jsonobj = response.text
    jsonobj = jsonobj.removeprefix("```json\n")
    jsonobj = jsonobj.removesuffix("```\n")
    print("Diagnosis concisation for the doctor: ",jsonobj)
    final_dict = json.loads(jsonobj)
    return final_dict

