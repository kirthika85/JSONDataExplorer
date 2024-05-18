import streamlit as st
import openai
import pandas as pd
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


st.title("JSON Data Explorer")
st.write("Parse and explore JSON data.")
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
if not openai_api_key.startswith('sk-'):
   st.warning('Please enter your OpenAI API key!', icon='⚠')
if openai_api_key.startswith('sk-'):
   json_input = st.text_area("Enter JSON data:")
   if st.button("Parse JSON"):
       if json_input:
          try:
             parsed_data = json.loads(json_input)
             if isinstance(parsed_data, list):
                 parsed_df=pd.DataFrame(parsed_data)
                 st.write("### Parsed JSON Data")
                 st.dataframe(parsed_df)
             elif isinstance(parsed_data, dict):
                 parsed_df=pd.DataFrame([parsed_data])
                 st.write("### Parsed JSON Data")
                 st.dataframe(parsed_df)
             else:
                 st.error("Invalid JSON data. Please check your input.")
          except json.JSONDecodeError:
                  st.error("Invalid JSON data. Please check your input.")       
       else:
           st.error("Please enter JSON data.")

   if st.button("Summarize JSON"):
       if json_input:
          llm=ChatOpenAI(api_key=openai_api_key,temperature=0.1,model_name="gpt-3.5-turbo")
          prompt=ChatPromptTemplate.from_template(f"Summarize the following JSON data:\n\n{json_input}")
          chain=prompt|llm
          response =response=chain.invoke()
          st.write("### JSON Summary")
          st.write(response.content)   
       else:
          st.error("Please enter JSON data.")

   if st.button("Query JSON"):
      query_input = st.text_input("Enter your query about the JSON data")
      if json_input and query_input:
           llm=ChatOpenAI(api_key=openai_api_key,temperature=0.1,model_name="gpt-3.5-turbo")
           prompt=ChatPromptTemplate.from_template(f"Query the following JSON data with: '{query_input}'\n\n{json_input}")
           chain=prompt|llm
           response =response=chain.invoke()
           st.write("### Query Result")
           st.write(response.content)
      else:
           st.error("Please enter both JSON data and your query.")
