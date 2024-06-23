import os
import xml.sax
import sys

# Function to read file content and handle errors
def read_file_content(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"Error reading {filename}: {e}")
    return []

# Function to count occurrences of a pattern in the file content
def count_occurrences(pattern, file_content):
    data = "".join(file_content)
    return data.count(pattern)

# SAX ContentHandler to parse XML and count specific elements
class XMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        super().__init__()
        self.count_title = 0
        self.count_page = 0
        self.count_page_close = 0
        self.count_revision = 0
        self.count_revision_close = 0

    def startElement(self, name, attrs):
        if name == "title":
            self.count_title += 1
        elif name == "page":
            self.count_page += 1
        elif name == "revision":
            self.count_revision += 1

    def endElement(self, name):
        if name == "page":
            self.count_page_close += 1
        elif name == "revision":
            self.count_revision_close += 1

# Function to check XML integrity conditions
def check_xml_integrity(file_content):
    handler = XMLHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)

    try:
        parser.parse(file_content)
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return False, False

    # Check conditions for the first three patterns
    first_three_conditions = (
        handler.count_title == handler.count_page == handler.count_page_close and
        handler.count_title > 0
    )

    # Check conditions for the last two patterns
    last_two_conditions = (
        handler.count_revision == handler.count_revision_close and handler.count_revision > 0
    )

    return first_three_conditions, last_two_conditions

# Function to check </mediawiki> tag at the end of the XML file
def check_mediawiki_end_tag(file_content):
    last_line = file_content[-1].strip() if file_content else ""
    if "</mediawiki>" not in last_line:
        return False
    return True

# Main script logic
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_xml_integrity.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    file_content = read_file_content(filename)

    if not file_content:
        print(f"{filename}\nFile reading failed or empty.")
        sys.exit(1)

    xml_integrity_result = check_xml_integrity(file_content)
    mediawiki_end_tag_result = check_mediawiki_end_tag(file_content)

    if xml_integrity_result == (True, True) and mediawiki_end_tag_result:
        print(f"{filename}\nFile integrity is okay.")
    else:
        print(f"{filename}\nFile integrity is not okay.")
