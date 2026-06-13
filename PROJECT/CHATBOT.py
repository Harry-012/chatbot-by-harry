import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate

import os
##PAGE CONFIG
st.set_page_config(page_title="Chatbot with Groq", page_icon=" 🤖")
##TITLE
st.title("🤖 YOUR PERSONAL AI")
st.markdown("This is a simple chatbot built using LangChain and Groq. Ask me anything!")

## SIDEBAR
with st.sidebar:
    st.header("Settings")
## API KEY
    api_key = st.text_input("GROQ API KEY", type="password", help="You can get your API key from the console.groq.com")
## MODEL SELECTION
    model_name= st.selectbox(
      "model", 
      ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
      index=0,
        )
##CLEAR BUTTON
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

#initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

## INITIALIZE LLM
@st.cache_resource
def get_chain(api_key, model_name):
    if not api_key:
        return None

    ## Initialize the Groq model
    llm = ChatGroq(
        groq_api_key=api_key,
        model=model_name,
        temperature=0.7,
        streaming=True,
    )

    ##CREATE PROMPT TEMPLATE
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer the user's question clearly and concisely."),
        ("user", "{question}"),
    ])

    #CERATE CHAIN
    chain = prompt | llm | StrOutputParser()
    return chain

##GET CHAIN
chain = get_chain(api_key, model_name)
if not chain:
    st.warning("Please enter your GROQ API key to start chatting.")
    st.markdown("You can get your API key from [console.groq.com](https://console.groq.com).")
else:
    ##display chat message
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

##USER INPUT
if question := st.chat_input("Type your message here..."):
##ADD USER MESSAGE TO SESSION STATE
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

##GENERATE RESPONSE
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            for chunk in chain.stream({"question":question}):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
            ##ADD TO HISTORY
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            message_placeholder.markdown("Sorry, something went wrong. Please try again.")
            st.error(f"Error: {e}")

##EXAMPLES
st.markdown("### ")
st.markdown("###  TRY THESE Examples")
col1, col2 = st.columns(2)
with col1:
    st.markdown("- What is Groq?")
    st.markdown("- How does Groq work?")
    st.markdown("- What is the difference between Groq and other AI accelerators?")
with col2:
    st.markdown("- What are the benefits of using Groq?")
    st.markdown("- How can I get started with Groq?")
    st.markdown("- What are some use cases for Groq?")

##FOOTER
st.markdown("---")
st.markdown("Made with ❤️ by [HARSHIT JOSHI]")