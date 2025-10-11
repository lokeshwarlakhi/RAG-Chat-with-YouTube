from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
# load_dotenv(dotenv_path=env_path)
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Your Google key is: {api_key}")

def ingest_video(video_id):
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id, languages=["en", "hi"])
    print(f"Transcript fetched for video id: {video_id}")

    transcript = ""
    for snippet in fetched_transcript:
        transcript = transcript + " " + snippet.text

    print(f"chunking the text:")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.create_documents([transcript])

    # Embedding and storing the data.
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(f"{video_id}_faiss_index")
    return len(chunks)

def format_docs(relevant_chunks):
    context_text = "\n\n".join(doc.page_content for doc in relevant_chunks)
    return context_text

# A function to load data, process it, and create a retriever
def retrieve_query_answer(video_id: str, query: str):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    vector_store = FAISS.load_local(f"{video_id}_faiss_index", embeddings,allow_dangerous_deserialization=True)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 4,
        },
    )

    relevant_chunks= retriever.invoke(query)
    context = format_docs(relevant_chunks)

    prompt_template = PromptTemplate(
        template="""You are a professional productivity coach, and you explain the queries in very comprehensive and easy manner. so based on this consider the below data: 
      {context}
      Now, consider only the above points and based on it answer the question: {query}""",
        input_variables=["context", "query"],
    )
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    parallel_chain = RunnableParallel(
        {
            "context": retriever | RunnableLambda(format_docs),
            "query": RunnablePassthrough(),
        }
    )
    parser = StrOutputParser()
    main_chain = parallel_chain | prompt_template | llm | parser

    answer = main_chain.invoke(query)

    return answer


if __name__ == "__main__":
    video_id = "Pmd6knanPKw"  # Example video ID
    ingest_video(video_id)
    query = "What is a binary search tree?"
    answer = retrieve_query_answer(query)
    print(f"Answer: {answer}")