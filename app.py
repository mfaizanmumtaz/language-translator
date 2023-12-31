import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"
os.environ["LANGCHAIN_PROJECT"]="Audo Evaluation"

from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI

model = ChatOpenAI(temperature=0,model="gpt-3.5-turbo-1106")

prompt = ChatPromptTemplate.from_messages(
    [
        ("user","""You are a helpful text translator assistant.
        Please translate the text that is enclosed within triple backticks (```) into {language}.
        Please do your best it is very important to my career.
        
        ------------

        > Text: ```{text}``` 
        """)
    ]
)

chain = prompt | model | StrOutputParser()

import streamlit as st

st.set_page_config("Language Translator", page_icon="💬")

st.title("Language Translator")

doc_file = st.sidebar.file_uploader("Upload PDF or Word Document",type=['pdf','docx'])

if doc_file is not None:

    with st.spinner("Extracting text Please wait..."):
        if "pdfs" not in os.listdir():
            os.mkdir("pdfs")
        try:
            file_path = os.path.join("pdfs",doc_file.name)
    
            with open(file_path,"wb") as f:
                f.write(doc_file.read())
    
            docs = PyPDFLoader(file_path).load()
            text = " ".join([doc.page_content for doc in docs])

        except Exception as e:
            st.write("There is some error",e)

        finally:
            os.remove(file_path)
    target_language = st.text_input("Enter target language:")

    if st.button("Translate") and target_language:

        with st.spinner("Translating Please wait..."):
            result = chain.invoke({"text":text,"language":target_language})
            st.markdown(result,unsafe_allow_html=True)

    else:
        st.warning("Please enter a target language to proceed with translation.")