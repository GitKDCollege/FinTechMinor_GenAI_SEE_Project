import streamlit as st
from io import StringIO
import backend

st.header("Welcome to Code-Analyser")
st.subheader("Upload any Code File to Analyse for Errors")

uploaded_file = st.file_uploader(label="Upload your Code File Here")

if uploaded_file:
    with st.spinner("Analysing ..."):
        file_object = uploaded_file.getvalue()
        file_content = StringIO(file_object.decode("utf-8")).read()

        generated_report = backend.process_single_file(file_content)

        st.write(generated_report)