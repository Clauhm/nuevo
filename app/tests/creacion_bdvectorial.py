from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
import re
from langchain.schema import Document

os.environ["OPENAI_API_KEY"] = ""
model = ChatOpenAI(model="gpt-4o", temperature=0.8)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=768
)

def limpiar_texto(texto):
    texto = re.sub(r'\s+', ' ', texto)
    texto = re.sub(r'•|·|-|\*|•|\u2022', '', texto)
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto.strip()

def summarize_and_add_metadata(model, pages):
    # Crear plantilla de prompt para el resumen
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Write a concise summary of the following:\\n\\n{context}")]
    )

    # Crear una cadena para procesar los documentos
    chain = create_stuff_documents_chain(model, prompt)
    result = chain.invoke({"context": pages})

    # Dividir el contenido en partes más pequeñas
    text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=50)
    splits = text_splitter.split_documents(pages)

    # Añadir metadatos de resumen a cada parte
    for i, split in enumerate(splits):
        split.metadata = {"resumen": result}

    return splits

ruta_carpeta = "C:\\Users\\Claudia\\Documents\\Temas Scotia\\prueba_chatbot\\app\\data\\corpus"
all_splits = []

for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith(".pdf"):
        ruta_pdf = os.path.join(ruta_carpeta, archivo)
        loader = PyPDFLoader(ruta_pdf)
        pages = loader.load_and_split()

        # Limpieza del texto y procesamiento
        cleaned_pages = [Document(page_content=limpiar_texto(page.page_content), metadata=page.metadata) for page in pages]
        splits = summarize_and_add_metadata(model, cleaned_pages)
        all_splits.extend(splits)

vectorstore = Chroma.from_documents(
    collection_name="db_prueba", 
    documents=all_splits, 
    embedding=embeddings, 
    persist_directory="C:\\Users\\Claudia\\Documents\\Temas Scotia\\prueba_chatbot\\app\\data\\chroma_langchain_db"
)



