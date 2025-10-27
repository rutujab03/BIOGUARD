import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# --- Streamlit UI setup ---
c1, c2 = st.columns([30, 50])
c2.title("PredictGuard 🧠 - Disease Prediction from Symptoms")
c1.image("logo-removebg-preview.png")

# --- Configure API ---
genai.configure(api_key="AIzaSyBdCcRrsHr7JsFCThMgVsTYApL9AO6aRfY")  # Replace with your key safely

# --- Create model once ---
def create_gen_model():
    return genai.GenerativeModel('models/gemini-2.5-flash')

model = create_gen_model()

# --- Core logic ---
def get_prediction_and_solution(symptoms):
    """Single combined Gemini API call with error handling."""
    prompt = f"""
    You are a helpful medical assistant.
    Step 1: From these symptoms: "{symptoms}", identify the most likely disease name in 1 line.
    Step 2: Suggest short and general medications or treatments (no prescriptions) for that disease in 4-5 lines.
    Format:
    Disease: <disease name>
    Treatment: <short advice>
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except exceptions.ResourceExhausted:
        return "⚠️ Error. Please wait a minute and try again."

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# --- Streamlit main function ---
def main():
    user_input = st.chat_input("🩺 Enter your symptoms:")

    if user_input:
        st.subheader("⏳ Analyzing symptoms...")
        output = get_prediction_and_solution(user_input)

        # Display cleanly formatted result
        if "Disease:" in output:
            disease_line, treatment_line = output.split("\n", 1)
            st.success(disease_line)
            st.info(treatment_line)
        else:
            st.warning(output)


if __name__ == "__main__":
    main()

