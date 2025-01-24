from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.sales import Sale

# Helper function to fetch a sale by ID
def get_sale_by_id(db: Session, sale_id: int) -> Sale:
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sale with ID {sale_id} not found."
        )
    return sale

# Retrieve all sales records
def get_all_sales(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Sale).offset(skip).limit(limit).all()
