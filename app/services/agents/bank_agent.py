from services.tools.bdrelacional import get_query_database
from services.tools.bdvectorial import get_qa_bank
from services.tools.get_estadosdecuenta import get_bank_statements
from services.tools.consultas_estadosdecuenta import query_pdf_tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from services.models.model_openai import modelo

model = modelo()

memory = MemorySaver()

tools = [ get_query_database, get_qa_bank, query_pdf_tool, get_bank_statements]

prompt = """
Respond in spanish. You are a helper who uses tools to answer questions related to account statements, database queries, PDF analysis, or banking queries that are obtained from the tools.
If the question is not related to these topics, respond with: 'Sorry, I don't know the answer.'
"""

graph = create_react_agent(model, tools=tools, state_modifier=prompt, checkpointer=memory)

