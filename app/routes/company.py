from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import getDb
from app.schemas.company import Company, CompanyCreate
from app.crud import company as crud_company

company_router = APIRouter()

@company_router.post(
    "/", 
    response_model=Company, 
    tags=["Companies"], 
    summary="Create a new company (Admin only)", 
    status_code=201
)
def create_company(company: CompanyCreate, db: Session = Depends(getDb)):
    return crud_company.create_company(db, company)

@company_router.get(
    "/", 
    response_model=list[Company], 
    tags=["Companies"], 
    summary="Retrieve a list of companies", 
    status_code=200
)
def get_companies(skip: int = 0, limit: int = 10, db: Session = Depends(getDb)):
    return crud_company.get_companies(db, skip=skip, limit=limit)

@company_router.get(
    "/{company_id}", 
    response_model=Company, 
    tags=["Companies"], 
    summary="Retrieve a specific company by ID", 
    status_code=200
)
def get_company(company_id: int, db: Session = Depends(getDb)):
    company = crud_company.get_companies(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
