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


def get_companies(db: Session, skip: int = 0, limit: int = 10) -> List[Company]:
    return db.query(Company).offset(skip).limit(limit).all()


def get_company(db: Session, company_id: int) -> Optional[Company]:
    return db.query(Company).filter(Company.id == company_id).first()


def update_company(db: Session, company_id: int, update_data: CompanyUpdate) -> CompanyRes:
    company = get_company(db, company_id)
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


def delete_company(db: Session, company_id: int) -> None:
    company = get_company(db, company_id)
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
