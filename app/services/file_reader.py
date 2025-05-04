from docx import Document
import fitz  # PyMuPDF

class FileReader:
    def read(self, path: str, filetype: str) -> str:
        if filetype == "pdf":
            return self._read_pdf(path)
        elif filetype == "docx":
            return self._read_docx(path)
        elif filetype == "txt":
            return self._read_txt(path)
        else:
            raise ValueError(f"Unsupported file type: {filetype}")

    def _read_txt(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"TXT read error: {e}")

    def _read_pdf(self, path: str) -> str:
        try:
            doc = fitz.open(path)
            return "\n".join([page.get_text() for page in doc])
        except Exception as e:
            raise RuntimeError(f"PDF read error: {e}")

    def _read_docx(self, path: str) -> str:
        try:
            doc = Document(path)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        except Exception as e:
            raise RuntimeError(f"DOCX read error: {e}")
