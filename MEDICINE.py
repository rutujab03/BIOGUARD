import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# --- App Header ---
c1, c2 = st.columns([30, 50])
c2.title("MedGuard: Medicine Info & Safe Alternatives")
c1.image("logo-removebg-preview.png")

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyATj2hweNVg7WGlxWeQC3dmDSjpGhuw4-0")  # Replace with your own API key

# --- Create model once ---
def create_model():
    return genai.GenerativeModel("models/gemini-2.5-flash")

model = create_model()

# --- Function to get combined medicine info and alternatives ---
def get_medicine_info(medicine_name):
    prompt = f"""
    You are a medical information assistant (not a doctor).
    Provide a brief, user-friendly response about the medicine **{medicine_name}**.
    Format your response in two clear sections:

    🧾 **1. Medicine Information**
    - Key uses (1–2 lines)
    - Common side effects (bullet list)
    - Precautions (1–2 lines)

    🌿 **2. Alternative Options**
    - List up to 5 medicines with the same active ingredient.
    - Mention 1–2 Ayurvedic or herbal alternatives (if relevant).
    - Keep total response under 200 words.

    Do NOT include fake data or URLs.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except exceptions.ResourceExhausted:
        return "⚠️ Error. Please try again in a minute."

    except Exception as e:
        return f"⚠️ Error fetching medicine info: {str(e)}"

# --- Main Streamlit function ---
def main():
    medicine_name = st.chat_input("💬 Enter the medicine name:")

    if medicine_name:
        st.subheader("⏳ Fetching information...")
        result = get_medicine_info(medicine_name)

        st.markdown("---")
        st.markdown("### 💊 Medicine Information & Alternatives")
        st.write(result)
        st.markdown("---")

# --- Run App ---
if __name__ == "__main__":
    main()
