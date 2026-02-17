from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.db.database import connect_db
from app.models.users import Users,UserRole
from app.schemas.users import UserLogin,UserResponse,UserCreate
from app.services.users import verify_password,create_access_token,hashed_password
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth",tags=["LOGIN ROUTERS"])

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(connect_db)):
    db_user = db.query(Users).filter(Users.name == user.name).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Utilisateur ou mot de passe  incorrect")


    token = create_access_token({
        "id": db_user.id,
        "role": db_user.role.value 
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

#ADD USER TO DATABASE (CREATE)
@router.post("/register",response_model=UserResponse)
def add_users(user:UserCreate, db:Session=Depends(connect_db)):
    existing=db.query(Users).filter(Users.name==user.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="un user avec ce nom existe déja"
        )
    new_user=Users(name=user.name,password=hashed_password(user.password),role=UserRole.user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "role": current_user.role.value
    }
