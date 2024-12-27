import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from services.agents.bank_agent import graph
from services.db_cache.cache import check_cache, save_answer

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

                
                last_message = response["messages"][-1]
                formatted_message = format_message(last_message, type(last_message).__name__.upper())

                if formatted_message:
                        st.markdown(formatted_message)

                        save_answer(user_input, formatted_message)

