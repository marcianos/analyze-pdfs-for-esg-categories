import json
import os
import sys
import spacy
import spacy.cli
from fitz import open as open_pdf
from collections import Counter
from spacy.matcher import PhraseMatcher
import csv

# Configuration embedded into the script
CONFIGS = {
    "csv_directory": "categories",  # Default relative directory for CSV files
    "pdf_directory": "Nachhaltigkeitsberichte",  # Default relative directory for PDF files
    "output_directory": "analysisOfWordFrequencies",
    "language_model": "en_core_web_sm",  # Default SpaCy language model
}

# def get_base_dir():
#     """Get the base directory dynamically for PyInstaller or script mode."""
#     if getattr(sys, "frozen", False):  # If running as a bundled executable
#         return sys._MEIPASS
#     return os.path.dirname(os.path.abspath(__file__))

# def get_directory(key):
#     """Get the specified directory path from CONFIGS."""
#     base_dir = get_base_dir()  # Always base it on the script or executable's directory
#     return os.path.join(base_dir, CONFIGS[key])

def get_directory(key):
    """Get the specified directory path from CONFIGS."""
    if getattr(sys, "frozen", False):  # If running as a bundled executable
        base_dir = os.path.dirname(sys.executable)  # Directory of the executable
        project_dir = os.path.abspath(os.path.join(base_dir, ".."))  # Parent directory of dist
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
        project_dir = base_dir  # Script directory is the project directory
    if key == "output_directory":
        return os.path.join(project_dir, CONFIGS[key])  # Output in project directory
    return os.path.join(project_dir, CONFIGS[key])  # Input folders in project directory

def get_base_dir():
    """Get the base directory dynamically for PyInstaller or script mode."""
    if getattr(sys, "frozen", False):  # If running as a bundled executable
        print(f"Base directory (executable): {os.path.dirname(sys.executable)}")
        return os.path.dirname(sys.executable)
    print(f"Base directory (script): {os.path.dirname(os.path.abspath(__file__))}")
    return os.path.dirname(os.path.abspath(__file__))

def load_word_lists(category_files):
    """Load multiple word lists for different categories."""
    categories = {}
    for category_name, filepath in category_files.items():
        word_list = {}
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            word_list = {row[0].strip(): row[1].strip() for row in reader}
        categories[category_name] = word_list
    return categories


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with open_pdf(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text


def analyze_word_frequency_by_category(text, categories, nlp, chunk_size=500000):
    """Analyze word frequencies for different categories in a text."""
    matchers = {}
    for category_name, word_list in categories.items():
        matcher = PhraseMatcher(nlp.vocab)
        patterns = [nlp.make_doc(word) for word in word_list.keys()]
        matcher.add(category_name, patterns)
        matchers[category_name] = matcher

    category_counts = {key: 0 for key in categories.keys()}
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        doc = nlp(chunk.lower())

        for category_name, matcher in matchers.items():
            matches = matcher(doc)
            category_counts[category_name] += len(matches)

    return category_counts


def main():
    print("Current working directory:", os.getcwd())
    script_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(script_dir, "en_core_web_sm")
    
    csv_folder = get_directory("csv_directory")
    pdf_folder = get_directory("pdf_directory")
    output_folder = get_directory("output_directory")
    # category_files = config["category_files"]

    if not os.path.exists(pdf_folder):
        raise FileNotFoundError(f"PDF folder not found: {pdf_folder}")
    
    if not os.path.exists(output_folder):
        print(f"Output directory not found: {output_folder}. Creating it...")
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")

    # for category, filepath in category_files.items():
    #     if not os.path.exists(filepath):
    #         raise FileNotFoundError(f"Word list for {category} not found: {filepath}")
    
    # Populate category_files as a dictionary
    category_files = {
        os.path.splitext(filename)[0]: os.path.join(csv_folder, filename)
        for filename in os.listdir(csv_folder) if filename.endswith(".csv")
    }

    categories = load_word_lists(category_files)
    
    nlp = spacy.load(model_path)

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Processing {filename}...")

            text = extract_text_from_pdf(pdf_path)
            category_counts = analyze_word_frequency_by_category(text, categories, nlp)

            output_path = os.path.join(output_folder, f"{filename}_category_counts.txt")
            with open(output_path, 'w') as f:
                for category, count in category_counts.items():
                    f.write(f"{category}: {count}\n")
            print(f"Results saved to {output_path}")


if __name__ == "__main__":
    main()
