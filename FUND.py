import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# --- App Header ---
c1, c2 = st.columns([30, 50])
c2.title("💰 FundGuard: Quick Emergency Loan Assistance")
c1.image("logo-removebg-preview.png")

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyCgZAWPA5aT5aBneNElR9qjSkS9Gsglr_I")  # Replace with your actual key

# --- Model Initialization (once) ---
def create_model():
    return genai.GenerativeModel("models/gemini-2.5-flash")

model = create_model()

# --- Function to get loan info ---
def get_loan_info(hospital_name):
    prompt = f"""
    You are an assistant helping users find **emergency financial help** near hospitals.
    The user is currently at: "{hospital_name}".
    Provide concise and real-world-style info in the following format:
    1. 🔸 Private Money Lenders (names or platforms)
    2. 💳 Quick Loan / Credit Card Services (like Paytm, KreditBee, etc.)
    3. 🏥 Hospital Contact (Dean / Admin Office info in short)
    4. 📞 Emergency Helplines (financial or hospital-based)
    5. NGO that help give funds
    Keep each section brief (max 2 lines each). Avoid fake data or assumptions.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except exceptions.ResourceExhausted:
        return "⚠️ Error. Please wait a minute before retrying."

    except Exception as e:
        return f"⚠️ Error fetching loan info: {str(e)}"

# --- Main Streamlit function ---
def emergency_loan_services_main():
    hospital_name = st.chat_input("🏥 Enter the name of the nearby hospital:")

    if hospital_name:
        st.subheader("⏳ Fetching Emergency Loan Information...")
        loan_info = get_loan_info(hospital_name)

        # Display structured, readable result
        st.markdown("---")
        st.markdown("### 🏦 Emergency Loan Assistance Details:")
        st.write(loan_info)
        st.markdown("---")

# --- Run App ---
if __name__ == "__main__":
    emergency_loan_services_main()

