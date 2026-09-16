import io
from typing import Union, Tuple, Dict, Any

def extract_text_from_pdf(file_input: Union[str, bytes, io.BytesIO]) -> Tuple[str, Dict[str, Any]]:
    """
    Extract text cleanly from a PDF file using PyMuPDF (fitz).
    Handles file paths, bytes, or Streamlit UploadedFile objects.
    Extracts text page by page preserving natural reading layout.
    """
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz
        except ImportError:
            raise ImportError("PyMuPDF is required for PDF parsing. Please install pymupdf.")

    text_parts = []
    metadata = {
        "format": "PDF",
        "page_count": 0,
        "char_count": 0,
        "pages_info": []
    }

    try:
        if isinstance(file_input, str):
            doc = fitz.open(file_input)
        elif isinstance(file_input, bytes):
            doc = fitz.open(stream=file_input, filetype="pdf")
        elif hasattr(file_input, "read"):
            # BytesIO or UploadedFile
            stream_bytes = file_input.read()
            if hasattr(file_input, "seek"):
                file_input.seek(0)
            doc = fitz.open(stream=stream_bytes, filetype="pdf")
        else:
            raise ValueError(f"Unsupported file input type: {type(file_input)}")

        metadata["page_count"] = len(doc)

        for page_num in range(len(doc)):
            page = doc[page_num]
            # Use 'blocks' extraction to respect vertical text layout
            blocks = page.get_text("blocks")
            # Sort blocks by vertical position (y0), then horizontal position (x0)
            blocks.sort(key=lambda b: (b[1], b[0]))
            
            page_text = "\n".join(b[4].strip() for b in blocks if b[4].strip())
            if not page_text:
                # Fallback to plain text extraction
                page_text = page.get_text("text").strip()
            
            text_parts.append(page_text)
            metadata["pages_info"].append({
                "page_number": page_num + 1,
                "char_count": len(page_text)
            })

        doc.close()
        full_text = "\n\n".join(text_parts).strip()
        metadata["char_count"] = len(full_text)
        return full_text, metadata

    except Exception as e:
        raise RuntimeError(f"Error parsing PDF file: {str(e)}") from e
