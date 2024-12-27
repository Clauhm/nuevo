import pdfplumber
import os
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import Document
from services.models.model_openai import modelo
import os
#from langchain_openai import ChatOpenAI

model = modelo()

#os.environ["OPENAI_API_KEY"] = ""
#model = ChatOpenAI(model="gpt-4o", temperature=0.8)

dni = "12345678"
mes = "agosto"
año = "2024"

# Directorio base donde se encuentran los estados de cuenta
base_dir = "app\data\estados_de_cuenta"

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

@tool
def query_pdf_tool(query):
    '''Use this tool to check your bank account status and answer user questions.'''

    pdf_filename = f"{dni}_{mes}_{año}.pdf"
    pdf_path = os.path.join(base_dir, dni, pdf_filename)

    text = extract_text_from_pdf(pdf_path)

    document = Document(page_content=text, metadata={})

    prompt = ChatPromptTemplate.from_messages(
        [("system", "El siguiente es el contenido del estado de cuenta:\n{context}\n\nPregunta: {query}\nRespuesta:")]
    )

    chain = create_stuff_documents_chain(model, prompt)

    try:
        result = chain.invoke({"context": [document], "query": query})
    except AttributeError as e:
        print(f"AttributeError: {e}")
        return str(e)

    return result


#response = query_pdf_tool.invoke("Cual es el pago minimo de mi estado de cuenta")
#print(response)



