#Sitemind-AI

Sitemind-AI is a modern AI-powered chatbot web application integrated with a knowledge base. Using Retrieval-Augmented Generation (RAG), it provides context-aware, accurate responses from PDFs, text files, and website content. Users can manage documents, interact with the chatbot, and review chat history in a secure environment.

##Features
###Authentication & Authorization

Secure user registration and login (email/username & password)

JWT and session-based authentication

Only authenticated users can access chat and document management

###AI Chatbot (RAG-Powered)

Context-aware responses from uploaded documents

Supports PDFs and text files

Maintains conversation history per user

###Knowledge Base Management

Upload and manage PDFs, text documents, or website content

Automatic text extraction and embedding generation

Only authenticated users can manage documents

###Chat Interface

Modern, clean, responsive UI

Floating chat widget with real-time message streaming

Typing indicators for user-friendly interaction

###Chat History

Stores chat sessions securely in the database

Users can view previous conversations and resume chats

###other

AI-augmented development with Groq API

Future-ready deployment on serverless platforms (Vercel, Railway, AWS Amplify)

##Tech Stack

Frontend: HTML5, CSS3, Tailwind CSS, JavaScript, React (optional for SPA)

Backend: Django 5, Django REST Framework, Python 3.11

Database: MySQL for structured data

Authentication: Django-allauth, JWT

AI Integration: Groq API (RAG-based responses)

Document Processing: PDF & text parsing with automatic embeddings

Deployment: Vercel / Railway / AWS Amplify (optional)

##Installation

###Clone the repository

git clone https://github.com/your-username/sitemind-ai.git
cd sitemind-ai


###Create a virtual environment

python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux / macOS


###Install dependencies

pip install -r requirements.txt


###Create a .env file in the project root with your keys:

SECRET_KEY=your_django_secret_key
DEBUG=True
MYSQL_DB=your_database_name
MYSQL_USER=your_database_user
MYSQL_PASSWORD=your_database_password
VOYAGE_API_KEY=your_voyage_api_key
GROQ_API_KEY=your_groq_api_key


###Run migrations

python manage.py migrate


###Start the development server

python manage.py runserver


###Open your browser at:
http://127.0.0.1:8000

##Folder Structure
sitemind_ai/
├── accounts/           # User authentication & management
├── chat/               # Chatbot & chat history
├── documents/          # PDF/Text management & embeddings
├── rag/                # Retrieval-Augmented Generation services
├── config/             # Django project settings
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── media/              # Uploaded files
├── venv/               # Python virtual environment
└── .env                # Environment variables (not tracked in Git)

##Usage

Register or log in as a user.

Access the chat page to start a conversation.

Upload PDFs or text documents via the admin page.

Chatbot retrieves relevant content using RAG embeddings.

Access chat history to view and resume previous sessions.

##Contributing

Fork the repository.

Create a branch: git checkout -b feature-name

Commit your changes: git commit -m "Add new feature"

Push to the branch: git push origin feature-name

Open a Pull Request.

##License

This project is licensed under the MIT License 
