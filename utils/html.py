from html.parser import HTMLParser

class SyntaxChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.error_flag = False

    def handle_data(self, data):
        pass

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_startendtag(self, tag, attrs):
        pass

    def error(self, message):
        self.error_flag = True

def check_html_syntax(html_file):
    # Initialize the SyntaxChecker
    syntax_checker = SyntaxChecker()

    # Open the HTML file for reading
    with open(html_file, 'r', encoding='utf-8') as file:
        # Parse the HTML content
        syntax_checker.feed(file.read())

    # Check if any syntax error occurred
    return not syntax_checker.error_flag