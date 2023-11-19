import streamlit as st
import random
import time

import llm_helper


st.set_page_config(
        page_title="Smart Chatbot",
        page_icon="🤖",
        initial_sidebar_state = "auto",
        # layout="wide"
    )


#### sidebar
with st.sidebar.expander("**Tech Stack**"):
    st.write('''
            - **LLM : Google Palm**
            - **Agents : Google Search, Wikipedia, etc.**
            - **Langchain**
            ''')

with st.sidebar.expander("**App Working**"):
    st.write('''
            **Smart Chatbot : Answers all your queries!!**
            ''')
    
    st.write('''
            - **Dual Modes for Varied Experiences:** Choose between "Default" and "Agents" modes for varied experiences.
            - **Default Mode:**
                - **Operates Internet-Independently:** Relies on LLM Google Palm AI for imaginative responses without requiring an internet connection.
            - **Agents Mode:**
                - **Real-Time Updates:** Integrates external tools like Google Search, Wikipedia, etc., via Langchain's agents, overcoming internet dependency for up-to-date information.
                - **Tackles Connectivity Issues:** Ensures functionality even in low-connectivity or offline scenarios, a feature not commonly found in other advanced chatbots.
            - **Seamless Mode Switching:** Effortlessly transition between modes to explore creativity or stay informed with real-time updates.
            - **Unique Advantage Over Others:** Offers uninterrupted interactions, adeptly handling internet accessibility constraints faced by many advanced chatbots in the market.
            - **Innovative Adaptability:** A chatbot that adjusts to diverse needs, functioning reliably in low-connectivity situations while providing an array of experiences.
            - **Comprehensive Functionality:** From imaginative responses to real-time updates, our Smart Chatbot App ensures a versatile and reliable conversational experience, irrespective of internet availability.
            ''')
    
    with st.sidebar.expander("**About me**"):
        st.write("**Priyansh Bhardwaj**")
        st.write("[Website](https://priyansh-portfolio.streamlit.app/)")
        st.write("[LinkedIn](https://www.linkedin.com/in/priyansh-bhardwaj-25964317a)")


#### chatbot
col1, col2 = st.columns([5, 1])
col2.write("")

#title
col1.title("Smart Chatbot")

#llm/agent selector
selection = col2.selectbox(label="Select method",
                            options=("Default", "Agents"),
                            index=0,
                            help="select Default to use advanced LLM to generate creative results\
                                    \nselect Agents for real time data, recent happenings, etc.",
                            label_visibility = "collapsed"
                            )


selector = {"Default": "**Default mode is used to generate creative results for all sort of queries from writing code to writing a poem, giving scientific explanations to giving life lessons by using only the Google Palm.\
                         To access real time data and to get answers of recent happenings use Agents mode.**",

            "Agents": "**Agents mode uses Google Palm and different tools like google search, wikipedia, etc. to answer your queries related to real time data and recent happenings.\
                         To boost your creativity while generating responses use Default mode.**"}

st.write(selector[selection])


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


## Deleting chat history after 5 conversation exchange(1Q+1A)
#only keeping last 5 conversation exchange

if len(st.session_state.messages) == 10:
    del st.session_state.messages[0:2]


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
        # print(prompt)
        # print(type(prompt))

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        with st.spinner(''):
            if selection == "Default":
                # assistant_response = llm_helper.llm_query_response(prompt)
                assistant_response = llm_helper.llm_with_memory(prompt)
            if selection == "Agents":
                assistant_response = llm_helper.query_response_with_agents(prompt)

        # Simulate stream of response with milliseconds delay
        # print(assistant_response.split('\n'),'\n\n')
        for lines in assistant_response.split('\n'):
            for chunk in lines.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            full_response += '  \n'
        # print(full_response, '\n\n')
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # print("\n\nMessages:\n", st.session_state.messages, "\n\n")
