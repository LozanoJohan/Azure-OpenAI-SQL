# main_app.py

import streamlit as st
import pandas as pd
import sql_db
from prompts.prompts import SYSTEM_MESSAGE_2
from openai_chat import get_completion_from_messages
import json
from utils import query_getter

def query_database(query, conn):
    """ Run SQL query and return results in a dataframe """
    return pd.read_sql_query(query, conn)

# Create or connect to SQLite database
conn = sql_db.create_connection()

# Schema Representation for finances table
schemas = sql_db.get_schema_representation_from_json()


def on_user_input(user_message):
    chat_response = ""
    # Format the system message with the schema
    formatted_system_message = SYSTEM_MESSAGE_2#.format(schema=schemas)

    # Use GPT-4 to generate the SQL query
    response = get_completion_from_messages(formatted_system_message, user_message)
    json_response = json.loads(response)

    st.write(json_response)

    answer = json_response["answer"]
    if answer and json_response["keywords"] == None:
        st.write(answer)
        return answer

    else:
        query = query_getter(json_response["keywords"], json_response["limit"])        
        # st.code(query, language="sql")

        # try:
        # Run the SQL query and display the results
        sql_results = query_database(query, conn)
        st.write("Query Results:")
        st.dataframe(sql_results)

        query_json = sql_results.to_dict()
        st.write(query_json)
        # Use GPT-4 to generate the SQL query
        info_str = SYSTEM_MESSAGE_2 + "You have to answer the questions based in the following info:" + str(query_json)
        response_ = get_completion_from_messages(info_str, user_message)
        print("aaaaa " + "You have to answer the questions based in the following info:" + str(query_json))

        response_ = json.loads(response_)
        st.write(response_)

        answer_ = response_["answer"]
        if answer_:
            st.write(answer_)
            chat_response += answer_
        
            return chat_response

        # except Exception as e:
        #     return f"An error occurred: {e}"




st.title("GPT")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Hola, en qué puedo ayudarte?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = on_user_input(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

