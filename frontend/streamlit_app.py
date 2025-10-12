import requests
import streamlit as st

st.set_page_config(
    page_title="RAG Chat with YouTube", page_icon="🎥", layout="centered"
)

st.title("🎬 RAG Chat with YouTube Video")

API_BASE_URL = "http://127.0.0.1:8000"


# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "video_id" not in st.session_state:
    st.session_state.video_id = None
if "video_ingested" not in st.session_state:
    st.session_state.video_ingested = False

st.write(st.session_state)

# --- Video ingestion section ---
with st.expander("📥 Ingest YouTube Video", expanded=True):
    yt_video_url = st.text_input("Paste the YouTube video URL")

    if st.button("🚀 Ingest Video", type="primary"):
        if not yt_video_url:
            st.warning("Please enter a valid YouTube URL.")
        else:
            video_id = yt_video_url.split("v=")[-1].split("&")[0]
            ingest_data = {"video_id": video_id}

            with st.spinner("Fetching and ingesting video transcripts..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/ingest_video", json=ingest_data
                    )
                    response.raise_for_status()
                    st.session_state.video_id = video_id
                    st.session_state.video_ingested = True
                    st.success("✅ Transcriptions successfully ingested!")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Error connecting to FastAPI: {e}")

# --- Chat interface ---
if st.session_state.video_ingested:
    st.markdown("---")
    st.subheader("💬 Chat with the Video")

    chat_container = st.container()

    # Display previous chat history
    with chat_container:
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown("---")
                st.markdown(f"#### _🧑 You: {chat['content']}_")
            else:
                st.markdown(f"**🤖 Assistant:** {chat['content']}")

    # User input at the bottom
    user_query = st.chat_input("Ask something about the video...")

    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        with st.spinner("Thinking..."):
            try:
                print("VIDEO ID:", st.session_state.video_id, "!")
                response = requests.post(
                    f"{API_BASE_URL}/query",
                    json={"video_id": st.session_state.video_id, "query": user_query},
                )
                response.raise_for_status()
                answer = response.json().get("answer", "No answer returned.")
            except requests.exceptions.RequestException as e:
                answer = f"Error connecting to FastAPI: {e}"

        # Append assistant response
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

        # Refresh chat display
        st.rerun()

else:
    st.info("👆 Ingest a video first to start chatting.")
