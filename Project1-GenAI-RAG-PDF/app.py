import streamlit as st
import tempfile
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

st.set_page_config(page_title="PDF Analyzer", page_icon="🤖")
st.title("PDF Analyzer Via Groq")
st.markdown("Upload a PDF and ask questions about it.")

groq_api_key = st.sidebar.text_input(
    "Enter your Groq API Key",
    type="password",
    placeholder="gsk..."
)

model_name = st.sidebar.selectbox(
    "Select a model",
    options=[
    "llama3-8b-8192",
    "llama-3.1-8b-instant"
],
    index=0
)

uploaded_file = st.file_uploader("Upload a PDF file...", type=["pdf"])

if uploaded_file:
    pdf_path = None

    try:
        with st.spinner("Processing PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                pdf_path = tmp_file.name

            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=512,
                chunk_overlap=100
            )
            chunks = splitter.split_documents(documents)

            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True}
            )

            vectorstore = FAISS.from_documents(
                documents=chunks,
                embedding=embeddings
            )

            llm = ChatGroq(
                api_key=groq_api_key,
                model_name=model_name,
                temperature=0
            )

            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever(),
                return_source_documents=True
            )

        st.success("PDF processed successfully!")

        query = st.text_input("Ask me anything about the PDF")

        if query:
            try:
                with st.spinner("Processing your query..."):
                    result = qa_chain.invoke({"query": query})

                st.subheader("Answer")
                st.write(result["result"])

                st.subheader("Source Chunks")
                for i, doc in enumerate(result["source_documents"]):
                    st.write(f"Chunk {i + 1}")
                    st.write(doc.page_content)
                    st.write("---")

            except Exception as e:
                st.error(f"Query Error: {str(e)}")

    except Exception as e:
        st.error(f"Processing Error: {str(e)}")

    finally:
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)
