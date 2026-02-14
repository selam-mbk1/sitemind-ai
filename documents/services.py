import os
from pypdf import PdfReader
from documents.models import DocumentChunk, Document
import voyageai
from rag.utils import cosine_similarity

vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))


def extract_text(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print("PDF extraction error:", e)

    return text.strip()


def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def embed_and_store(document):
    """
    Extract → chunk → embed → save
    """

    if document.extracted_text:
        text = document.extracted_text
    else:
        text = extract_text(document.file.path)
        document.extracted_text = text
        document.save()

    if not text:
        print("No text found")
        return

    chunks = chunk_text(text)

    for chunk_content in chunks:

        embedding = vo.embed(
            [chunk_content],
            model="voyage-2"
        ).embeddings[0]

        DocumentChunk.objects.create(
            document=document,
            content=chunk_content,
            embedding=embedding
        )


def get_response(question, top_k=5):
    """
    RAG pipeline:
    1. Embed question
    2. Compare with all chunks
    3. Return best context
    """

    question_embedding = vo.embed(
        [question],
        model="voyage-2"
    ).embeddings[0]

    all_chunks = DocumentChunk.objects.exclude(embedding=None)

    if not all_chunks.exists():
        return None

    scored = []

    for chunk in all_chunks:
        try:
            score = cosine_similarity(
                question_embedding,
                chunk.embedding
            )
            scored.append((score, chunk.content))
        except:
            continue

    scored.sort(key=lambda x: x[0], reverse=True)

    top_chunks = [c for _, c in scored[:top_k]]

    context = "\n\n".join(top_chunks)

    return context
