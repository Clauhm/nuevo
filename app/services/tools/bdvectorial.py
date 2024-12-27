from langchain.agents import tool
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from loguru import logger
from services.models.model_openai import modelo
import os
from langchain_openai import ChatOpenAI

#os.environ["OPENAI_API_KEY"] = ""
#model = ChatOpenAI(model="gpt-4o", temperature=0.8)

model = modelo()
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=768
) 

vectorstore = Chroma(collection_name="db_prueba", embedding_function=embeddings, persist_directory="app\data\chroma_langchain_db")
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5}) 

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "Answer in Spanish"
    "\n\n"
    "{context}"
) 

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(model, prompt) 

rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@tool
def get_qa_bank(consulta):
    """Use this tool when the user makes queries related to procedures, applications such as Yape, products or banking regulations that are documented in the available guides or reports. Answer the query of any banking entity."""
    
    response = rag_chain.invoke({"input": consulta })
    return response["answer"] 

#response = get_qa_bank.invoke("No puedo afiliarme a Yape")
#print(response)


