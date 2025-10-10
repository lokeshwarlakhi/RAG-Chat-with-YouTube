# RAG-Chat-with-YouTube
This project is a basic RAG based application built to interact with the youtube videos you like in chat manner. user can provide the youtube video URL and ask questions from the video, and get a answer that is fully grounded to the video uploaded(URL).

<!-- Demo -->
<div style="text-align: center;">
<iframe src="https://drive.google.com/file/d/1qFzcn6GBEhCjMsR3CEuhEs-3qm8Ji33s/preview" width="730" height="480" allow="autoplay"></iframe>
</div>

### Motivation
I've built it to gain a hands-on, practical understanding of how RAG systems work. This project was a journey to explore key concepts such as document ingestion, vector embeddings, similarity search, and prompting large language models (LLMs) to retrieve information from an external knowledge base rather than relying solely on their pre-trained data.

### Challenges & Solutions


### Quick Setup
1. clone the repo 
   ```bash
   git clone https://github.com/lokeshwarlakhi/RAG-Chat-with-YouTube.git
   ```
2. add secrets to .env file [paste in your Google API key in the place of"[YOUR-API-KEY-HERE]" ]
   ```bash
   echo 'GOOGLE_API_KEY="[YOUR-API-KEY-HERE]"' >> .env
   ```
3. install the required packages 
   ```bash
   pip install -r requirements.txt
   ```
4. get the backend started
   ```bash  
   uvicorn backend.app:app --reload
   ```
5. get the frontend started
   ```bash
   streamlit run frontend/streamlit_app.py
   ```
