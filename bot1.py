import streamlit as st
import openai

st.title("Personal Chatbot")

# Set OpenAI API key from Streamlit secrets
openai_api_key = st.text_input("Enter your OpenAI API key:", type="password")
openai.api_key = openai_api_key

if openai_api_key:
    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4-turbo"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Create the messages to send to the API
        api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

        # Request a completion from OpenAI
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=api_messages
        )

        # Extract the assistant's message from the response
        assistant_message = response.choices[0].message["content"]
        
        # Add the assistant's message to the chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        
        # Display the assistant's message in the chat message container
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
else:
    st.warning("Please enter your OpenAI API key to continue.")
