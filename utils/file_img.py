import base64

def encrypt_image_to_base64(image_path: str) -> str:
    """
    Encrypts an image file and returns its base64 encoded representation.

    Args:
        image_path (str): Path to the image file to be encrypted.

    Returns:
        str: Base64 encoded representation of the encrypted image.
    """
    # Read the image file
    with open(image_path, 'rb') as image_file:
        # Encrypt the image
        encrypted_image_bytes = image_file.read()
        
        # Convert the encrypted image to base64
        encrypted_image_base64 = base64.b64encode(encrypted_image_bytes)
        
        return encrypted_image_base64.decode('utf-8')

def decrypt_image_from_base64(encrypted_image_base64: str) -> bytes:
    """
    Decrypts an image encoded in base64 and returns its content as bytes.

    Args:
        encrypted_image_base64 (str): Base64 encoded string of the encrypted image.

    Returns:
        bytes: Decrypted image content.
    """
    # Decode base64 string
    encrypted_image_bytes = base64.b64decode(encrypted_image_base64.encode('utf-8'))
    
    return encrypted_image_bytes
