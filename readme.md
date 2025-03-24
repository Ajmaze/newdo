# Bolt Clone with Deep Seek AI Integration

A clone of bolt.new with AI-powered code generation using the Deep Seek API.

## Features

- Modern, responsive UI built with Tailwind CSS
- AI-powered code generation and assistance
- Real-time text generation
- Quick action buttons for common development tasks
- Backend API with Flask
- Error handling and logging
- Environment variable configuration

## Prerequisites

- Python 3.8 or higher
- Node.js (for development)
- Deep Seek API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd bolt-clone
```

2. Set up the Python environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env.example` to `.env`
- Add your Deep Seek API key to `.env`:
```
DEEPSEEK_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_APP=server.py
```

## Running the Application

1. Start the Flask backend:
```bash
python server.py
```
The backend will run on `http://localhost:5000`

2. Serve the frontend:
```bash
python -m http.server 8000
```
The frontend will be available at `http://localhost:8000`

## Project Structure

```
├── index.html          # Main HTML file
├── styles.css          # Custom styles
├── script.js           # Frontend JavaScript
├── server.py           # Flask backend
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
└── .gitignore         # Git ignore rules
```

## API Endpoints

- `POST /api/generate`: Generate AI responses
  - Request body: `{ "prompt": "your prompt here" }`
  - Returns generated code or text

- `GET /api/health`: Health check endpoint
  - Returns API status and configuration state

## Development

- The frontend uses Tailwind CSS for styling
- Real-time text generation is handled through the Deep Seek API
- The backend provides a RESTful API for the frontend
- Logs are stored in the `logs` directory

## Error Handling

- Frontend displays toast notifications for errors
- Backend logs errors to `logs/app.log`
- API errors are properly handled and returned to the client

## Security

- API keys are stored in environment variables
- CORS is configured for development
- Sensitive files are git-ignored

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this code for your own projects.