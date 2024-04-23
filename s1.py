from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

responce = llm.invoke("What is 2+2")

print(responce)