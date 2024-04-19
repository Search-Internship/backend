from fastapi import FastAPI, File, UploadFile, Form
from exceptions import FileExtensionException,FileNotFoundException,PasswordException
from email.main import is_password_structure


app = FastAPI()

@app.post("/send/")
async def send_emails(emails: UploadFile = File(None), messages: UploadFile = File(None),
                      resume: UploadFile = File(None), sender_email: str = Form(...), 
                      sender_password: str = Form(...), email_subject: str = Form(...)):
    # Check if any of the files are null
    if emails is None:
        raise FileNotFoundException(detail="Emails TXT files are missing.")
    if messages is None:
        raise FileNotFoundException(detail="Message HTML files are missing.")
    if resume is None:
        raise FileNotFoundException(detail="Resume PDF files are missing.")
    
    # Check if the emails file is a TXT file
    if not emails.filename.lower().endswith('.txt'):
        raise FileExtensionException(detail="The emails file must be a TXT file.")
    
    # Check if the messages file is a HTML file
    if not messages.filename.lower().endswith('.html'):
        raise FileExtensionException(detail="The messages file must be a HTML file.")
        
    # Check if the resume file is a PDF file
    if not resume.filename.lower().endswith('.pdf'):
        raise FileExtensionException(detail="The resume file must be a PDF file.")
    
    # Check if the password form is correct
    if not is_password_structure(sender_password):
        raise PasswordException(detail="The password form maybe like this : xxxx xxxx xxxx xxxx")

    # Proceed with processing if the files are of the correct types
    emails_content = await emails.read()
    messages_content = await messages.read()
    resume_content = await resume.read()
    success_receiver = []
    
    # Process emails, messages, and resume here
    
    return {"emails_filename": emails.filename, "messages_filename": messages.filename, "resume_filename": resume.filename}
