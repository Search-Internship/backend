import base64
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.

    Parameters:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: Extracted text from the PDF.

    Example:
        >>> extract_text_from_pdf('example.pdf')
        'This is an example PDF document.\nIt contains some text that we want to extract.\n...'
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        for page_number in range(num_pages):
            page = reader.pages[page_number]
            text += page.extract_text()
    return text

def encrypt_pdf_to_base64(pdf_path:str, password:str)->str:
    """
    Encrypts a PDF file using the provided password and returns its base64 encoded representation.

    Args:
        pdf_path (str): Path to the PDF file to be encrypted.
        password (str): Password to encrypt the PDF.

    Returns:
        str: Base64 encoded representation of the encrypted PDF.

    Raises:
        FileNotFoundError: If the PDF file specified by pdf_path does not exist.
        Exception: If an error occurs during PDF encryption.
    """
    # Read the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        
        # Create a PDF writer
        pdf_writer = PdfWriter()
        
        # Encrypt the PDF
        pdf_writer.append_pages_from_reader(pdf_reader)
        pdf_writer.encrypt(password)
        
        # Write the encrypted PDF to a BytesIO object
        encrypted_pdf_stream = BytesIO()
        pdf_writer.write(encrypted_pdf_stream)
        
        # Convert the BytesIO object content to base64
        encrypted_pdf_base64 = base64.b64encode(encrypted_pdf_stream.getvalue())
        
        return encrypted_pdf_base64.decode('utf-8')
    
def decrypt_pdf_from_base64(encrypted_pdf_base64:str, password:str):
    """
    Decrypts a PDF file encoded in base64 using the provided password and returns its content as bytes.

    Args:
        encrypted_pdf_base64 (str): Base64 encoded string of the encrypted PDF.
        password (str): Password used to decrypt the PDF.

    Returns:
        bytes: Decrypted PDF content.

    Raises:
        Exception: If the provided PDF is not encrypted or if an error occurs during decryption.
    """
    # Decode base64 string
    encrypted_pdf_bytes = base64.b64decode(encrypted_pdf_base64.encode('utf-8'))
    
    # Read the PDF from BytesIO object
    encrypted_pdf_stream = BytesIO(encrypted_pdf_bytes)
    
    # Create a PDF reader
    pdf_reader = PdfReader(encrypted_pdf_stream)
    
    # Check if the PDF is encrypted
    if pdf_reader.is_encrypted:
        # Decrypt the PDF
        pdf_reader.decrypt(password)
        
        # Create a PDF writer
        pdf_writer = PdfWriter()
        
        # Copy decrypted pages to PDF writer
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        
        # Write decrypted PDF to BytesIO object
        decrypted_pdf_stream = BytesIO()
        pdf_writer.write(decrypted_pdf_stream)
        
        # Get decrypted PDF content
        decrypted_pdf_content = decrypted_pdf_stream.getvalue()
        
        return decrypted_pdf_content
    
    else:
        raise Exception("PDF is not encrypted")

