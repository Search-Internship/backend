import os
import sys
import unittest

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from pathlib import Path
from utils.file_pdf import extract_text_from_pdf

class TestPDFTextExtraction(unittest.TestCase):

    def test_extract_text(self):
        expected_extracted_text="""Hello test pdf
1""".strip()
        # Provide a path to a sample PDF file
        pdf_path = str(Path("./tests/resource/test.pdf"))
        
        # Extract text from the sample PDF file
        extracted_text = extract_text_from_pdf(pdf_path)
        # Assert that the extracted text is not empty
        self.assertNotEqual(extracted_text, "")
        self.assertEqual(extracted_text, expected_extracted_text)
        
        # Add more assertions as needed to test specific aspects of the extracted text

if __name__ == '__main__':
    unittest.main()
