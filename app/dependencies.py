from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.utils.uow import IUnitOfWork, UnitOfWork

oauth2_token = OAuth2PasswordBearer(tokenUrl="login")
TokenDep = Annotated[str, Depends(oauth2_token)]

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
AuthDep = Annotated[OAuth2PasswordRequestForm, Depends()]
