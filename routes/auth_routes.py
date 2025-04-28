from fastapi import APIRouter,Header, HTTPException, Body
from controllers.auth_controller import *
from models.auth_model import Auth

router = APIRouter()

nuevo_auth = AuthController()


@router.post("/token")
async def token(auth: Auth):
    user = nuevo_auth.login(auth)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    else:
        access_token = nuevo_auth.create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verifytoken")
def verifytoken(Authorization: str = Header(None)):
    if Authorization is None:
        raise HTTPException(status_code=400, detail="Authorization header is missing")

    parts = Authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=400, detail="Invalid Authorization header format")

    token = parts[1]

    return nuevo_auth.validate_token(token, output=True)

@router.post("/verify-google-user")
async def verify_google_user(payload: dict = Body(...)):
    user = nuevo_auth.verify_google_user(payload["email"])
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Crear token con datos adicionales de Google
    google_data = {
        "photoURL": payload.get("photoURL"),
        "uid": payload.get("uid"),
        "displayName": payload.get("displayName")
    }
    
    access_token = nuevo_auth.create_access_token(user, google_data)
    return {"access_token": access_token, "user": user}



