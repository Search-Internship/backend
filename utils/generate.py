import random
import string

def generate_random_code(length: int = 4, type_: str = "number") -> str:
    """
    Generate a random code of specified length and type.

    Parameters:
        length (int): Length of the code to be generated. Default is 4.
        type_ (str): Type of characters to include in the code.
            - 'number': Only digits (0-9).
            - 'string': Only uppercase letters (A-Z).
            - 'mixte': Both digits and uppercase letters.

    Returns:
        str: Generated random code.

    Example:
        >>> generate_random_code() # Generates a 6-character code with numbers
        '123456'
        >>> generate_random_code(8, 'mixte') # Generates an 8-character code with numbers and letters
        'A1B2C3D4'
    """
    characters = ""
    if type_ == "number":
        characters = string.digits
    elif type_ == "string":
        characters = string.ascii_uppercase
    elif type_ == "mixte":
        characters = string.digits + string.ascii_uppercase
    
    code = ''.join(random.choice(characters) for _ in range(length))
    return code
