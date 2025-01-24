from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate

def create_company(db: Session, company: CompanyCreate):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_companies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Company).offset(skip).limit(limit).all()

def get_company(db: Session, user_id: int):
    return db.query(Company).filter(Company.id == user_id).first()
