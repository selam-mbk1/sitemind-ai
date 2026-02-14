from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import DocumentUploadForm
from .models import Document, DocumentChunk
import PyPDF2
from .utils import get_embedding


# -------------------------------
# HELPER FUNCTION TO CREATE CHUNKS
# -------------------------------
def create_chunks(document, text, chunk_size=500):
    """
    Split text into chunks, embed each, and save as DocumentChunk.
    """
    for i in range(0, len(text), chunk_size):
        chunk_text = text[i:i + chunk_size]

        try:
            embedding_vector = get_embedding(chunk_text)
        except Exception as e:
            print(f"Embedding failed: {e}")
            embedding_vector = None

        DocumentChunk.objects.create(
            document=document,
            content=chunk_text,
            embedding=embedding_vector
        )


# -------------------------------
# DOCUMENTS HOME VIEW
# -------------------------------
@login_required
def documents_home(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)

            # ✅ FIXED: use uploaded_by
            document.uploaded_by = request.user
            document.save()

            # Extract text from PDF
            text = ""
            try:
                pdf_reader = PyPDF2.PdfReader(document.file)
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""

                document.extracted_text = text
                document.save()

            except Exception as e:
                print(f"PDF extraction failed: {e}")

            # Create chunks + embeddings
            if text:
                create_chunks(document, text)

            return redirect('documents:documents_home')

    else:
        form = DocumentUploadForm()

    # ✅ FIXED: filter by uploaded_by
    documents = Document.objects.filter(uploaded_by=request.user)

    return render(request, 'documents/documents_home.html', {
        'form': form,
        'documents': documents
    })


# -------------------------------
# API VIEW TO UPLOAD DOCUMENT
# -------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_document(request):
    file = request.FILES.get('file')
    title = request.data.get('title')

    if not file or not title:
        return Response({"error": "Title and file are required"}, status=400)

    # ✅ FIXED: use uploaded_by
    document = Document.objects.create(
        title=title,
        file=file,
        uploaded_by=request.user
    )

    # Extract text
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(document.file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        document.extracted_text = text
        document.save()

    except Exception as e:
        print(f"PDF extraction failed: {e}")

    # Create chunks + embeddings
    if text:
        create_chunks(document, text)

    return Response({
        "message": "Document processed successfully",
        "document_id": document.id
    })
