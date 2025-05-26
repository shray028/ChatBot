# PDF ChatBot

A Python chatbot that answers questions based on PDF documents using Groq's free API, featuring a responsive Tkinter GUI.

## Features

- **PDF Analysis**: Read and analyze text content from PDF files
- **Conversational AI**: Multi-turn chat with context awareness
- **File Attachment**: Supports PDF and text files (.txt, .md, .csv)
- **Responsive UI**: Adapts to different screen sizes
- **Secure**: API key management through environment variables

## Prerequisites

- Python 3.7+
- [Groq API Key](https://console.groq.com/)
- PDF files with selectable text (not image-based)

## Usage

1. Start the application:
```bash
python src/main.py
```

2. In the GUI:
   - Click **Attach File** to select a PDF/text file
   - Type your question in the input box
   - Press **Send** or `Enter` to get answers

Example questions:
- "Summarize this document"
- "What are the key points from page 5?"
- "Explain the methodology section"

## Configuration

```
GROQ_API_KEY=your_api_key_here
MODEL_NAME=llama3-70b-8192  # Default model
MAX_TOKENS=4096             # Response length limit
```

## Troubleshooting

**Common Issues**:
- `401 Unauthorized`: Verify your Groq API key
- `PDF read error`: Ensure PDF has selectable text
- `Model not found`: Check [Groq docs](https://console.groq.com/docs/models) for current models

**Error** | **Solution**
--- | ---
`KeyError: 'choices'` | Update model name in `.env`
`JSONDecodeError` | Reduce PDF file size (<5MB recommended)

## Acknowledgements

- [Groq](https://groq.com/) for their free API tier
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing