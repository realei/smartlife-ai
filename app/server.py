from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import RedirectResponse
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes


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

# @app.get("/")
# async def redirect_root_to_docs():
#     return RedirectResponse("/docs")


# # Edit this to add the chain you want to add
# add_routes(app, NotImplemented)

add_routes(
    app,
    ChatOpenAI(model="gpt-3.5-turbo-1106"),
    path="/openai",
)

model = chat = ChatOpenAI(model="gpt-3.5-turbo-1106")
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
add_routes(
    app,
    prompt | model,
    path="/joke",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
