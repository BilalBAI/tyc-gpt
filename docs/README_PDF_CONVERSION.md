# PDF to Text Conversion

The application now reads from a text file (`AAOIFI-Standards.txt`) instead of parsing the PDF directly. This is:
- **Much faster** - No PDF parsing overhead
- **More reliable** - No memory issues
- **Easier to deploy** - Text file is much smaller and faster to load

## Converting the PDF

To convert the full PDF to text file, run:

```bash
python convert_pdf_to_text.py
```

This will create `AAOIFI-Standards.txt` with all pages from the PDF.

**Note:** The conversion may take a few minutes for the full 1264-page PDF.

## How It Works

1. The application first checks for `AAOIFI-Standards.txt`
2. If found, it reads from the text file (fast!)
3. If not found, it falls back to PDF parsing (slower, may have memory issues)

## Deployment

For deployment to Render:
1. Convert the PDF to text file locally
2. Commit the text file to git (it's much smaller than PDF)
3. Deploy - the app will use the text file automatically

The text file is much smaller (~2-3 MB vs 11 MB PDF) and loads instantly without memory issues.

