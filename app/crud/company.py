from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyRes, CompanyUpdate


def create_company(db: Session, company: CompanyCreate) -> CompanyRes:
    # Check if email or name already exists
    if db.query(Company).filter(Company.email == company.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A company with this email already exists.",
        )
    if db.query(Company).filter(Company.name == company.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A company with this name already exists.",
        )

    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_companies(db: Session, current_user) -> List[CompanyRes]:
    companies = db.query(Company).filter(Company.id == current_user.company_id).offset(0).limit(40).all()
    return companies

def get_company(db: Session, current_user) -> Optional[CompanyRes]:
    company = db.query(Company).filter(Company.id == current_user.company_id).first()
    return CompanyRes.model_validate(company) if company else None

def update_company(db: Session, company_id: int, update_data: CompanyUpdate, current_user) -> CompanyRes:
    company = get_company(db, current_user)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found.",
        )

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(company, key, value)

    try:
        db.commit()
        db.refresh(company)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update company: {str(e)}",
        )
    return company

def delete_company(db: Session, company_id: int, current_user) -> None:
    company = get_company(db, company_id, current_user)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found.",
        )
    db.delete(company)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete company: {str(e)}",
        )
