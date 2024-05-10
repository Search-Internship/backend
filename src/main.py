import os
import sys
import uuid
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

from models import Operations,User
from utils.jwt import (
                        create_access_token,decode_access_token
                      )
from utils.file_pdf import (
                            encrypt_pdf_to_base64,decrypt_pdf_from_base64
                            )
from utils.file_img import (
                            encrypt_image_to_base64,decrypt_image_from_base64
                             )
from utils.generate import generate_random_code
from dotenv import load_dotenv
from database import session
from chat.main import get_possible_job_titles,get_email_body


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
async def send_emails(access_token:str= Form(None),emails: UploadFile = File(None), email_body: str = Form(...),
                      resume: UploadFile = File(None), email_subject: str = Form(...), 
                      file_separator: str = Form(...)):
    """
    Send internship emails with attachments.
    """
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY,ALGORITHM)
    if not decode_token["valid"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user_id:str=decode_token["user_id"]
    user:User|None=User.get_user_by_id(session,user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    sender_email:str=user.email
    sender_password:str=user.get_email_password(encryption_key=FERNET_KEY)
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
    temp_dir:str = str(Path("./temp"))
    resume_dir:str = str(Path("./data/resume"))
    data_dir:str = str(Path("./data"))
    # Check if data directory exists, if not, create it
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Check if resume directory exists within data directory, if not, create it
    if not os.path.exists(resume_dir):
        os.makedirs(resume_dir)
    
    # Check if temp_dir exists, if not, create it
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)


    pdf_id:str = str(uuid.uuid4())
    with open(f"{temp_dir}/emails.txt", "wb") as emails_file:
        shutil.copyfileobj(emails.file, emails_file)

    with open(f"{resume_dir}/{pdf_id}.pdf", "wb") as resume_file:
        shutil.copyfileobj(resume.file, resume_file)
    
    # Proceed with processing if the files are of the correct types
    success_receiver:list = []
    failed_receiver:list = []
    # Use parse_text_file to parse the emails file with the specified separator
    emails_list:list = parse_text_file(f"{temp_dir}/emails.txt", file_separator)

    # Iterate over the parsed emails list and process each email address
    for email in emails_list:
        if send_email_smtp(sender_email,sender_password,email,email_subject,email_body,f"{resume_dir}/{pdf_id}.pdf",resume.filename):
            success_receiver.append(email)
        else:
            failed_receiver.append(email)
    try:
        is_saved_operations:bool=Operations.create_operation(session,sender_email,email_body,email_subject,",".join(success_receiver),",".join(failed_receiver),pdf_id,user_id)
    except ValueError as ve:
        raise UserExistException(detail="User does not exist with the provided user id")
    os.remove(f"{temp_dir}/emails.txt")

    if is_saved_operations:
        return {"success_receiver": success_receiver, "failed_receiver": failed_receiver,"saved":is_saved_operations}
    return {"success_receiver": success_receiver, "failed_receiver": failed_receiver,"saved":False}












@api_router.post("/email/send-verification-code")
async def send_verification_email_code(to: str = Form(...),language:str = Form("fr"),length:int=Form(4),type_:str=Form("number")):
    """
    Send a verification code to the provided email address.
    """
    if not is_valid_email(to):
        raise EmailException(detail="The email form is incorrect")
    #Check the validity of email and password to connect to gmail
    if not check_gmail_connection(EMAIL_PROJECT,PASSWORD_EMAIL_PROJECT):
        raise EmailConnectionFailedException("Failed to connect to gmail.")
    code_generated:str=generate_random_code(length,type_)
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
    

@api_router.post("/users/email-exist")
async def check_email_exist(email: str = Form(...)):
    """
    Check if an email exists.
    """
    if not is_valid_email(email):
        raise EmailException(detail="The email form is incorrect")
    user:User|None=User.get_user_by_email(session,email)
    if user:
        access_token = create_access_token(user.id,ACCESS_TOKEN_EXPIRE_MINUTES,JWT_SECRET_KEY,ALGORITHM)
        return {"exist":True,"access_token":access_token}
    return {"exist":False,"access_token":""}


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
        
        # Check if linkdin link has correct strutxtcture
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

@api_router.put("/users/change-password")
def change_password(
    new_password: str= Form(...),
    access_token: str= Form(...)
    ):
    # Get the user from the database
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY,ALGORITHM)
    if not decode_token["valid"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user_id:str=decode_token["user_id"]
    user:User|None=User.get_user_by_id(session,user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    # Check if email password has correct structure
    if not is_valid_password(new_password):
        raise PasswordException("Invalid password structure")
    # Set the new password
    user.set_password(new_password)
    session.commit()
    
    # Update the user in the database    
    return {"message": "Password changed successfully"}

"""
@api_router.put("/users/forgot-password")
def forgot_password(
    new_password: str= Form(...),
    email: str= Form(...)
    ):
    user:User|None=User.get_user_by_email(session,email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    # Check if email password has correct structure
    if not is_valid_password(new_password):
        raise PasswordException("Invalid password structure")
    # Set the new password
    user.set_password(new_password)
    session.commit()
    
    # Update the user in the database    
    return {"message": "Password changed successfully"}
"""
@api_router.post("/operations/")
async def create_operation(
    email_body: str = Form(...),
    subject: str = Form(...),
    success_receiver: str = Form(...),
    failed_receiver: str = Form(...),
    access_token: str = Form(...)
):
    """
    Create a new operation associated with a user.
    """
    
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY,ALGORITHM)
    if not decode_token["valid"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user_id:str=decode_token["user_id"]
    user:User|None=User.get_user_by_id(session,user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    from_email:str=user.email
    try:
        # Create the operation
        operation = Operations.create_operation(
            session,
            from_email=from_email,
            email_body=email_body,
            subject=subject,
            success_receiver=success_receiver,
            failed_receiver=failed_receiver,
            user_id=user_id
        )
        return {"message": "Operation created successfully"}
    except ValueError as ve:
        raise UserExistException(detail="User does not exist with the provided user id")
    

@api_router.get("/operations/{access_token}/{operation_id}/")
async def get_operation(access_token:str,operation_id: str):
    """
    Get an operation by operation ID.
    """
    print("/operations/{access_token}/{operation_id}/")
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY,ALGORITHM)
    if not decode_token["valid"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user_id:str=decode_token["user_id"]
    user:User|None=User.get_user_by_id(session,user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    try:
        operation = Operations.get_operation_by_id(session, operation_id, user_id)
    except ValueError as ve:
        raise UserExistException(detail="User does not exist with the provided user id")
    return {"data": operation}  


@api_router.get("/operations/{access_token}/")
async def get_operation_user(access_token:str):
    """
    Get an operation by access_token(user ID).
    """
    print("/operations/{access_token}/")
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY,ALGORITHM)
    if not decode_token["valid"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user_id:str=decode_token["user_id"]
    user:User|None=User.get_user_by_id(session,user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    try:
        operations_info:list = Operations.get_operations_info(session, user_id)
    except ValueError as ve:
        raise UserExistException(detail="User does not exist with the provided user id")
    return {"data":operations_info}




@api_router.post("/chat/possible-job-titles")
async def get_possible_job_titles_(resume: UploadFile = File(None)):
    """
    Send internship emails with attachments.
    """
    
    if resume is None:
        raise FileNotFoundException(detail="Resume PDF files are missing.")
    
    # Check if the resume file is a PDF file
    if not resume.filename.lower().endswith('.pdf'):
        raise FileExtensionException(detail="The resume file must be a PDF file.")

    temp_dir = str(Path("./temp"))
    resume_dir = str(Path("./temp/resume"))

    # Check if resume directory exists within data directory, if not, create it
    if not os.path.exists(resume_dir):
        os.makedirs(resume_dir)
    
    # Check if temp_dir exists, if not, create it
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    pdf_id = str(uuid.uuid4())
    resume_pdf = f"{resume_dir}/{pdf_id}.pdf"
    
    with open(resume_pdf, "wb") as resume_file:
        shutil.copyfileobj(resume.file, resume_file)
    
    # Await the asynchronous function
    possible_job_titles = get_possible_job_titles(resume_pdf)

    os.remove(resume_pdf)
    return {"possible_job_titles": possible_job_titles}

    


@api_router.post("/chat/generated-email-body")
async def get_email_body_(resume: UploadFile = File(None),langauage:str=Form("English"),email_subject:str=Form(...)):
    """
    Send internship emails with attachments.
    """
    
    if resume is None:
        raise FileNotFoundException(detail="Resume PDF files are missing.")
    
    
    # Check if the resume file is a PDF file
    if not resume.filename.lower().endswith('.pdf'):
        raise FileExtensionException(detail="The resume file must be a PDF file.")

    temp_dir:str = str(Path("./temp"))
    resume_dir:str = str(Path("./temp/resume"))


    # Check if resume directory exists within data directory, if not, create it
    if not os.path.exists(resume_dir):
        os.makedirs(resume_dir)
    
    # Check if temp_dir exists, if not, create it
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    pdf_id:str = str(uuid.uuid4())
    resume_pdf:str=f"{resume_dir}/{pdf_id}.pdf"
    with open(resume_pdf, "wb") as resume_file:
        shutil.copyfileobj(resume.file, resume_file)
    
    email_body= get_email_body(resume_pdf,email_subject,langauage)

    
    os.remove(resume_pdf)
    return {"email_body": email_body}









# Include the API router in the main app
app.include_router(api_router)