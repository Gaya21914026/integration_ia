from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.database import connect_db
from app.models.users import Users
from app.services.users import SECRET_KEY, ALGORITHM



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(connect_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        role: str = payload.get("role")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token invalide")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    return user


def is_admin(current_user = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    return current_user
