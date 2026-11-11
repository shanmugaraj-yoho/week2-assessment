from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import InterfaceError

from .database import get_db
from . import models, schemas
from src.dependencies import verify_api_key

app = APIRouter(prefix="/customers", tags={"Customers"}, dependencies=[Depends(verify_api_key)])

#Create Customers
@app.post("/",response_model=schemas.CustomerOut)
def create_customer(
    customer : schemas.CustomerCreate,
    db : Session = Depends(get_db),
):
    new_customer = models.Customer(**customer.model_dump())

    db.add(new_customer)

    try:
        db.commit()
        db.refresh(new_customer)
    except InterfaceError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")

    return new_customer

#Get customers
@app.get("/", response_model=list[schemas.CustomerOut])
def get_customers(
    page : int = Query(1,ge=1),
    per_page : int = Query(5, ge =1, le=100),
    db : Session = Depends(get_db)):
        offset = (page-1) * per_page
        customers = db.query(models.Customer).offset(offset).limit(per_page).all()
        return customers

#Get customer by id
@app.get("/{cutomer_id}", response_model=schemas.CustomerOut)
def get_customer(customer_id : int, db : Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer Not Found")

    return customer

#Update Customer
@app.put("/{customer_id}", response_model= schemas.CustomerOut)
def update_customer( customer_id: int, customer_data: schemas.CustomerUpdate,db:Session= Depends(get_db)):
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer Not Found")

    update_data = customer_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(customer, key, value)

        try:
            db.commit()
            db.refresh(customer)
        except InterfaceError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Email already exists")

        return customer

#Delete Customer
@app.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()
     
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer Not Found")

    db.delete(customer)
    db.commit()

    return {"message" : "Customer Deteled Successfully"}