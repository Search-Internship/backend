import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from utils.file_txt import parse_text_file

from fastapi import (
                    FastAPI, File, UploadFile, Form, status, HTTPException,APIRouter
                    )   
from src.exceptions import (
                            FileExtensionException,FileNotFoundException,
                            PasswordException,EmailException,EmailConnectionFailedException,
                            LinkException
                            )
from src.emails.main import (
                            send_email_smtp,check_gmail_connection
                            )
from utils.validity import (is_gmail_password_structure,is_valid_email,
                            is_valid_password,is_linkedin_profile_link)
import shutil
from pathlib import Path
from models.user import User








app = FastAPI()

# Create a router for API endpoints
api_router = APIRouter(prefix="/api")

@app.get("/")
def index():
    return {"messgae":"I am working good !"}

@app.post("/email/send-internship")
async def send_emails(emails: UploadFile = File(None), email_body: str = Form(...),
                      resume: UploadFile = File(None), sender_email: str = Form(...), 
                      sender_password: str = Form(...), email_subject: str = Form(...), 
                      file_separator: str = Form(...)):
    # Check if any of the files are null
    if emails is None:
        raise FileNotFoundException(detail="Emails TXT files are missing.")
    
    if resume is None:
        raise FileNotFoundException(detail="Resume PDF files are missing.")
    
    # Check if the emails file is a TXT file
    if not emails.filename.lower().endswith('.txt'):
        raise FileExtensionException(detail="The emails file must be a TXT file.")    
    
    # Check if the resume file is a PDF file
    if not resume.filename.lower().endswith('.pdf'):
        raise FileExtensionException(detail="The resume file must be a PDF file.")
    # Check if the password form is correct
    if not is_gmail_password_structure(sender_password):
        raise PasswordException(detail="The password form maybe like this : xxxx xxxx xxxx xxxx")
    # Check if the email form is correct
    if not is_valid_email(sender_email):
        raise EmailException(detail="The email form is incorrect")

    #Check the validity of email and password to connect to gmail
    if not check_gmail_connection(sender_email,sender_password):
        raise EmailConnectionFailedException("Failed to connect to gmail.")
    temp_dir = str(Path("./temp"))
    with open(f"{temp_dir}/emails.txt", "wb") as emails_file:
        shutil.copyfileobj(emails.file, emails_file)

    with open(f"{temp_dir}/resume.pdf", "wb") as resume_file:
        shutil.copyfileobj(resume.file, resume_file)
    
    # Proceed with processing if the files are of the correct types
    success_receiver:list = []
    failed_receiver:list = []
    # Use parse_text_file to parse the emails file with the specified separator
    emails_list:list = parse_text_file(f"{temp_dir}/emails.txt", file_separator)

    # Iterate over the parsed emails list and process each email address
    for email in emails_list:
        if send_email_smtp(sender_email,sender_password,email,email_subject,email_body,f"{temp_dir}/resume.pdf"):
            success_receiver.append(email)
        else:
            failed_receiver.append(email)

    os.remove(f"{temp_dir}/emails.txt")
    os.remove(f"{temp_dir}/resume.pdf")
    
    return {"success_receiver": success_receiver, "failed_receiver": failed_receiver},status.HTTP_200_OK

@app.post("/user/")
def create_user(
    username: str = Form(...),
    email: str = Form(...),
    linkedin_link: str = Form(None),
    password: str = Form(...),
    phone_number: str = Form(...),
    email_password: str = Form(...)
):
    try:
        # Check if email is valid
        if not is_valid_email(email):
            raise EmailException("Invalid email")

        # Check if email password has correct structure
        if not is_gmail_password_structure(email_password) and not email_password=="":
            raise PasswordException("Invalid email password structure")

        # Check if email password has correct structure
        if not is_valid_password(password):
            raise PasswordException("Invalid email password structure")
        
        # Check if linkdin link has correct structure
        if not is_linkedin_profile_link(linkedin_link) and not linkedin_link=="":
            raise LinkException("Invalid linkdin link structure")
        

        # Check Gmail connection
        if not check_gmail_connection():
            raise EmailConnectionFailedException("Failed to connect to email server")

        # Save user to database
        User.create_user(username, email, linkedin_link, password, phone_number, email_password)

        # Send confirmation email
        # send_email_smtp(email, "User Created", "Your account has been successfully created.")

        return {"message": "User created successfully"}
    except (EmailException, PasswordException, EmailConnectionFailedException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

















# Include the API router in the main app
app.include_router(api_router)