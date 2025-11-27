# TYC Islamic Finance Advisor Web Application

A beautiful web interface for the TYC Islamic Finance Advisor, powered by OpenAI.

## Features

- Modern, responsive web interface
- Real-time chat with the Islamic Finance Advisor
- Educational insights based on AAOIFI standards
- Sharia compliance guidance

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure your `.env` file contains your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
   - **Local access**: http://localhost:5000
   - **Network access**: http://YOUR_IP_ADDRESS:5000

## Deployment for Wide Sharing

**For deploying to the cloud and sharing with anyone, anywhere, see [DEPLOY.md](DEPLOY.md) for detailed instructions.**

### Quick Deploy Options:

1. **Render** (Recommended - Free tier): See DEPLOY.md for step-by-step guide
2. **Railway**: Easy deployment with GitHub integration
3. **Fly.io**: Good free tier with global CDN
4. **ngrok** (Quick test): Temporary tunnel for testing

### Local Network Sharing

If you just want to share on your local network:
1. Find your computer's IP address:
   - **Mac/Linux**: Run `ifconfig` or `ipconfig getifaddr en0`
   - **Windows**: Run `ipconfig` and look for IPv4 Address
2. Share the link: `http://YOUR_IP_ADDRESS:5000`
3. Make sure your friends are on the same WiFi network
4. Ensure your firewall allows connections on port 5000

## Usage

1. Type your question about Islamic finance in the input box
2. Click "Ask" or press Enter
3. The advisor will provide a comprehensive, educational response
4. Continue the conversation by asking follow-up questions

## Example Questions

- "Can you explain whether a conventional fixed-rate bond is Sharia-compliant?"
- "What is the difference between sukuk and conventional bonds?"
- "How does murabaha work in Islamic finance?"
- "What are the key principles of Islamic banking?"

## Notes

- The application runs on port 5000 by default
- For production use, consider using a production WSGI server like Gunicorn
- Make sure to keep your `.env` file secure and never commit it to version control

