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

   def flatten_json(data, prefix=''):
       if isinstance(data, dict):
           flattened_data = {}
           for key, value in data.items():
               if isinstance(value, (dict, list)):
                   flattened_data.update(flatten_json(value, prefix + key + '_'))
               else:
                   flattened_data[prefix + key] = value
           return flattened_data
       elif isinstance(data, list):
           flattened_data = {}
           for i, item in enumerate(data):
               if isinstance(item, dict):
                   flattened_item = flatten_json(item, prefix)
                   flattened_data.append(flattened_item)
           return flattened_data
       else:
           return {prefix[:-1]: data}
       
   if st.button("Parse JSON"):
       if json_input:
          try:
             parsed_data = json.loads(json_input)
             if isinstance(parsed_data, dict) or isinstance(parsed_data, list):
                flattened_data = flatten_json(parsed_data)
                if isinstance(flattened_data, dict):
                   df = pd.DataFrame([flattened_data])
                elif isinstance(parsed_data, dict):
                    df = pd.DataFrame([flattened_data])
                else:
                    st.error("Invalid JSON data. Please check your input.")
                    st.stop()
                orders_df = pd.DataFrame(df.pop('orders').explode().tolist())
                df = pd.concat([df.reset_index(drop=True), orders_df.reset_index(drop=True)], axis=1)
                st.write("### Parsed JSON Data")
                st.dataframe(df)
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
