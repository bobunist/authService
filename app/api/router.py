from fastapi import APIRouter
from jose import jwt

from app.dependencies import TokenDep, UOWDep, AuthDep
from app.schemas.user import UserAuth, UserRead
from app.services.auth.auth_service import AuthService
from config import settings

router = APIRouter(
    prefix="",
    tags=[],
    dependencies=[],
    responses={},
)
# ///////////////////////
# //  _____   ____ ______
# // / ___/  / __//_  __/
# /// (_ /  / _/   / /
# //\___/  /___/  /_/
# ///////////////////////

# //////////////////////////////
# //   ___   ____    ____ ______
# //  / _ \ / __ \  / __//_  __/
# // / ___// /_/ / _\ \   / /
# ///_/    \____/ /___/  /_/
# //////////////////////////////


@router.post('/registration')
async def registration(uow: UOWDep, user: UserAuth):
    res = await AuthService().reg_user(user, uow)
    return res


@router.post('/new-confirm-code')
async def send_new_confirm_code(uow: UOWDep, token: TokenDep):
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    email: str = payload.get("sub")
    res = await AuthService().send_email_confirm(email, uow)
    return res


@router.post('/confirm-registration/{email}/{code}')
async def confirm_registration(uow: UOWDep, code: str, email: str):
    res = await AuthService().confirm_reg(email, code, uow)
    if not res:
        return 'Successful'
    return res


@router.post('/login')
async def login(uow: UOWDep, form_data: AuthDep):
    email = form_data.username
    password = form_data.password
    res = await AuthService().log_user(email, password, uow)
    return res


@router.post('/me')
async def me(uow: UOWDep, token: TokenDep) -> UserRead:
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    email: str = payload.get("sub")
    res = await AuthService().get_me(email, uow)
    return res

# ///////////////////////////////////////////
# //   ___    ____   __    ____ ______   ____
# //  / _ \  / __/  / /   / __//_  __/  / __/
# // / // / / _/   / /__ / _/   / /    / _/
# ///____/ /___/  /____//___/  /_/    /___/
# ///////////////////////////////////////////


# ////////////////////////
# //   ___   __  __ ______
# //  / _ \ / / / //_  __/
# // / ___// /_/ /  / /
# ///_/    \____/  /_/
# ////////////////////////
