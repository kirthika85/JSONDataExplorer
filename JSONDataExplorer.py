import streamlit as st
import openai
import pandas as pd
import json

st.title("JSON Data Explorer")
st.write("Parse and explore JSON data.")
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
if not openai_api_key.startswith('sk-'):
   st.warning('Please enter your OpenAI API key!', icon='⚠')
if openai_api_key.startswith('sk-'):
   def parse_json(json_data):
      try:
          parsed_data = json.loads(json_data)
          if isinstance(parsed_data, list):
              return pd.DataFrame(parsed_data)
          elif isinstance(parsed_data, dict):
              return pd.DataFrame([parsed_data])
          else:
              return None
      except json.JSONDecodeError:
          return None
   def summarize_json(json_data):
      prompt = f"Summarize the following JSON data:\n\n{json_data}"
      response = openai.Completion.create(
              engine="text-davinci-003",
              prompt=prompt,
              max_tokens=150
      )
  




if st.button("Parse JSON"):
    if json_input:
        parsed_df = parse_json(json_input)
        if parsed_df is not None:
            st.write("### Parsed JSON Data")
            st.dataframe(parsed_df)
        else:
            st.error("Invalid JSON data. Please check your input.")
    else:
        st.error("Please enter JSON data.")

if st.button("Summarize JSON"):
    if json_input:
        summary = summarize_json(json_input)
        st.write("### JSON Summary")
        st.write(summary)
    else:
        st.error("Please enter JSON data.")

# Function to query JSON data
def query_json(json_data, query):
    prompt = f"Query the following JSON data with: '{query}'\n\n{json_data}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

query_input = st.text_input("Enter your query about the JSON data")

if st.button("Query JSON"):
    if json_input and query_input:
        query_result = query_json(json_input, query_input)
        st.write("### Query Result")
        st.write(query_result)
    else:
        st.error("Please enter both JSON data and your query.")
