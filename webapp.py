import streamlit as st
import re
from google import genai
import os

# Set your Gemini API key
API_KEY = os.getenv("api_key")

# Configure Gemini client
client = genai.Client(api_key=API_KEY)

# Sentiment analysis function with confidence
def analyze_sentiment(text):
    prompt = f"""
Classify the sentiment of the following text into one of these categories: Positive, Negative, or Neutral.

Text: "{text}"

Respond in this format (exactly):
Sentiment: <Positive/Negative/Neutral>
Confidence: <percentage between 0 and 100>
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        result_text = response.text.strip()

        # Extract sentiment and confidence using regex
        sentiment_match = re.search(r"Sentiment:\s*(Positive|Negative|Neutral)", result_text, re.IGNORECASE)
        confidence_match = re.search(r"Confidence:\s*(\d{1,3})", result_text)

        sentiment = sentiment_match.group(1).capitalize() if sentiment_match else "Unknown"
        confidence = int(confidence_match.group(1)) if confidence_match else None

        return sentiment, confidence
    except Exception as e:
        return "Error", None

# Helper to pick emoji
def sentiment_emoji(sentiment):
    return {
        "Positive": "😊",
        "Negative": "😞",
        "Neutral": "😐"
    }.get(sentiment, "❓")

# Streamlit UI
st.set_page_config(page_title="Sentiment Analyzer", layout="centered")
st.markdown("<h1 style='text-align: center;'>🧠 Sentiment Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Enter some text below to detect its sentiment and confidence level.</p>", unsafe_allow_html=True)

# Input area
with st.container():
    user_input = st.text_area("✍️ Your text:", height=150, placeholder="Type something...")

# Analyze button
if st.button("🔍 Analyze"):
    if not user_input.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing..."):
            sentiment, confidence = analyze_sentiment(user_input)

            if sentiment == "Error":
                st.error("Something went wrong during analysis.")
            else:
                st.markdown("---")
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f"<h2 style='text-align: center;'>{sentiment_emoji(sentiment)}</h2>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"### Sentiment: `{sentiment}`")

                if confidence is not None:
                    st.markdown(f"**Confidence:** {confidence}%")
                    st.progress(confidence)
                else:
                    st.info("Confidence level not available.")

