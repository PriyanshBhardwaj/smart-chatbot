from langchain.prompts import PromptTemplate
# from langchain.llms import HuggingFaceHub
from langchain.llms import GooglePalm
# from langchain.llms import Palm2
from langchain.chains import LLMChain

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

from langchain.agents import AgentType, initialize_agent, load_tools

import os
import streamlit as st
import re

###### create a .env file in your project directory and add HUGGINGFACEHUB_API_TOKEN,GOOGLE_API_KEY, GOOGLE_CSE_ID, PALM_API_KEY as:
# GOOGLE_API_KEY = "your_key"
# GOOGLE_CSE_ID = "your_cse_id"
# HUGGINGFACEHUB_API_TOKEN = "your_key"
# PALM_API_KEY = "your_key"
#
# after that uncomment below two lines of code to load all the tokens


# from dotenv import load_dotenv
# load_dotenv()


# hfHub_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")         #commented because im not using any model from huggingface 
google_key = os.getenv("GOOGLE_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")
google_palm_key = os.getenv("PALM_API_KEY")


##trying different LLMs

#falcon-7b-instruct: LLM
# model_id = "tiiuae/falcon-7b-instruct"

# google/flan-t5-large: LLM
# model_id = "google/flan-t5-large"

# llm = HuggingFaceHub(repo_id = model_id,
#                     model_kwargs = {
#                         "max_length": 500,
#                         "max_new_tokens": 500,
#                         "do_sample":True,
#                         "top_k": 10, 		
#                         "temperature": 0.8,
#                         "repetition_penalty": 50,
#                         "return_full_text": True,
#                         "wait_for_model": True
#                     }
#                     )

#google palm
palm_llm = GooglePalm(google_api_key=google_palm_key, temperature=0.7)
# palm2_llm = Palm2(google_api_key=google_palm_key, temperature=0.7)

#GooglePalm() class is a wrapper for the LaMDA language model. it uses LaMDA language model for response generation.

##google palm(LaMDA) is working best so using it



## conversational objects

#globalising the conversational object without restriction to memory
convo_without_buffer = ConversationChain(llm=palm_llm)   #, verbose=True)

#buffer window memory with memory of only 5 conversational exchange
memory = ConversationBufferWindowMemory(k=5)
convo = ConversationChain(llm=palm_llm, memory=memory)    #, verbose=True)



### creating agent
tools = load_tools(tool_names=["google-search", "wikipedia"], llm = palm_llm)
agent = initialize_agent(
    tools,
    palm_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    # verbose = True,
    handle_parsing_errors=True,
    )



#query response using prompt template but without using memory
def llm_query_response(query: str):
    # print("\n\ncalling only llm\n\n")
    #using prompt template to create a prompt
    
    prompt = PromptTemplate(
        input_variables = ['query'],

        # template_question 1 = "Answer the following question by carefull understanding."

        # template_question 2 = "Understand the statement carefully.\
        #                     If it is a greeting then respond to that greeting by greeting back appropriately.\
        #                     If it is a question then answer the following question by carefull understanding."

        template = '''
                        Question: Understand the statement carefully.
                            If it is a question then answer the following question by carefull understanding.
                            If it contains multiple questions then answer all of them.
                            {query}
                        Answer: 
                '''
    )

    text = prompt.format(query=query)
    print(text,"\n\n")

    #using llmchain to pass a prompt to llm
    # chain = LLMChain(llm=llm, prompt = prompt)        #falcon llm
    chain = LLMChain(llm=palm_llm, prompt = prompt)     #, verbose=True)          #google palm
    
    try:
        response = chain.run(query).strip()
        response = re.sub(re.compile('<.*?>'), '', response)
        # print(response,'\n\n')

        result =  response
    
    except Exception as e:
        # print(f'\nproblem occured in Default mode in function llm_query_response: {str(e)}\n')
        if str(e) == "list index out of range":
            # print("working")
            result = "I didn't understand your question. Please type it correctly."
        else:
            # print("not working")
            result =  "Please accept our apology as something went wrong with the server. Please wait for a while or use Agents mode. If the problem persists please reload the page."
    
    return result



#query response without using prompt template but with memory with buffer
def llm_with_memory(query: str):

    # print("\n\n",convo.memory.buffer)

    try:
        result = convo.run(query)
    except Exception as e:
        # print(f'\nproblem occured in Default mode in function llm_with_memory: {str(e)}\n')
        if str(e) == "list index out of range":
            # print("working")
            result = "I didn't understand your question. Please type it correctly."
        else:
            # print("not working")
            result =  "Please accept our apology as something went wrong with the server. Please wait for a while or use Agents mode. If the problem persists please reload the page."
    
    return result



# query response using only agents without memory
# bcz i'm yet unable to figure out how to use memory with agents
def query_response_with_agents(query: str):
    # print("\n\ncalling llm with agents\n\n")
    try:
        result = agent.run(query)
    except Exception as e:
        # print(f'\nproblem occured in Agents mode in function query_response_with_agents: {str(e)}\n')
        if str(e) == "list index out of range":
            # print("working")
            result = "I didn't understand your question. Please type it correctly."
        else:
            # print("not working")
            result =  "Please accept our apology as something went wrong with the server. Please wait for a while or use Default mode. If the problem persists please reload the page."
    
    return result



if __name__ == "__main__":
    pass