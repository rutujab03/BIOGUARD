import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# --- App Header ---
c1, c2 = st.columns([30, 50])
c2.title("🚑 RescueGuard: Emergency Contacts & Nearest Hospitals")
c1.image("logo-removebg-preview.png")

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyC_vqWwogUV6_obXPyPzGL0NFql5jImmYA")  # Replace with your actual key

# --- Create model once globally ---
def create_model():
    return genai.GenerativeModel("models/gemini-2.5-flash")

model = create_model()

# --- Function to get emergency info ---
def get_emergency_info(keyword, location):
    prompt = f"""
    You are an assistant helping users in a medical emergency.
    The user reported an emergency related to: "{keyword}".
    Their current location: "{location}".

    Provide a clear, concise, and realistic list in this format:
    🏥 **Nearest Hospitals (with phone numbers or helplines)**
    - Hospital name – contact number – area (approx)
    - Mention up to 5 entries.

    🚑 **Ambulance / Emergency Services**
    - List 2–3 ambulance numbers or hotlines (e.g., 108, Red Cross, etc.)

    ⏱️ **Estimated Help Time**
    - Mention average response time or travel duration (short, realistic estimate).

    Keep the tone urgent but calm. Avoid fake data or precise map links.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except exceptions.ResourceExhausted:
        return "⚠️ Error. Please wait a minute and try again."

    except Exception as e:
        return f"⚠️ Error fetching emergency info: {str(e)}"

# --- Main Streamlit function ---
def emergency_services_main():
    st.write("Please provide your emergency details below 👇")

    keyword = st.text_input("🆘 Type of Emergency (e.g., accident, chest pain, pregnancy):")
    location = st.text_input("📍 Current Location (address, city, or coordinates):")

    if st.button("🚨 Get Emergency Help"):
        if keyword and location:
            st.subheader("⏳ Searching for nearest emergency help...")
            emergency_info = get_emergency_info(keyword, location)

            st.markdown("---")
            st.markdown("### 🏥 Emergency Assistance Details")
            st.write(emergency_info)
            st.markdown("---")
        else:
            st.warning("⚠️ Please enter both the emergency type and your location.")

# --- Run App ---
if __name__ == "__main__":
    emergency_services_main()
