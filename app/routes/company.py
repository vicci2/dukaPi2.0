from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import getDb
from app.schemas.company import Company, CompanyCreate, CompanyUpdate
from app.crud import company as crud_company

company_router = APIRouter()

@company_router.post(
    "/",
    response_model=Company,
    summary="Create a new company (Admin only)",
    status_code=201,
)
def create_company(company: CompanyCreate, db: Session = Depends(getDb)):
    """
    Create a new company entry.
    """
    return crud_company.create_company(db, company)


@company_router.get(
    "/",
    response_model=list[Company],
    summary="Retrieve a list of companies",
    status_code=200,
)
def get_companies(skip: int = 0, limit: int = 10, db: Session = Depends(getDb)):
    """
    Get a paginated list of companies.
    """
    return crud_company.get_companies(db, skip=skip, limit=limit)


@company_router.get(
    "/{company_id}",
    response_model=Company,
    summary="Retrieve a specific company by ID",
    status_code=200,
)
def get_company(company_id: int, db: Session = Depends(getDb)):
    """
    Retrieve a specific company by its ID.
    """
    company = crud_company.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@company_router.put(
    "/{company_id}",
    response_model=Company,
    summary="Update an existing company",
    status_code=200,
)
def update_company(
    company_id: int, payload: CompanyUpdate, db: Session = Depends(getDb)
):
    """
    Update company details.
    """
    return crud_company.update_company(db, company_id, payload)


@company_router.delete(
    "/{company_id}",
    response_model=dict,
    summary="Delete a company",
    status_code=200,
)
def delete_company(company_id: int, db: Session = Depends(getDb)):
    """
    Delete a specific company by its ID.
    """
    crud_company.delete_company(db, company_id)
    return {"message": f"Company with ID {company_id} successfully deleted."}