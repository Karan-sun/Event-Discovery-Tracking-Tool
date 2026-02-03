import sys
import io
from pypdf import PdfReader

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file_path = r"c:\Users\parth\OneDrive\Desktop\Project\Full Stack Developer Intern – Assignment.pdf"

try:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    print(text)
except Exception as e:
    print(f"Error reading PDF: {e}")
