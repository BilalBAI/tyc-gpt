# TYC Islamic Finance Advisor

A web application providing AI-powered Islamic finance and Sharia compliance advisory services, powered by OpenAI and AAOIFI Standards.

## 📁 Project Structure

```
tyc-gpt/
├── src/                    # Main application code
│   ├── app.py             # Flask web application
│   ├── tyc_advisor.py     # Core advisor class
│   ├── pdf_knowledge.py   # AAOIFI Standards knowledge base
│   ├── prompt_config.py   # System prompt configuration
│   ├── templates/         # HTML templates
│   └── static/            # CSS and static assets
├── data/                   # Data files
│   ├── AAOIFI-Standards.pdf
│   └── AAOIFI-Standards.txt
├── scripts/                # Utility scripts
│   ├── convert_pdf_to_text.py
│   └── ...
├── docs/                   # Documentation
│   ├── DEPLOY.md
│   └── ...
├── requirements.txt        # Python dependencies
├── Procfile               # Deployment configuration
└── README.md              # This file
```

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Run the application:**
   ```bash
   python src/app.py
   ```

4. **Access the application:**
   - Local: http://localhost:5000
   - Network: http://YOUR_IP:5000

## 📚 Features

- **AI-Powered Advisor**: Answers questions about Islamic finance and Sharia compliance
- **AAOIFI Standards Integration**: References official AAOIFI Standards when relevant
- **Modern Web Interface**: Beautiful, responsive chat interface
- **Educational Focus**: Provides clear, structured explanations suitable for beginners and professionals

## 🔧 Configuration

### System Prompt
Edit `src/prompt_config.py` to modify the advisor's behavior and knowledge base.

### PDF Knowledge Base
The application uses a text file (`data/AAOIFI-Standards.txt`) for fast access to AAOIFI Standards. To regenerate:
```bash
python scripts/convert_pdf_to_text.py
```

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `ENABLE_PDF_KNOWLEDGE`: Set to `'true'` to enable PDF context (default: `'false'`)

## 📦 Deployment

See [docs/DEPLOY.md](docs/DEPLOY.md) for detailed deployment instructions to Render, Railway, or other platforms.

### Quick Deploy to Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn src.app:app`
5. Add environment variable: `OPENAI_API_KEY`

## 📖 Documentation

- [Deployment Guide](docs/DEPLOY.md)
- [Deployment Checklist](docs/DEPLOYMENT_CHECKLIST.md)
- [PDF Conversion Guide](docs/README_PDF_CONVERSION.md)

## 🛠️ Development

### Running Tests
```bash
python -c "from src.app import app; print('App loads successfully')"
```

### Converting PDF
```bash
python scripts/convert_pdf_to_text.py
```

## 📝 License

Copyright © 2021 TYC Finance Limited. All rights reserved.

## 🤝 Support

For issues or questions, please refer to the documentation in the `docs/` folder.
