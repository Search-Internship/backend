import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from utils.file_txt import parse_text_file

from fastapi import (
                    FastAPI, File, UploadFile, Form, status, HTTPException,APIRouter
                    )   
from exceptions.exceptions import (
                            FileExtensionException,FileNotFoundException,
                            PasswordException,EmailException,EmailConnectionFailedException,
                            LinkException,UserExistException
                            )
from src.emails.main import (
                            send_email_smtp,check_gmail_connection
                            )
from utils.validity import (is_gmail_password_structure,is_valid_email,
                            is_valid_password,is_linkedin_profile_link)
import shutil
from pathlib import Path
from models.user import User
from models.operations import Operations
from utils.jwt import (
                        create_access_token,decode_access_token
                      )
from utils.file_pdf import (
                            encrypt_pdf_to_base64,decrypt_pdf_from_base64
                            )
from utils.generate import generate_random_code
from dotenv import load_dotenv
from database import session


# Load variables from the specified .env file
load_dotenv(dotenv_path=str(Path("./env/secrets.env")))
load_dotenv(dotenv_path=str(Path("./env/communication.env")))
load_dotenv(dotenv_path=str(Path("./env/secrets.env")))

ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
FERNET_KEY:str=os.getenv("FERNET_KEY")
EMAIL_PROJECT:str=os.getenv("EMAIL_PROJECT")
PASSWORD_EMAIL_PROJECT:str=os.getenv("PASSWORD_EMAIL_PROJECT")
PDF_ENCRYPTION_SECRET:str=os.getenv("PDF_ENCRYPTION_SECRET")

app = FastAPI()

# Create a router for API endpoints
api_router = APIRouter(prefix="/api")

@api_router.get("/")
async def index():
    """
    Index endpoint to check if the server is running.
    """
    return {"messgae":"I am working good !"}

@api_router.post("/email/send-internship")
async def send_emails(emails: UploadFile = File(None), email_body: str = Form(...),
                      resume: UploadFile = File(None), sender_email: str = Form(...), 
                      sender_password: str = Form(...), email_subject: str = Form(...), 
                      file_separator: str = Form(...)):
    """
    Send internship emails with attachments.
    """
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
    
    return {"success_receiver": success_receiver, "failed_receiver": failed_receiver}

@api_router.post("/email/send-verification-code")
async def send_verification_email_code(to: str = Form(...),language:str = Form("fr")):
    """
    Send a verification code to the provided email address.
    """
    if not is_valid_email(to):
        raise EmailException(detail="The email form is incorrect")
    #Check the validity of email and password to connect to gmail
    if not check_gmail_connection(EMAIL_PROJECT,PASSWORD_EMAIL_PROJECT):
        raise EmailConnectionFailedException("Failed to connect to gmail.")
    code_generated:str=generate_random_code()
    email_subject:str="Verification code"
    email_body:str=f"<h1>Your code is {code_generated}</h1>"
    is_send:bool=send_email_smtp(
        sender_email=EMAIL_PROJECT,
        sender_password=PASSWORD_EMAIL_PROJECT,
        to=to,
        email_subject=email_subject,
        email_body=email_body
    )

    return {"code":(code_generated if is_send else "")}  
    



@api_router.post("/users/")
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    linkedin_link: str = Form(None),
    password: str = Form(...),
    phone_number: str = Form(...),
    email_password: str = Form(None)
):
    """
    Create a new user.
    """
    try:
        if linkedin_link is None:
            linkedin_link=''
        if email_password is None:
            email_password=''
        # Check if email is valid
        if not is_valid_email(email):
            raise EmailException("Invalid email")

        # Check if email password has correct structure
        if not is_gmail_password_structure(email_password) and email_password!='':
            raise PasswordException("Invalid email password structure")

        # Check if email password has correct structure
        if not is_valid_password(password):
            raise PasswordException("Invalid password structure")
        
        # Check if linkdin link has correct structure
        if not is_linkedin_profile_link(linkedin_link) and not linkedin_link=="":
            raise LinkException("Invalid linkdin link structure")
        

        # Save user to database
        is_created:bool=User.create_user(session,username, email, linkedin_link, password, phone_number, email_password,FERNET_KEY)
        if not is_created:
            raise UserExistException(f"User already exist with this email {email}")
        
        # Send confirmation email
        # send_email_smtp(email, "User Created", "Your account has been successfully created.")

        return {"message": "User created successfully"}
    except (EmailException, PasswordException, EmailConnectionFailedException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post("/users/login")
async def login(
    email: str = Form(...),
    password: str = Form(...)
):
    """
    User login.
    """
    # Verify login credentials
    is_valid_login, user_id = User.verify_login(session,email, password)
    
    if not is_valid_login:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    access_token = create_access_token(user_id,ACCESS_TOKEN_EXPIRE_MINUTES,JWT_SECRET_KEY,ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.post("/operations/")
async def create_operation(
    from_email: str = Form(...),
    pdf_base64: str = Form(...),
    email_body: str = Form(...),
    subject: str = Form(...),
    success_receiver: str = Form(...),
    failed_receiver: str = Form(...),
    user_id: str = Form(...)
):
    """
    Create a new operation associated with a user.
    """
    
    
    try:
        # Create the operation
        operation = Operations.create_operation(
            session,
            from_email=from_email,
            pdf_base64=pdf_base64,
            email_body=email_body,
            subject=subject,
            success_receiver=success_receiver,
            failed_receiver=failed_receiver,
            user_id=user_id
        )
        return {"message": "Operation created successfully"}
    except ValueError as ve:
        raise UserExistException(detail="User does not exist with the provided user id")
    


# Include the API router in the main app
app.include_router(api_router)