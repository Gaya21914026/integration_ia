from fastapi import APIRouter, Depends,HTTPException,status
from app.schemas.products import ProductCreate, ProductResponse,ProductUpdate
from app.db.database import connect_db
from sqlalchemy.orm import Session
from app.models.products import Products
router = APIRouter(prefix="/products",tags=["PRODUCT ROUTERS"])




#ADD PRODUCT TO DATABASE (CREATE)
@router.post("",response_model=ProductResponse)
def add_products(product:ProductCreate,  db: Session = Depends(connect_db)):
    existing = db.query(Products).filter(Products.name == product.name).first() 
    if existing: 
        raise HTTPException( 
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Un produit avec ce nom existe déjà." 
            )
    new_product = Products(name=product.name,price=product.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

#GET ALL PRODUCT FROM DATABASE (READ)
@router.get("",response_model=list[ProductResponse])
def get_products(db: Session = Depends(connect_db)):
    products = db.query(Products).all() 
    return products


#UPDATE PRODUCT BY ID (UPDATE)
@router.put("/{id}",response_model=ProductUpdate)
def update_product(id:int, data:ProductUpdate,db:Session=Depends(connect_db)):
    product = db.query(Products).filter(Products.id == id).first()
    if not product: 
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit introuvable" 
        )
    
    if data.name is not None:
        product.name = data.name 
    
    if data.price is not None:
        product.price = data.price
    
    db.commit() 
    db.refresh(product) 
    return product


#DELETE PRODUCT FROM DATABASE (DELETE)
@router.delete("/{id}")
def delete_products(id:int,db: Session = Depends(connect_db)):
    product = db.query(Products).filter(Products.id == id).first() 
    if not product: 
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Produit introuvable" 
            )
    db.delete(product) 
    db.commit() 
    return {"message": "Produit effacé avec succès"}