from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# APIRouter
from .routes.api import router
# db configs
from .db import Base, engine

# table creation on startup
# from .models.inventory import Inventory
# from .models.sales import Sale
# from .models.vendors import Vendor
Base.metadata.create_all(bind=engine)

# instance of the fastAPI class
app = FastAPI(
    title="Vicci Shop API",
    description="A sample VicciShop IMS API",
    version="4.1.0",
    docs_url="/viccishop/docs",
    redoc_url="/viccishop/redoc",
    contact={
        "name":"Vicci",
        "email":"vicci2regia@gmail.com",
        "tel":"0728893493"
    }    
)
# CORS Cross Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Template App"}

# Iclude custom endpoints
app.include_router(router)