import os
import pdfplumber
from docx import Document


ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()

    if ext == 'pdf':
        return _extract_from_pdf(filepath)
    elif ext == 'docx':
        return _extract_from_docx(filepath)
    elif ext == 'txt':
        return _extract_from_txt(filepath)
    else:
        raise ValueError(f'Unsupported file type: {ext}')


def _extract_from_pdf(filepath):
    text_parts = []
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return '\n'.join(text_parts)


def _extract_from_docx(filepath):
    doc = Document(filepath)
    text_parts = [para.text for para in doc.paragraphs if para.text.strip()]
    return '\n'.join(text_parts)


def _extract_from_txt(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()