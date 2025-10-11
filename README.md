# 🎥 RAG-Chat-with-YouTube
This project is a basic RAG based application built to interact with the youtube videos you like in chat manner. user can provide the youtube video URL and ask questions from the video, and get a answer that is fully grounded to the video uploaded(URL).

---
## 🎬 Demo
<!-- Demo -->
<div align="center">
   <video src="https://github.com/user-attachments/assets/5b1d273c-12b0-41d9-b984-ab7c69e9e88b" alt="Demo of Hands-On with Rag Chat with YouTube" autoplay>
</div>

---
### 💡 Motivation
I've built it to gain a hands-on, practical understanding of how RAG systems work. This project was a journey to explore key concepts such as document ingestion, vector embeddings, similarity search, and prompting large language models (LLMs) to retrieve information from an external knowledge base rather than relying solely on their pre-trained data.

---
## ⚡️ Challenges & Solutions

---
## 🚀 Quick Setup
### 1. 📥 clone the repo 
```bash
git clone https://github.com/lokeshwarlakhi/RAG-Chat-with-YouTube.git
```
### 2. 📁 Navigate to project directory
```bash
cd RAG-Chat-with-YouTube
```
### 3. 🔑 Setup API Key
- Generate an API Key 🔗 _[Here.](https://aistudio.google.com/app/api-keys)_
- Add it to your .env file:
```bash
echo 'GOOGLE_API_KEY="[YOUR-API-KEY-HERE]"' >> .env
```

### 4. 📦 Install dependencies
```bash
pip install -r requirements.txt
```
### 5. 🔧 Start the backend server
```bash  
uvicorn backend.main:app --reload
```
### 6. 🌐 Launch the frontend
```bash
streamlit run frontend/streamlit_app.py
```
---
## 🛠️ Tech Stack
🤖 Tags: Google Gemini API, RAG Architecture

🌐 Backend: FastAPI, Uvicorn

🎨 Frontend: Streamlit

📊 Vector Store: FAISS

🔍 Embeddings: Google Embeddings

## 📋 Features
✅ YouTube video content extraction

✅ Intelligent chat interface

✅ Context-aware responses

✅ Real-time processing

> 💫 Star this repo if you find it helpful! 
