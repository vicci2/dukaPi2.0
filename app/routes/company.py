from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import getDb
from app.dependencies.auth import get_current_user_with_role
from app.schemas.company import CompanyRes, CompanyCreate, CompanyUpdate
from app.crud import company as crud_company
from app.schemas.user import User

company_router = APIRouter()

@company_router.post(
    "/",
    response_model=CompanyRes,
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
    response_model=list[CompanyRes],
    summary="Retrieve a list of companies (Admin Only)",
    status_code=200,
)
def get_companies(db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    """
    Get a paginated list of companies.
    """
    return crud_company.get_companies(db,current_user)


@company_router.get(
    "/{company_id}",
    response_model=CompanyRes,
    summary="Retrieve a specific company by ID (Admin Only)",
    status_code=200,
)
def get_company(db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin"))):
    """
    Retrieve a specific company by its ID.
    """
    company = crud_company.get_company(db, current_user)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@company_router.put(
    "/{company_id}",
    response_model=CompanyRes,
    summary="Update an existing company (Admin Only)",
    status_code=200,
)
def update_company(
    company_id: int, payload: CompanyUpdate, db: Session = Depends(getDb)
, current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    """
    Update company details.
    """
    return crud_company.update_company(db, company_id, payload, current_user), 


@company_router.delete(
    "/{company_id}",
    response_model=dict,
    summary="Delete a company  (Admin Only)",
    status_code=200,
)
def delete_company(company_id: int, db: Session = Depends(getDb),current_user: User = Depends(get_current_user_with_role("admin"))):
    """
    Delete a specific company by its ID.
    """
    crud_company.delete_company(db, company_id, current_user)
    return {"message": f"Company with ID {company_id} successfully deleted."}