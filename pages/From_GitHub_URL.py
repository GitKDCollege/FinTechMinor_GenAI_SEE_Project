import streamlit as st
import os
import backend

if 'clicked' not in st.session_state:
    st.session_state.clicked=False

st.header("Welcome to Code-Analyser")
st.subheader("Enter URL of GitHub Repository to analyse for Errors")

st.write("Enter Repository URL in the Format")
st.write("https://github.com/username/reponame")
url = st.text_input('')

if(url):
    uname_and_reponame = backend.get_username_and_repo_from_url(url)
    # reports_dir = f"""D:/ACADEMICS/SEM4/FINTECH_MINOR/GenAI_Prompt_Engineering/Mini_Project_and_SEE/reports_generated/{uname_and_reponame}"""
    reports_dir = f"""reports_generated/{uname_and_reponame}"""

def generate_report():
    if st.button("Generate Report"):
        st.session_state.clicked=True
        if url:
            with st.spinner('Generating Report...'):
                try:
                    files = backend.process_url(url)
                    st.success("Report Generated Successfully")
                    st.write(f"""Report saved in: ../reports_generated/{uname_and_reponame}""")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

def get_all_files(root,files=None):
    if(files==None):
        files=[]
    items = os.listdir(root)
    for item in items:
        if(os.path.isdir(f"{root}/{item}")):
            get_all_files(f"{root}/{item}",files)
        else:
            files.append(f"{root}/{item}")
    # return [("/").join(file.split("/")[9:]) for file in files]
    return [("/").join(file.split("/")[3:]) for file in files]
try:
    if(os.path.exists(reports_dir)):
        st.session_state.clicked=True
        st.write(f"Reports Already Available for {uname_and_reponame}")
    else:
            generate_report()
except:
    pass

if(st.session_state.clicked):
    reports_list = get_all_files(reports_dir)
    report_file = st.selectbox("Select desired report to View:", reports_list)
    if report_file:
        with open(f"{reports_dir}/{report_file}", 'r', encoding='utf-8') as f:
            report_content = f.read()
            st.markdown(report_content, unsafe_allow_html=True)
