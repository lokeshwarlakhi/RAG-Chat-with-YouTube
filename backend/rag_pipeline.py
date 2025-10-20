from dotenv import load_dotenv
from pinecone import Pinecone , ServerlessSpec
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
import asyncio

load_dotenv()

def get_transcirpt(video_id):
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id, languages=["en", "hi"])
    print(f"Transcript fetched for video id: {video_id}")

    transcript = ""
    for snippet in fetched_transcript:
        transcript = transcript + " " + snippet.text

    print(f"chunking the text:")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.create_documents([transcript],metadatas=[{"video_id":video_id}])

    return chunks

def pinecone_ingest(video_id):
    chunks = get_transcirpt(video_id)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    pc_client = Pinecone()
    pc_index_name = "video-transcript"
    if pc_index_name not in pc_client.list_indexes().names():
        pc_client.create_index(
        name=pc_index_name,
        dimension=3072,
        metric='cosine', 
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    ) 
    pc_index = pc_client.Index(pc_index_name)
    vectors = []
    for i,chunk in enumerate(chunks):
        embedding = embeddings.embed_query(chunk.page_content) 
        vector = {
            "id": f"chunk_{i}_{chunk.metadata.get("video_id")}",
            "values":embedding,
            "metadata":{
                "text": chunk.page_content, 
                "video_id":chunk.metadata.get("video_id"),
                "chunk_index":i
            }
        }
        vectors.append(vector)

    return pc_index.upsert(vectors)


def format_docs(relevant_chunks):
    context_text = "\n\n".join(doc["text"] for doc in relevant_chunks)
    return context_text


# A function to load data, process it, and create a retriever
async def retrieve_query_answer( query: str, video_id: str | None=None):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    query_vector = embeddings.embed_query(query)
    pc_client = Pinecone()
    pc_index_name = "video-transcript"
    pc_index = pc_client.Index(pc_index_name)

    search_with_vector= pc_index.query(
        vector = query_vector,
        top_k=4,
        include_metadata=True,
        include_values=False
        )

    relevant_chunks = []
    for match in search_with_vector.matches:
        relevant_chunks.append({
                "id": match.id,
                "score": match.score,
                "text": match.metadata.get("text")
                })
        
    context = format_docs(relevant_chunks)

    prompt_template = PromptTemplate(
        template="""You are a professional productivity coach, and you explain the queries in very comprehensive and easy manner. so based on this consider the below data: 
      {context}
      Now, consider only the above points and based on it answer the question: {query}""",
        input_variables=["context", "query"],
    )

    prompt = prompt_template.invoke({"context":context,"query":query})
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    answer = llm.invoke(prompt)
    return answer

async def main():
    video_id = "Pmd6knanPKw"  # Example video ID
    pinecone_ingest(video_id)
    query = "What is the true nature of atman?"
    answer = await retrieve_query_answer(query=query)
    print(f"Answer: {answer}")

if __name__ == "__main__":
    asyncio.run(main())
