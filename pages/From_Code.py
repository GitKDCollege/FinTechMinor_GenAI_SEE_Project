import streamlit as st
import backend

st.header("Welcome to Code-Analyser")
st.subheader("Paste any Code here to Analyse for Errors")

entered_code = st.text_area("Paste your Code Here")

if st.button("Analyse"):
    with st.spinner("Analysing ..."):
        generated_report = backend.process_single_file(entered_code)
    st.write(generated_report)