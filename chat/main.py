import os
import sys
import uuid
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
import re



load_dotenv(str(Path("./env/chat.env")))
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
MODEL_NAME=os.getenv("MODEL_NAME")
PROJECT_NAME=os.getenv("PROJECT_NAME")

def get_pages_contents_from_pdf(resume_pdf_path:str)->str:
    """
    Extracts the content of all pages from a PDF file.

    Args:
        resume_pdf_path (str): The path to the PDF file.

    Returns:
        str: The concatenated content of all pages in the PDF.

    Example:
        >>> get_pages_contents_from_pdf("./resume.pdf")
        'Page 1 content\nPage 2 content\n...'
    """
    loader = PyPDFLoader(resume_pdf_path)
    documents=loader.load()
    page_contents:str=""
    for document in documents:
        page_contents+=dict(document)["page_content"]+"\n"
    return page_contents

def get_possible_job_titles(resume_pdf_path: str) -> list:
    """
    Extracts possible job titles from a resume PDF.

    Args:
        resume_pdf_path (str): The path to the PDF file.

    Returns:
        list: A list of possible job titles extracted from the resume.

    Example:
        >>> get_possible_job_titles("./resume.pdf")
        ['Software Engineer', 'Data Analyst', ...]
    """
    page_contents = get_pages_contents_from_pdf(resume_pdf_path)
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME, google_api_key=GEMINI_API_KEY, project=PROJECT_NAME
    )
    result = llm.invoke(f"Extract possible job titles from this resume en list dashe : {page_contents}")
    return extract_list_from_string(result.content)


def extract_list_from_string(result:str)->list:
    """
    Extracts a list from a string based on a specific pattern.

    Args:
        result (str): The string to extract the list from.

    Returns:
        list: The extracted list.

    Example:
        >>> extract_list_from_string("- Item 1\n- Item 2\n- Item 3\n")
        ['Item 1', 'Item 2', 'Item 3']
    """
    # Define the regex pattern to match the list items
    pattern = r"- (.+)"
    
    # Find all matches using the pattern
    matches = re.findall(pattern, result)
    
    return matches

def get_email_body(resume_pdf_path:str,email_subject:str,language:str)->list:
    """
    Generates an email body in markdown language from a resume PDF.

    Args:
        resume_pdf_path (str): The path to the PDF file.
        email_subject (str): The subject of the email.
        language (str): The language for generating the email body.

    Returns:
        list: The generated email body.

    Example:
        >>> get_email_body("./resume.pdf", "Job Application", "English")
        'Dear Hiring Manager, ...'
    """
    page_contents=get_pages_contents_from_pdf(resume_pdf_path)
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME,google_api_key=GEMINI_API_KEY,project=PROJECT_NAME)
    result = llm.invoke(f"Generate an email body with this spe")

    return remove_markdown(result.content)



def remove_markdown(text):
    """
    Removes markdown formatting from text.

    Args:
        text (str): The text containing markdown formatting.

    Returns:
        str: The text with markdown formatting removed.

    Example:
        >>> remove_markdown("**Hello** *world*")
        'Hello world'
    """
    if text.startswith("```markdown\n") and text.endswith("```"):
        return text[len("```markdown\n") : -len("```")]
    return text