import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from services.agents.bank_agent import graph
from services.db_cache.cache import check_cache, save_answer
import json

def format_message(message, message_type):
    if message_type == "HUMANMESSAGE":
        return f"**🧑 Usted:** {message.content}"
    elif message_type == "AIMESSAGE" and message.content.strip():
        return f"**🤖 AI:** {message.content}"
    else:
        return None

st.title("Chatbot Bancario")

user_input = st.text_input("Escribe tu mensaje:")

if st.button("Enviar") and user_input:

        answer = check_cache(user_input)
        if answer is not None:
            st.markdown(answer)
        else:
            msg = f"{user_input}"
            response = graph.invoke(
                input={"messages": msg},
                config={
                    "configurable": {
                        "thread_id": "1",    
                    }
                }
            )
            
            last_message = None

            # Busca si hay un llamado a herramienta
            last_tool_call = next(
                (
                    tool_call for tool_call in response.get("messages", [])
                    if hasattr(tool_call, "type") and tool_call.type == "tool_call"
                ),
                None
            )

            # Verifica si el tool utilizado es 'get_qa_bank'
            if last_tool_call and hasattr(last_tool_call, "name") and last_tool_call.name == "get_qa_bank":
                # Encuentra el mensaje relacionado con 'get_qa_bank'
                last_message = response["messages"][-1]  # Último mensaje en la lista
                formatted_message = format_message(last_message, type(last_message).__name__.upper())

                if formatted_message:
                    st.markdown(formatted_message)
                    save_answer(user_input, formatted_message)
            else:
                # Si no es 'get_qa_bank', simplemente muestra la última respuesta del agente
                last_message = response["messages"][-1]  # Último mensaje en la lista
                formatted_message = format_message(last_message, type(last_message).__name__.upper())

                if formatted_message:
                    st.markdown(formatted_message)