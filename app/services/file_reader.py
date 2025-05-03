# app/services/file_reader.py
from docx import Document
import fitz

class FileReader:
    def read(self, path: str, filetype: str) -> str:
        if filetype == "pdf":
            return self._read_pdf(path)
        elif filetype == "docx":
            return self._read_docx(path)
        else:
            raise ValueError("Unsupported file type")

    def _read_pdf(self, path: str) -> str:
        text = ""
        doc = fitz.open(path)
        for page in doc:
            text += page.get_text()
        return text

    def _read_docx(self, path: str) -> str:
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
