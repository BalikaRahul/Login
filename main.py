from fastapi import FastAPI, Request,Form,Depends,Query
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel

from database import engine, Base,SessionLocal
from models import Forms
DATABASE_URL = "sqlite:///./task.db"


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
#this function helps to create temp connection between backend and server
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Inputtype(BaseModel):
        first_name:str
        last_name:str
        phone_number:str
        email:str
        gender:str
        city:str

@app.get("/home.html", response_class=HTMLResponse)
def home(req: Request, first_name: str = Query()):
    return templates.TemplateResponse(
        request=req,
        name="home.html",
        context={
            "first_name": first_name
        }
    )


@app.get("/product.html", response_class=HTMLResponse)
def products(req: Request):
    products = [
        (1, "laptop", 80000),
        (2, "iphone", 87000)
    ]

    return templates.TemplateResponse(
        request=req,
        name="product.html",
        context={
            "products": products
        }
    )
@app.get('/index.html',response_class=HTMLResponse)
def FormsInput(req:Request):
    return templates.TemplateResponse(
        request=req,
        name="index.html",
        context={   
        }
    )
@app.post('/index.html')
def register(user:Annotated[Inputtype,Form()],db=Depends(get_db)):
    new_user = Forms(
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        email=user.email,
        gender=user.gender,
        city=user.city
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse(
        url=f"/home.html?first_name={user.first_name}",
        status_code=303
    )
