from fastapi import APIRouter, Depends,HTTPException,status
from app.db.database import connect_db
from sqlalchemy.orm import Session
from app.models.users import Users
from app.schemas.users import AdminUpdateUser,UserUpdate,UserResponse
from app.services.users import hashed_password
from app.dependencies.auth import get_current_user


router = APIRouter(prefix="/users",
                   tags=["USERS ROUTERS"],
                   dependencies=[Depends(get_current_user)]
                   )


#CREATE USER == REGISTER USER (CREATE)
#GET ALL USERS FROM DATABASE (READ)
@router.get("",response_model=list[UserResponse])
def get_users(db:Session=Depends(connect_db)):
    users=db.query(Users).all()
    return users

#UPDATE USER BY ID (UPDATE)
@router.put("/{id}",response_model=UserResponse)
def update_users(id:int,data:dict,db:Session=Depends(connect_db),current_user = Depends(get_current_user)):
    user=db.query(Users).filter(Users.id==id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user introuvable"
        )
    
    if current_user.role.value!="admin" :
        update_data = AdminUpdateUser(**data)
    else:
        if current_user.id!=id :   
            raise HTTPException( 
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=["Tu ne peux modifier que ton propre profil", 
                        f"ton id c'est: {current_user.id}"] 
            )
        update_data = UserUpdate(**data) 

    if update_data.name is not None: 
        user.name = update_data.name 
    if update_data.password is not None: 
        user.password = hashed_password(update_data.password)
    
    if current_user.role.value == "admin" and getattr(update_data, "role", None) is not None: 
        user.role = update_data.role

    db.commit() 
    db.refresh(user)
    return user

@router.delete("/{id}")
def delete_user(id:int,db:Session=Depends(connect_db),current_user=Depends(get_current_user)):
    user=db.query(Users).filter(Users.id==id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User introuvable"
        )
    if current_user.role.value!="admin" and current_user.id!=id:
        raise HTTPException( 
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=["Tu ne peux supprimer que ton propre compte", 
                        f"ton id c'est: {current_user.id}"] 
            )
        
    db.delete(user)
    db.commit()
    return {"message": "User effacé avec succès"}