from fastapi import APIRouter,Header, HTTPException
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





'''

@router.post("/verifytoken")
def verifytoken(Authorization: str=Header(None)):
    token = Authorization.split(" ")[1]
    print(token)
    return "success"


@router.post("/token")
async def token(auth: Auth):
    
    ##print("AQUI")
    user = nuevo_auth.login(auth)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    else:
        print(user["id"])
        access_token = nuevo_auth.create_access_token(data={"sub": user["usuario"]})
    return access_token

 
@router.get("/protected-endpoint/")
async def protected_endpoint(token: str = Depends(nuevo_auth.verify_token)):
    if nuevo_auth.verify_token_expiration(token):
        raise HTTPException(status_code=401, detail="Token has expired")
        # Resto del código para el endpoint protegido
    return {"message": "Access granted "}
'''