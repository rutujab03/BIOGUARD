import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# --- App Header ---
c1, c2 = st.columns([30, 50])
c2.title("🏋️‍♂️ FitGuard: Smart BMI & Fitness Planner")
c1.image("logo-removebg-preview.png")

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyBM4eT0kLhUSr5r-8Iwj5W-8pC5MhAP-k4")  # Replace with your API key

# --- Create model once globally ---
def create_model():
    return genai.GenerativeModel("models/gemini-2.5-flash")

model = create_model()

# --- Core Calculations ---
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def bmi_status_label(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal weight"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# --- Gemini Recommendation ---
def get_fitness_plan(bmi_status, health_condition, weight, height, age, gender, activity_level):
    prompt = f"""
    You are a certified fitness and nutrition assistant (not a doctor).
    Based on these user details, create a **concise, readable plan**:

    - BMI Status: {bmi_status} (from height {height} m, weight {weight} kg)
    - Health Conditions: {health_condition or "None"}
    - Age: {age}, Gender: {gender}
    - Activity Level: {activity_level}

    Format your response in markdown with emoji headers:

    🧠 **1. Health Summary**
    🍎 **2. Nutrition Plan** (3 meal ideas, short)
    💪 **3. Exercise Plan** (simple home or gym routine)
    ⚕️ **4. Special Advice** (based on health conditions)
    📅 **5. Weekly Progress Tips**

    Keep under 250 words, avoid fake data or long paragraphs.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except exceptions.ResourceExhausted:
        return "⚠️ Error please try again after a minute"

    except Exception as e:
        return f"⚠️ Error generating fitness plan: {str(e)}"


# --- Main App Logic ---
def fitguard_main():
    st.subheader("💬 Enter Your Details Below")

    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (m):", 0.5, 2.5, 1.7, 0.01)
        weight = st.number_input("Weight (kg):", 10.0, 200.0, 70.0, 0.1)
        age = st.number_input("Age:", 18, 100, 30, 1)
    with col2:
        gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
        activity = st.select_slider(
            "Activity Level:",
            options=[
                "Sedentary", "Lightly Active",
                "Moderately Active", "Very Active", "Extremely Active"
            ],
            value="Moderately Active"
        )
        condition = st.text_area("Health Conditions (if any):", height=90)

    if st.button("⚖️ Calculate BMI & Generate Plan", type="primary"):
        if height > 0 and weight > 0:
            bmi = calculate_bmi(weight, height)
            status = bmi_status_label(bmi)

            with st.spinner("🧠 Generating your personalized fitness plan..."):
                plan = get_fitness_plan(status, condition, weight, height, age, gender, activity)

            # --- Display results right below inputs ---
            st.markdown("---")
            st.subheader("📋 Your Fitness Report")

            bmi_col1, bmi_col2 = st.columns([1, 2])
            with bmi_col1:
                st.metric("Your BMI", f"{bmi:.1f}")
                colors = {
                    "Underweight": "orange",
                    "Normal weight": "green",
                    "Overweight": "orange",
                    "Obese": "red"
                }
                st.markdown(
                    f"<h3 style='color:{colors.get(status, 'blue')};'>{status}</h3>",
                    unsafe_allow_html=True
                )
            with bmi_col2:
                st.markdown("""
                **BMI Reference:**
                - Underweight: < 18.5  
                - Normal: 18.5–24.9  
                - Overweight: 25–29.9  
                - Obese: ≥ 30
                """)

            st.markdown("### 🧾 Your Personalized Plan")
            st.markdown(plan)

            # --- Download option ---
            st.download_button(
                "⬇️ Download Fitness Plan",
                data=f"# FitGuard Plan\n\nBMI: {bmi:.1f} ({status})\n\n{plan}",
                file_name="fitguard_plan.md",
                mime="text/markdown",
            )


# --- Run App ---
if __name__ == "__main__":
    fitguard_main()

