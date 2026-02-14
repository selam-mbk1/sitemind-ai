# chat/views.py 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import ChatSession, ChatMessage
from .forms import MessageForm
from documents.services import get_response
import requests


@login_required
def chat_home(request, session_id=None):

    if session_id:
        session = get_object_or_404(
            ChatSession,
            id=session_id,
            user=request.user
        )
    else:
        session = ChatSession.objects.create(user=request.user)

    messages = session.messages.all().order_by("timestamp")
    form = MessageForm()

    if request.method == "POST":

        form = MessageForm(request.POST)

        if form.is_valid():

            user_message = form.cleaned_data["message"]

            ChatMessage.objects.create(
                session=session,
                role="user",
                content=user_message
            )

            try:
                
                # RAG Context Retrieval
                
                context = get_response(user_message, top_k=5)

                if not context:
                    assistant_reply = "No documents found."
                else:

                    prompt = f"""
You are a helpful AI assistant.
Answer ONLY using the context below.

Context:
{context}

Question:
{user_message}
"""

                    
                    # Groq API
                   
                    response = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": "llama-3.1-8b-instant",
                            "messages": [
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.2,
                        },
                    )

                    response.raise_for_status()

                    assistant_reply = response.json()["choices"][0]["message"]["content"]

            except Exception as e:
                print("ERROR:", e)
                assistant_reply = "⚠️ AI error. Check API keys."

            ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=assistant_reply
            )

            return redirect("chat:chat_session", session_id=session.id)

    return render(request, "chat/chat_home.html", {
        "session": session,
        "messages": messages,
        "form": form
    })
