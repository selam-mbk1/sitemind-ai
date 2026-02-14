import os
import voyageai
from groq import Groq
from rag.vector_store import search
from documents.models import DocumentChunk

vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_response(question):
    query_embedding = vo.embed([question], model="voyage-2").embeddings[0]
    chunk_ids = search(query_embedding)
    chunks = DocumentChunk.objects.filter(embedding_id__in=chunk_ids)
    context = "\n".join([c.content for c in chunks])
    prompt = f"""
    Use the context below to answer clearly.

    Context:
    {context}

    Question:
    {question}
    """
    completion = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content
