# # import streamlit as st
# # from pymongo.mongo_client import MongoClient
# # from pymongo.server_api import ServerApi
# from spacy.matcher import Matcher
# from tika import parser
# import spacy
# import re
# import nltk

# # Load the English NLP model
# nlp = spacy.load("en_core_web_sm")
# nltk.download('punkt')

# technical_skills = ['machine', 'data', 'python',
#                     'javascript', 'java', 'c', 'c++', 'html', 'css', 'react']
# with open('names.rtf', 'r') as file:
#     names_corpus = [name.lstrip('\\outl0\\strokewidth0 \\strokec2 ').rstrip(
#         '\\\n').lower() for name in file.readlines() if '\\\n' in name]
# names_corpus.remove('an')


# def extract_resume_data(file_path):
#     try:
#         parsed_document = parser.from_file(file_path)
#         resume_text = parsed_document['content'].strip()
#         return resume_text
#     except Exception as e:
#         print("Error:", str(e))
#         return None


# def extract_skills(text):
#     tokens = nltk.word_tokenize(text.lower())
#     extracted_skills = []
#     for skill in technical_skills:
#         if skill in tokens:
#             if skill == 'machine':
#                 extracted_skills.append(skill+' learning')
#             elif skill == 'data':
#                 extracted_skills.append(skill+' science')
#             else:
#                 extracted_skills.append(skill)

#     return extracted_skills


# def extract_name_and_email(text):
#     matcher = Matcher(nlp.vocab)
#     pattern1 = [
#         {"TEXT": {"REGEX": r"\+?\d{2}"}},
#         {"TEXT": {"REGEX": r"\d{5}"}},
#         {"TEXT": {"REGEX": r"\d{5}"}},
#     ]
#     pattern2 = [
#         {"TEXT": {"REGEX": r"\+?\d{0,2}"}},
#         {"TEXT": {"REGEX": r"\d{10}"}},
#     ]

#     matcher.add("PHONE_NUMBER", [pattern1, pattern2])

#     # Process the input string using spaCy
#     doc = nlp(text)

#     # Initialize variables to store name, number, and email
#     name = []
#     number = []
#     email = []
#     matches = matcher(doc)

#     for match_id, start, end in matches:
#         number.append(int(str(doc[start:end]).strip()))

#     for token in doc:
#         if token.like_email:
#             email.append(token)
#         if str(token).lower() in names_corpus:
#             if str(token).capitalize() in name:
#                 name.remove(str(token).capitalize())
#                 continue
#             name.append(str(token).capitalize())

#     return ' '.join(name), email, number


# def extract_branch(text):
#     branch = None

#     # Process the input string using spaCy
#     doc = nlp(text)

#     for ent in doc.ents:
#         if ent.label_ == "ORG":
#             branch = ent.text
#             break

#     return branch


# def extract_education_from_resume(text):
#     education = []

#     # Use regex pattern to find education information
#     pattern = r'\b(?:Ph\.?D\.?|M\.?S\.?|M\.?Sc\.?|M\.?A\.?|B\.?S\.?|B\.?A\.?|B\.?E\.?|B\.?Tech\.?|M\.?Tech\.?|Bachelor(?:\'s)?|Master(?:\'s)?|Doctorate|High School|GED)\b'
#     matches = re.findall(pattern, text)
#     for match in matches:
#         education.append(match.strip())

#     # Process the input string using spaCy
#     doc = nlp(text)

#     for ent in doc.ents:
#         if ent.label_ == "ORG":
#             if 'SCIENCE' in str(ent.text) and 'SCIENCE' != str(ent.text):
#                 education.append(ent.text)

#     return education

# # # Function to create or get the session state


# # class SessionState:
# #     def __init__(self, **kwargs):
# #         self.__dict__.update(kwargs)

# # # Function to get the session state


# # def get_session():
# #     return SessionState(user_authenticated=False, sign_up=False)

# # # Function to initialize MongoDB connection


# # def get_mongo_db():
# #     uri = "mongodb+srv://akshatkumar2001:h7Kkq4ECKvRcWmMA@personal.zuw99dp.mongodb.net/?retryWrites=true&w=majority"

# #     # Create a new client and connect to the server
# #     client = MongoClient(uri, server_api=ServerApi('1'))
# #     db = client.myDatabase
# #     my_collection = db["Credentials"]

# #     return my_collection

# # # Function to show the login page


# # def show_login_page(session_state, db):
# #     st.subheader("Sign In")

# #     username = st.text_input("Username")
# #     password = st.text_input("Password", type="password")

# #     if st.button("Sign In"):
# #         # Check credentials against MongoDB
# #         user = db.users.find_one({"username": username, "password": password})
# #         if user:
# #             session_state.user_authenticated = True
# #             st.success("Successfully signed in!")
# #         else:
# #             st.error("Invalid credentials. Please try again.")

# #     st.markdown("Don't have an account? [Sign Up](?page=signup)")

# # # Function to show the sign-up page


# # def show_signup_page(session_state, db):
# #     st.subheader("Sign Up")

# #     new_username = st.text_input("New Username")
# #     new_password = st.text_input("New Password", type="password")

# #     if st.button("Sign Up"):
# #         # Add sign-up logic to insert user into MongoDB
# #         user_data = {"username": new_username, "password": new_password}
# #         db.users.insert_one(user_data)
# #         st.success("Account created successfully! You can now sign in.")

# #     st.markdown("Already have an account? [Sign In](?page=login)")

# # # Function to show the authenticated page


# # def show_authenticated_page(session_state):
# #     st.sidebar.subheader("Navigation")
# #     page_options = ["Upload Resume", "Sign Out"]
# #     selected_page = st.sidebar.radio("Go to", page_options)

# #     if selected_page == "Upload Resume":
# #         st.subheader("Upload a Resume")

# #         # File upload widget
# #         uploaded_file = st.file_uploader(
# #             "Choose a file", type=["txt", "pdf"])

# #         # Display file details if a file is uploaded
# #         if uploaded_file is not None:
# #             file_details = {"FileName": uploaded_file.name,
# #                             "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
# #             st.write("### Uploaded File Details")
# #             st.write(file_details)

# #             # Display file content for text files
# #             if uploaded_file.type == "application/pdf":
# #                 st.write("### File Content")
# #                 # text_content = uploaded_file.read()
# #                 # st.code(text_content)

# #                 resume_text = extract_resume_data(uploaded_file)
# #                 resume_skills = extract_skills(resume_text)
# #                 education = extract_education_from_resume(resume_text)
# #                 name, email, number = extract_name_and_email(resume_text)
# #                 branch = ' '.join(extract_branch(resume_text).split())

# #                 if resume_text:
# #                     st.code(f'Resume skills: {resume_skills}')
# #                     st.code(
# #                         f'Name: {name}\n'f'Branch: {branch}\n'f'Email: {email[0]}\n'f'Number: {number[0]}\n'f'Education: {education}')

# #     elif selected_page == "Sign Out":
# #         st.subheader("Sign Out")
# #         if st.button("Confirm Sign Out"):
# #             session_state.user_authenticated = False
# #             st.success("Successfully signed out!")

# # # Main function to run the Streamlit app


# # def main():
# #     # Get the session state
# #     session_state = get_session()

# #     # Initialize MongoDB connection
# #     db = get_mongo_db()

# #     # Get the current page from the URL (using query parameters)
# #     current_page = st.experimental_get_query_params().get("page", ["login", "signup", "user"])[0]

# #     st.title("Streamlit Authentication Example")

# #     # Show the appropriate page based on the URL parameter
# #     if current_page == "user":
# #         show_authenticated_page(session_state)
# #     # Default to the login page if the URL parameter is not recognized
# #     if current_page == "login":
# #         show_login_page(session_state, db)
# #     if current_page == "signup":
# #         show_signup_page(session_state, db)


# # if __name__ == "__main__":
# #     main()


# def upload_file():
#     # if 'resumes' not in os.listdir():
#     #     os.mkdir('resumes')

#     file_path = "CV.pdf"

#     resume_text = extract_resume_data(file_path)
#     # resume_skills = extract_skills(resume_text)
#     # education = extract_education_from_resume(resume_text)
#     # name, email, number = extract_name_and_email(resume_text)
#     # branch = ' '.join(extract_branch(resume_text).split())

#     if resume_text:
#         # print(resume_text.split('SUMMER  INTERNSHIP  /  WORK  EXPERIENCE')[1].split('PROJECTS')[0].strip())
        
#         # return {"resume_skills": resume_skills, "name": name, "email":email, "number":number, "education":education, "branch":branch}
#         return resume_text
    
# if __name__ == '__main__':
#     print(upload_file())

# import PyPDF2


# def extract_pdf_text(pdf_path):
#     with open(pdf_path, 'rb') as file:
#         pdf_reader = PyPDF2.PdfReader(file)
#         text = ''

#         # Iterate through all pages in the PDF
#         for page_num in range(pdf_reader.numPages):
#             page = pdf_reader.getPage(page_num)
#             text += page.extractText()

#     return text


# def extract_pdf_metadata(pdf_path):
#     with open(pdf_path, 'rb') as file:
#         pdf_reader = PyPDF2.PdfReader(file)
#         metadata = pdf_reader.getDocumentInfo()

#     return metadata


# if __name__ == "__main__":
#     # Replace 'your_pdf_file.pdf' with the path to your PDF file
#     pdf_file_path = 'CV.pdf'

#     extracted_text = extract_pdf_text(pdf_file_path)
#     print("Extracted Text:")
#     print(extracted_text)

#     extracted_metadata = extract_pdf_metadata(pdf_file_path)
#     print("\nMetadata:")
#     for key, value in extracted_metadata.items():
#         print(f"{key}: {value}")

from spacy.matcher import Matcher
import fitz
import nltk
import re
import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")
nltk.download('punkt')

technical_skills = ['machine', 'data', 'python',
                    'javascript', 'java', 'c', 'c++', 'html', 'css', 'react']

with open('names.rtf', 'r') as file:
    names_corpus = [name.lstrip('\\outl0\\strokewidth0 \\strokec2 ').rstrip(
        '\\\n').lower() for name in file.readlines() if '\\\n' in name]
names_corpus.remove('an')

def extract_resume_data(file_path):
    text = ""
    try:
        with fitz.open(file_path) as pdf_document:
            num_pages = pdf_document.page_count
            for page_number in range(num_pages):
                page = pdf_document[page_number]
                text += page.get_text()
    except Exception as e:
        return e
    return text


def extract_skills(text):
    tokens = nltk.word_tokenize(text.lower())
    extracted_skills = []
    for skill in technical_skills:
        if skill in tokens:
            if skill == 'machine':
                extracted_skills.append(skill+' learning')
            elif skill == 'data':
                extracted_skills.append(skill+' science')
            else:
                extracted_skills.append(skill)

    return extracted_skills


def extract_name_and_email(text):
    matcher = Matcher(nlp.vocab)
    pattern1 = [
        {"TEXT": {"REGEX": r"\+?\d{2}"}},
        {"TEXT": {"REGEX": r"\d{5}"}},
        {"TEXT": {"REGEX": r"\d{5}"}},
    ]
    pattern2 = [
        {"TEXT": {"REGEX": r"\+?\d{0,2}"}},
        {"TEXT": {"REGEX": r"\d{10}"}},
    ]

    matcher.add("PHONE_NUMBER", [pattern1, pattern2])

    # Process the input string using spaCy
    doc = nlp(text)

    # Initialize variables to store name, number and email
    name = []
    number = []
    email = []
    matches = matcher(doc)

    for match_id, start, end in matches:
        number.append(int(str(doc[start:end]).strip().lstrip(': ')))

    for token in doc:
        if token.like_email:
            email.append(token)
        if str(token).lower() in names_corpus:
            if str(token).capitalize() in name:
                name.remove(str(token).capitalize())
                continue
            name.append(str(token).capitalize())

    return ' '.join(name), email, number


def extract_branch(text):
    branch = None

    # Process the input string using spaCy
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "ORG":
            branch = ent.text
            break

    return branch


def extract_education_from_resume(text):
    education = []

    # Use regex pattern to find education information
    pattern = r'\b(?:Ph\.?D\.?|M\.?S\.?|M\.?Sc\.?|M\.?A\.?|B\.?S\.?|B\.?A\.?|B\.?E\.?|B\.?Tech\.?|M\.?Tech\.?|Bachelor(?:\'s)?|Master(?:\'s)?|Doctorate|High School|GED)\b'
    matches = re.findall(pattern, text)
    for match in matches:
        education.append(match.strip())

    # Process the input string using spaCy
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "ORG":
            if 'SCIENCE' in str(ent.text) and 'SCIENCE' != str(ent.text):
                education.append(ent.text)

    return education

file_path = 'CV.pdf'

resume_text = extract_resume_data(file_path)
# resume_skills = extract_skills(resume_text)
# education = extract_education_from_resume(resume_text)
name, email, number = extract_name_and_email(resume_text)
# branch = ' '.join(extract_branch(resume_text).split())

print(name, email, number)