from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi import File
from fastapi.encoders import jsonable_encoder

register = Jinja2Templates(directory="templates")
adminLogin = Jinja2Templates(directory="templates")
result = Jinja2Templates(directory="templates")
header = Jinja2Templates(directory="templates")
school = Jinja2Templates(directory="templates")
index = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/homePage", response_class=HTMLResponse)#http://127.0.0.1:8000/homePage/
def show_home_page(request: Request):
    return index.TemplateResponse("index.html", context={"request": request})

@app.get("/schoolPage", response_class=HTMLResponse)#http://127.0.0.1:8000/schoolPage/
def show_school_page(request: Request):
    return school.TemplateResponse("school.html", context={"request": request})
@app.get("/headerPage", response_class=HTMLResponse)#http://127.0.0.1:8000/headerPage/
def show_header_page(request: Request):
    return header.TemplateResponse("header.html", context={"request": request})

@app.get("/registerPage", response_class=HTMLResponse)#http://127.0.0.1:8000/registerPage/
def show_service_page(request: Request):
    return register.TemplateResponse("register.html", context={"request": request})

@app.get("/resultPage", response_class=HTMLResponse)#http://127.0.0.1:8000/resultPage/
def show_result_page(request: Request):
    return result.TemplateResponse("result.html", context={"request": request})

uri = "mongodb+srv://demo:Demo_123@cluster0.w2hpa44.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.school


class Result(BaseModel):
   
    Roll_no: int
    Name:str
    Course :str
    Total_mark : int
    Percentage:int
    Status: str

class User(BaseModel):
    user_name:str
    password: int
class Register(BaseModel):
   
    name: str
    email:str
    mobile:int
    dob: str
    Password:str
    


@app.get("/api/result/findAll", response_model=List[Result])
def list_results():
    results = list(db["results"].find(limit=100))
    return results

@app.post("/api/result/create", response_model=List[Result])
def create_result(result: Result):
    result = jsonable_encoder(result)
    object_id = db["results"].insert_one(result)
    results = list(db["results"].find(limit=100))
    return results


@app.get("/api/result/findOne", response_model=List[Result])
def find_one(Roll_no: int=Form()):
    results = db["results"].find_one({"Roll_no": Roll_no})
    return results


@app.put("/api/result/update")
def update_result(Roll_no: int, results:Result ):
    results = jsonable_encoder(results)
    update_result = db["result"].update_one(
        {"Roll_no": Roll_no}, {"$set": results})
    return f"{Roll_no} updated successfully"


@app.delete("/api/result/delete")
def delete_result(Roll_no: int):
    delete_result = db["results"].delete_one({"Roll_no": Roll_no})
    return f"{Roll_no} deleted successfully"

@app.post("/register") #http://127.0.0.1:8000/register/
def user(name: str = Form(), email: str = Form(),mobile: int = Form(),dob: str = Form(),Password: str = Form()):
    """This service takes details from client and return a greeting msg"""
    x = {"name":name,"email":email,"mobile":mobile,"dob":dob,"password":Password}
    obj = db["Registers"].insert_one(x)  

    return "Successfully Registered"



@app.post("/result") #http://127.0.0.1:8000/result/
def user(roll_no: str = Form()):
    """This service takes details from client and return a greeting msg"""
    
    return "Successfully"

@app.get("/loginPage", response_class=HTMLResponse)#http://127.0.0.1:8000/loginPage/
def show_service_page(request: Request):
    return adminLogin.TemplateResponse("adminLogin.html", context={"request": request})
@app.post("/login")#http://127.0.0.1:8000/login/
def check_user(request: Request, name: str = Form(), password: int = Form()):
    '''
    checking username and password
    '''
    user = db["Registers"].find_one({"name": name})
    if name == user["name"] and password == user[ "password"] :
        return "Success"
        #adminLogin.TemplateResponse("adminLogin.html", context={"request": request})
    else:
        return "Unsuccessful sign_in"
