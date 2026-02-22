import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import status
import logging
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM

import os
from dotenv import load_dotenv
load_dotenv()

app =FastAPI()

os.environ["LANGSMITH_API_KEY"] =os.getenv("LANGCHAIN_API_KEY")

## API's

@app.post("/blogs")
async def create_blogs(request:Request):
    data = await request.json()
    topic =data.get("topic","")
    language =data.get("language",'')

    ## get the llm object

    groqllm = GroqLLM()
    llm = groqllm.get_llm()

    ## get the graph
    graph_builder = GraphBuilder(llm)
    try:
        if language and topic:
            graph = graph_builder.setup_graph(usecase="language")
            state = graph.invoke({"topic": topic, "current_language": language.lower()})
            print(language)
        elif topic:
            graph = graph_builder.setup_graph(usecase="topic")
            state = graph.invoke({"topic": topic})
        else:
            return JSONResponse({"error": "missing_parameters", "detail": "topic (and optional language) required"}, status_code=status.HTTP_400_BAD_REQUEST)

        return {"data": state}
    except Exception as e:
        logging.exception("create_blogs failed")
        # try to include any extra debug info without exposing secrets
        extra = None
        try:
            extra = getattr(e, "response", None)
        except Exception:
            extra = None
        return JSONResponse({"error": "generation_failed", "detail": str(e), "debug": str(extra)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


if __name__=="__main__":
    uvicorn.run("app:app",host="localhost",port=8000, reload=True)

