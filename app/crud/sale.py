from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.company import Company
from app.models.inventory import Inventory
from app.models.sales import Sale
from app.schemas.sales import SalesCreate, SalesUpdate

# Helper function to fetch a sale by ID
def get_sale_by_id(db: Session, sale_id: int) -> Sale:
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sale with ID {sale_id} not found."
        )
    return sale
# Fetch a company by ID
def get_company_by_id(db: Session, company_id: int) -> Company:
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found."
        )
    return company

# Fetch an inventory item by ID
def get_inventory_by_id(db: Session, inventory_id: int) -> Inventory:
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory with ID {inventory_id} not found."
        )
    return inventory

# Retrieve all sales records
def get_all_sales(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Sale).offset(skip).limit(limit).all()

# Create a new sale and update inventory atomically
def create_sale(db: Session, payload: SalesCreate) -> Sale:
    company = get_company_by_id(db, payload.company_id)
    inventory_item = get_inventory_by_id(db, payload.inventory_id)

    # Validate Company
    if not company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Company with ID {payload.company_id} does not exist."
        )
   
    # Validate inventory stock
    if inventory_item.quantity < payload.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock for inventory item {inventory_item.serial_no}.",
        )

    # Create sale and update inventory within a transaction
    new_sale = Sale(**payload.dict())
    inventory_item.quantity -= payload.quantity

    try:
        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create sale: {str(e)}"
        )

    return new_sale

# Update a sale
def update_sale(db: Session, sale: Sale, payload: SalesUpdate) -> Sale:
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(sale, key, value)  # Update only provided fields
    db.add(sale)
    try:
        db.commit()
        db.refresh(sale)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update sale: {str(e)}",
        )
    return sale

# Delete a sale
def delete_sale(db: Session, sale: Sale):
    try:
        db.delete(sale)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete sale: {str(e)}",
        )