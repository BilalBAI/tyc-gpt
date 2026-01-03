# TYC Islamic Finance Advisor API Documentation

## Base URL

```
https://your-app-name.onrender.com/api/v1
```

## Authentication

Currently, the API is open and does not require authentication. For production use, consider adding API key authentication.

## Endpoints

### 1. Ask a Question

**Endpoint:** `POST /api/v1/ask`

Ask a question to the TYC Islamic Finance Advisor.

#### Request Body

```json
{
  "question": "Can you explain whether a conventional fixed-rate bond is Sharia-compliant?",
  "model": "gpt-5.1",
  "use_pdf_context": false,
  "temperature": 0.3,
  "max_tokens": 1000
}
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `question` | string | Yes | - | Your question about Islamic finance |
| `model` | string | No | `"gpt-5.1"` | Model to use: `"gpt-5.1"` or `"gpt-5-mini"` |
| `use_pdf_context` | boolean | No | `false` | Whether to include AAOIFI Standards context |
| `temperature` | float | No | `0.3` | Sampling temperature (0-2). Only for `gpt-5.1` |
| `max_tokens` | integer | No | `null` | Maximum tokens in response |

#### Response

**Success (200 OK):**

```json
{
  "success": true,
  "question": "Can you explain whether a conventional fixed-rate bond is Sharia-compliant?",
  "answer": "A conventional fixed-rate bond is generally not considered Sharia-compliant...",
  "model": "gpt-5.1",
  "timestamp": "2025-11-30T12:00:00Z"
}
```

**Error (400 Bad Request):**

```json
{
  "success": false,
  "error": "Please provide a question"
}
```

**Error (500 Internal Server Error):**

```json
{
  "success": false,
  "error": "An error occurred while processing your question"
}
```

#### Example: cURL

```bash
curl -X POST https://your-app-name.onrender.com/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is sukuk?",
    "model": "gpt-5.1"
  }'
```

#### Example: Python

```python
import requests

url = "https://your-app-name.onrender.com/api/v1/ask"
payload = {
    "question": "What is sukuk?",
    "model": "gpt-5.1",
    "use_pdf_context": False
}

response = requests.post(url, json=payload)
data = response.json()

if data['success']:
    print(f"Question: {data['question']}")
    print(f"Answer: {data['answer']}")
else:
    print(f"Error: {data['error']}")
```

#### Example: JavaScript

```javascript
fetch('https://your-app-name.onrender.com/api/v1/ask', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: 'What is sukuk?',
    model: 'gpt-5.1'
  })
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log('Answer:', data.answer);
  } else {
    console.error('Error:', data.error);
  }
});
```

---

### 2. Health Check

**Endpoint:** `GET /api/v1/health`

Check if the API is running.

#### Response

```json
{
  "status": "healthy",
  "service": "TYC Islamic Finance Advisor API",
  "version": "1.0.0"
}
```

---

### 3. List Available Models

**Endpoint:** `GET /api/v1/models`

Get information about available models.

#### Response

```json
{
  "models": [
    {
      "id": "gpt-5.1",
      "name": "GPT-5.1",
      "description": "Standard model with full features",
      "supports_temperature": true
    },
    {
      "id": "gpt-5-mini",
      "name": "GPT-5 Mini",
      "description": "Fast model optimized for speed",
      "supports_temperature": false
    }
  ]
}
```

---

## Model Information

### GPT-5.1
- **Description:** Standard model with full features
- **Temperature:** Supported (0-2)
- **Speed:** Standard
- **Use case:** Detailed, comprehensive answers

### GPT-5 Mini
- **Description:** Fast model optimized for speed
- **Temperature:** Not supported (uses default 1)
- **Speed:** Fast
- **Use case:** Quick responses

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (missing or invalid parameters) |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently, there are no rate limits. For production use, consider implementing rate limiting based on your needs.

---

## Notes

- The API uses UTC timestamps
- PDF context is disabled by default to prevent memory issues
- Set `use_pdf_context: true` only if you have sufficient resources
- The `temperature` parameter is ignored for `gpt-5-mini` model

