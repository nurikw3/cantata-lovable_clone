from langchain_groq import ChatGroq
import os, dotenv
dotenv.load_dotenv()


llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"))
print(llm.invoke("Hello, world!"))