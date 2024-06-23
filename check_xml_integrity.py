import os
import xml.sax
import sys

# Function to count occurrences of a pattern in the XML file
def count_occurrences(pattern, filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read()
            return data.count(pattern)
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"Error reading {filename}: {e}")
    return 0

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
def check_xml_integrity(filename):
    handler = XMLHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)

    try:
        parser.parse(filename)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return False, False
    except Exception as e:
        print(f"Error parsing {filename}: {e}")
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
def check_mediawiki_end_tag(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            last_line = file.readlines()[-1]
            if "</mediawiki>" not in last_line:
                return False
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return False
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return False
    return True

# Main script logic
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_xml_integrity.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    xml_integrity_result = check_xml_integrity(filename)
    mediawiki_end_tag_result = check_mediawiki_end_tag(filename)

    if xml_integrity_result == (True, True) and mediawiki_end_tag_result:
        print(f"{filename}\nFile integrity is okay.")
    else:
        print(f"{filename}\nFile integrity is not okay.")