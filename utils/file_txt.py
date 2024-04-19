

def parse_text_file(path: str, sep: str = '\n'):
    """
    Parse a text file containing email addresses separated by a specified separator.
    
    Args:
    - path (str): The path to the text file.
    - sep (str, optional): The separator used to separate email addresses in the file. Default is newline ('\n').
    
    Returns:
    - list: A list of email addresses parsed from the text file.
    """
    # Open the text file
    with open(path, 'r') as file:
        emails = []
        # Read each line in the file
        for line in file:
            # Remove leading and trailing whitespaces and split by the separator
            line_emails = [email.strip() for email in line.strip().split(sep)]
            # Add the parsed email addresses to the list
            emails.extend(line_emails)
    return emails
