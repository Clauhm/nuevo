from langchain_openai import ChatOpenAI
from config.settings import settings

def modelo():
       model = ChatOpenAI(model="gpt-4o", temperature=0, api_key=settings.openai_api_key)
       return model 
