import PyPDF2

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
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_number in range(num_pages):
            page = reader.pages[page_number]
            text += page.extract_text()
    return text