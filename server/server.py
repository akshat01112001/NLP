from spacy.matcher import Matcher
from fastapi import FastAPI, HTTPException, UploadFile, Depends, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
import fitz
import jwt
import uvicorn
import os
import spacy
import re
import nltk
import json

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
        number.append(str(doc[start:end]).strip().lstrip(': '))

    for token in doc:
        if token.like_email:
            email.append(token.text)
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

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Secret key to sign JWT tokens
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# MongoDB connection settings
MONGO_URI = "mongodb+srv://akshatkumar2001:h7Kkq4ECKvRcWmMA@personal.zuw99dp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# OAuth2PasswordBearer for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class UserSignup(BaseModel):
    username: str
    password: str
    
class UserProfile(BaseModel):
    name: str
    email: str
    number: str
    username: str

# Function to create an access token


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get the current user based on the provided token

@app.post("/get_user")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    db = client.myDatabase["Credentials"]
    user = db.users.find_one({"username": username})
    if user is None:
        raise credentials_exception

    return payload

# Endpoint to get a token


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = client.myDatabase["Credentials"]
    user = db.users.find_one({"username": form_data.username})
    print(user)
    
    if user and user["password"] == form_data.password:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
# Endpoint to create a new user (sign-up)


@app.post("/signup")
async def signup(form_data: UserSignup):
    # Check if the username is already taken
    db = client.myDatabase["Credentials"]
    existing_user = db.users.find_one({"username": form_data.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Create a new user
    new_user = {"username": form_data.username, "password": form_data.password}
    db.users.insert_one(new_user)

    # Return a success message
    return {"message": "User registered successfully"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if 'resumes' not in os.listdir():
        os.mkdir('resumes')
    
    file_path = f'resumes/{file.filename}'
    
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
        
    resume_text = extract_resume_data(file_path)
    resume_skills = extract_skills(resume_text)
    education = extract_education_from_resume(resume_text)
    name, email, number = extract_name_and_email(resume_text)
    # branch = ' '.join(extract_branch(resume_text).split())

    if resume_text:
        # print(resume_text.split('SUMMER  INTERNSHIP  /  WORK  EXPERIENCE')[1].split('PROJECTS')[0].strip())
        return((
            {"resume_skills": resume_skills, 
             "name": name,
             "email": email, 
             "number": number, 
             "education": education,
            #  "branch": branch
             }))


@app.post("/profile")
async def profile(form_data: UserProfile):
    try:
        print(form_data)
        
        # Check if the username is already taken
        db = client.myDatabase["Profile"]

        # Using count_documents to check if the username exists
        existing_user_count = db.users.count_documents({"username": form_data.username})

        if existing_user_count > 0:
            # Update existing user
            filter_criteria = {"username": form_data.username}

            update_data = {
                '$set': {
                    "name": form_data.name,
                    "email": form_data.email,
                    "number": form_data.number
                }
            }
            
            result = db.users.update_one(filter_criteria, update_data)
            
        else:
            # Create a new user
            new_user = {
                "name": form_data.name,
                "email": form_data.email,
                "number": form_data.number,
                "username": form_data.username
            }

            result = db.users.insert_one(new_user)

            if result.inserted_id is None:
                raise HTTPException(status_code=500, detail="Failed to create profile")

        # Return a success message
        return {"message": "Profile updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run('server:app', port=8000, reload=True)
