
# Module Imports
import os
from dotenv import load_dotenv
import base64
import streamlit as st
from github import Github,Auth
import google.generativeai as genai

load_dotenv()

def create_get_gemini_model():
    genai.configure(api_key=os.getenv('GOOGLE_GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    return model

def create_get_github_object():
    g = Github(auth=Auth.Token(os.getenv('GITHUB_ACCESS_TOKEN')))
    return g

def get_username_and_repo_from_url(url):
    starting = 'https://github.com/'
    try:
        if url.startswith(starting):
            return url[len(starting):].strip("/")
    except:
        pass

def create_get_repository_object(github_object,repo_url):
    uname_and_reponame = get_username_and_repo_from_url(repo_url)
    repo_object = github_object.get_repo(uname_and_reponame)
    return repo_object

def load_prompt(file_path='./prompt1.txt'):
    with open(file_path,'r') as f:
        prompt=f.read()
    return prompt

def decode_bytes_to_str(byte_data):
    decoded = base64.b64decode(byte_data)
    return decoded

def get_file_content_from_repo(repo_object,file_name):
    encoded_file_content = repo_object.get_contents(file_name).content
    decoded_file_content = decode_bytes_to_str(encoded_file_content)
    return decoded_file_content

def convert_to_md(file_name):
    return f"""{file_name.replace(".","_")}_report.md"""

def write_file(uname_and_reponame,file_path,file_content):
    with open(f"""./reports_generated/{uname_and_reponame}/{file_path}""",'w',encoding='utf-8') as f:
        f.write(file_content)

def get_report_from_gemini(model,file_content,prompt_path='./prompt1.txt'):
    prompt=load_prompt(prompt_path)
    report = model.generate_content(f"""{prompt}/n{file_content}""")
    buffer=""""""
    for part in report.parts:
        buffer+=part.text
    return buffer

dirs_to_ignore=['node_modules','.github','__pycache__','.idea']
files_to_ignore=['LICENSE','.gitignore','.git','.gitattributes','.env','.bat','.sh','.ico']
extensions_to_ignore=['md','txt','pptx','docx','xlsx','csv','db','sqlite','yaml','abi','bin','json','onnx','jpg','png','jpeg']

def store_report_in_local_directory(uname_and_reponame,repo_object,gemini_model):
    contents= repo_object.get_contents("")
    while contents:
        item = contents.pop(0)
        if (item.type == "dir" and item.name not in dirs_to_ignore):
            if not os.path.exists(f"""./reports_generated/{uname_and_reponame}/{item.path}"""):
                os.mkdir(f"""./reports_generated/{uname_and_reponame}/{item.path}""")
            contents.extend(repo_object.get_contents(item.path))
        elif (item.type=="file" and item.name not in files_to_ignore and item.name.split(".")[-1] not in extensions_to_ignore):
            file_content = get_file_content_from_repo(repo_object,item.path)
            generated_report = get_report_from_gemini(gemini_model,file_content)
            write_file(uname_and_reponame,convert_to_md(item.path),generated_report)

def process_url(url):

    print("-"*80);print("Process Started ...\n")
    github_object   = create_get_github_object()
    repo_url        = url
    repo_object     = create_get_repository_object(github_object,repo_url)
    gemini_model    = create_get_gemini_model()

    uname_and_reponame = get_username_and_repo_from_url(repo_url)

    if not os.path.exists(f"""./reports_generated/{uname_and_reponame.split("/")[0]}"""):
        os.mkdir(f"""./reports_generated/{uname_and_reponame.split("/")[0]}""")
    if not os.path.exists(f"""./reports_generated/{uname_and_reponame.split("/")[0]}/{uname_and_reponame.split("/")[1]}"""):
        os.mkdir(f"""./reports_generated/{uname_and_reponame.split("/")[0]}/{uname_and_reponame.split("/")[1]}""")

    print("Extracting Information from Repository ...\n")
    store_report_in_local_directory(uname_and_reponame,repo_object,gemini_model)

    print(f"""Process Complete.\nReport Generated Successfully, stored in "./reports_generated/{uname_and_reponame}" """)
    print("-"*80)

def process_single_file(file_content):
    gemini_model    = create_get_gemini_model()
    report          = get_report_from_gemini(gemini_model,file_content,prompt_path='./prompt2.txt')
    return report


if __name__=="__main__":
    url = input("""Enter the Github Repository URL\nFormat : "https://github.com/<username>/<repository_name>"\n: """).strip()
    process_url(url)
