from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from src.tyc_advisor import TYCIslamicFinanceAdvisor
import os

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Advisor will be created per request with selected model


@app.route('/')
def index():
    return render_template('index.html')


def _process_question(question, model=None, use_pdf_context=None, temperature=None, max_tokens=None):
    """
    Internal function to process a question with the advisor.
    Returns the answer or raises an exception.
    """
    # Default to gpt-5.1
    if model is None:
        model = 'gpt-5.1'

    # Validate model
    valid_models = ['gpt-5.1', 'gpt-5-mini']
    if model not in valid_models:
        model = 'gpt-5.1'  # Fallback to default

    # Create advisor with selected model
    advisor = TYCIslamicFinanceAdvisor(model=model)

    # Determine PDF context usage
    if use_pdf_context is None:
        use_pdf = os.getenv('ENABLE_PDF_KNOWLEDGE', 'false').lower() == 'true'
    else:
        use_pdf = use_pdf_context

    # Get the answer from the advisor
    answer = advisor.ask(
        question, 
        use_pdf_context=use_pdf,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return answer


@app.route('/ask', methods=['POST'])
def ask():
    """Web frontend endpoint (same as before for backward compatibility)."""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        model = data.get('model', 'gpt-5.1')

        if not question:
            return jsonify({'error': 'Please provide a question'}), 400

        answer = _process_question(question, model=model)

        return jsonify({
            'question': question,
            'answer': answer
        })
    except Exception as e:
        # Log error but return user-friendly message
        print(f"Error in /ask endpoint: {e}")
        return jsonify({'error': 'An error occurred while processing your question. Please try again.'}), 500


@app.route('/api/v1/ask', methods=['POST'])
def api_ask():
    """
    Public API endpoint for TYC Islamic Finance Advisor.
    
    Request body (JSON):
    {
        "question": "Your question about Islamic finance",
        "model": "gpt-5.1" | "gpt-5-mini" (optional, default: "gpt-5.1"),
        "use_pdf_context": true | false (optional, default: false),
        "temperature": 0.3 (optional, only for gpt-5.1),
        "max_tokens": 1000 (optional)
    }
    
    Response (JSON):
    {
        "success": true,
        "question": "Your question",
        "answer": "The advisor's response",
        "model": "gpt-5.1",
        "timestamp": "2025-11-30T12:00:00Z"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400
        
        question = data.get('question', '').strip()
        if not question:
            return jsonify({
                'success': False,
                'error': 'Please provide a question'
            }), 400

        # Get optional parameters
        model = data.get('model', 'gpt-5.1')
        use_pdf_context = data.get('use_pdf_context', False)
        temperature = data.get('temperature')
        max_tokens = data.get('max_tokens')

        # Process the question
        answer = _process_question(
            question, 
            model=model,
            use_pdf_context=use_pdf_context,
            temperature=temperature,
            max_tokens=max_tokens
        )

        from datetime import datetime
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer,
            'model': model,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        })
        
    except Exception as e:
        # Log error for debugging
        print(f"Error in /api/v1/ask endpoint: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': str(e) if os.getenv('FLASK_ENV') == 'development' else 'An error occurred while processing your question'
        }), 500


@app.route('/api/v1/health', methods=['GET'])
def api_health():
    """Health check endpoint for API."""
    return jsonify({
        'status': 'healthy',
        'service': 'TYC Islamic Finance Advisor API',
        'version': '1.0.0'
    })


@app.route('/api/v1/models', methods=['GET'])
def api_models():
    """Get list of available models."""
    return jsonify({
        'models': [
            {
                'id': 'gpt-5.1',
                'name': 'GPT-5.1',
                'description': 'Standard model with full features',
                'supports_temperature': True
            },
            {
                'id': 'gpt-5-mini',
                'name': 'GPT-5 Mini',
                'description': 'Fast model optimized for speed',
                'supports_temperature': False
            }
        ]
    })


if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run on all interfaces so it can be accessed from other devices
    app.run(host='0.0.0.0', port=port, debug=False)
