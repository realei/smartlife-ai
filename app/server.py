from fastapi import FastAPI, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import RedirectResponse
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
from jose import JWTError, jwt
import os

from .agent import shoppingAgent



app = FastAPI(
    title="SmartLife-AI's LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.middleware("http")
async def verify_jwt(request: Request, call_next):
    # Skip the middleware for the /docs and /openapi.json endpoints
    if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
        return await call_next(request)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    authorization: str = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if authorization is None or scheme.lower() != "bearer":
        raise credentials_exception
    try:
        unverified_header = jwt.get_unverified_header(param)
        alg = unverified_header['alg']
        jwt.decode(param, os.getenv('AUTH_SECRET'), algorithms=[alg])
    except (JWTError, Exception):
        raise credentials_exception
    return await call_next(request)


# @app.get("/")
# async def redirect_root_to_docs():
#     return RedirectResponse("/docs")


# # Edit this to add the chain you want to add
# add_routes(app, NotImplemented)

add_routes(
    app,
    ChatOpenAI(),
    path="/openai",
)

agent = shoppingAgent()

add_routes(
    app,
    agent,
    path="/agent",
)

model = ChatOpenAI(model="gpt-3.5-turbo-1106")
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
add_routes(
    app,
    prompt | model,
    path="/joke",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", default=8000))