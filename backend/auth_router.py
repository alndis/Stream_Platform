from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from redis import Redis

from templates import templates
from schemas import UserCreate, User, Token
from repository import UserRepository
from celery_tasks import send_confirmation_email

router = APIRouter(
    prefix="/api/auth",
    tags=["Аутентификация"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Секретный ключ для JWT
SECRET_KEY = "scrtkey2251"  # Замените на ваш секретный ключ
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время действия токена

# Создание подключения к Redis
redis_client = Redis(host='redis', port=6379, decode_responses=True)

# Функция для создания JWT токена
def create_jwt_token(user: User):
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user.username, "exp": expiration}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register")
async def register(user: UserCreate):
    try:
        existing_user = await UserRepository.get_user_by_username(user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

        existing_user_email = await UserRepository.get_user_by_email(user.email)
        if existing_user_email:
            raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

        hashed_password = pwd_context.hash(user.password)
        user.password = hashed_password

        new_user = await UserRepository.create_user(user)

        confirmation_token = create_jwt_token(new_user)

        send_confirmation_email.delay(user.email, confirmation_token)

        return {"message": "Пользователь успешно зарегистрирован. Проверьте свою почту для подтверждения."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/confirm/{token}", response_class=HTMLResponse)
async def confirm_email(token: str, request: Request):
    print(f"Received token: {token}")  # Для отладки
    try:
        payload = verify_jwt_token(token)
        if payload is None:
            raise HTTPException(status_code=400, detail="Неправильный токен")

        username = payload["sub"]
        user = await UserRepository.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        await UserRepository.confirm_user_email(user.id)
        print("Rendering confirmation_success.html")  # Для отладки
        return templates.TemplateResponse("confirmation_success.html", {"request": request})

    except Exception as e:
        print(f"Error: {str(e)}")  # Для отладки
        raise HTTPException(status_code=400, detail=str(e))




    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserRepository.get_user_by_username(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Неправильный логин или пароль")

    # Генерация токена
    token = create_jwt_token(user)

    # Сохранение токена в Redis с временем жизни 30 минут
    redis_client.set(token, user.username, ex=ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    return {"access_token": token, "token_type": "bearer"}

# Функция для проверки токена
def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

# Зависимость для получения текущего пользователя из токена
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Проверка существования токена в Redis
    username = redis_client.get(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Неправильный токен")

    user = await UserRepository.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Подтвердите email для активации аккаунта.")
    return user
