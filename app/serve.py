from fastapi import FastAPI
from langserve import add_routes
from app.chain import qa_chain

app = FastAPI(title="Retrieval App")

# Add the LangServe routes to the FastAPI app
add_routes(app, qa_chain)

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app
    uvicorn.run(app, host="localhost", port=8000)