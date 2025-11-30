from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from src.tyc_advisor import TYCIslamicFinanceAdvisor
import os

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Initialize the advisor
advisor = TYCIslamicFinanceAdvisor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()

        if not question:
            return jsonify({'error': 'Please provide a question'}), 400

        # Get the answer from the advisor
        # PDF context disabled by default on Render due to memory constraints
        # Set ENABLE_PDF_KNOWLEDGE=true to enable (not recommended on free tier)
        use_pdf = os.getenv('ENABLE_PDF_KNOWLEDGE', 'false').lower() == 'true'
        answer = advisor.ask(question, use_pdf_context=use_pdf)

        return jsonify({
            'question': question,
            'answer': answer
        })
    except Exception as e:
        # Log error but return user-friendly message
        print(f"Error in /ask endpoint: {e}")
        return jsonify({'error': 'An error occurred while processing your question. Please try again.'}), 500


if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run on all interfaces so it can be accessed from other devices
    app.run(host='0.0.0.0', port=port, debug=False)
