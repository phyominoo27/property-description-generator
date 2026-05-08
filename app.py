import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

if "history" not in st.session_state:
    st.session_state.history = []


# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)



# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Property Description Generator",
    page_icon="🏠",
    layout="centered",
)


# -----------------------------
# Dark theme CSS
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #111827 45%, #1e1b4b 100%);
        color: #e5e7eb;
    }

    .main-card {
        background: rgba(15, 23, 42, 0.88);
        padding: 28px;
        border-radius: 24px;
        border: 1px solid rgba(129, 140, 248, 0.25);
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.35);
        margin-bottom: 24px;
    }

    .app-title {
        font-size: 38px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 8px;
        line-height: 1.15;
    }

    .app-subtitle {
        font-size: 16px;
        color: #cbd5e1;
        margin-bottom: 0px;
        line-height: 1.6;
    }

    .details-title {
        color: #60a5fa;
        font-size: 24px;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 14px;
    }

    .preview-title {
        color: #c084fc;
        font-size: 24px;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 14px;
    }

    .output-title {
        color: #34d399;
        font-size: 24px;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 14px;
    }

    .preview-box {
        background: rgba(15, 23, 42, 0.95);
        color: #e2e8f0;
        padding: 20px;
        border-radius: 18px;
        margin-top: 16px;
        line-height: 1.8;
        border: 1px solid rgba(148, 163, 184, 0.25);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.28);
    }

    .preview-box strong {
        color: #ffffff;
    }

    .small-note {
        color: #94a3b8;
        font-size: 14px;
        margin-top: -4px;
        margin-bottom: 16px;
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 14px;
        font-weight: 700;
        font-size: 16px;
    }

    div.stButton > button:hover {
        color: white;
        border: none;
        box-shadow: 0 10px 25px rgba(96, 165, 250, 0.28);
    }

    label,
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stNumberInput label {
        color: #e5e7eb !important;
        font-weight: 600;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Helper functions
# -----------------------------
def build_prompt(
    property_type,
    location,
    bedrooms,
    bathrooms,
    area,
    price,
    special_features,
    language_style,
    tone,
):
    prompt = f"""
You are a professional real estate marketing assistant for Myanmar property agents.

Your job:
Generate attractive property listing copy from the property details below.

Important requirements:
- Burmese language support is mandatory.
- Understand Myanmar real estate style.
- Handle Myanmar price formats like lakh, သိန်း, MMK, USD.
- Make the Burmese natural, not robotic.
- Keep the English professional and clear.
- Do not invent missing facts.
- If some details are missing, write around them naturally.

Property details:
- Property type: {property_type}
- Location: {location}
- Bedrooms: {bedrooms}
- Bathrooms: {bathrooms}
- Area: {area}
- Price: {price}
- Special features: {special_features}
- Language style requested: {language_style}
- Tone requested: {tone}

Output format:

## 1. Headline
Write one short attractive headline.

## 2. Burmese Description
Write 3-5 natural Burmese sentences for Myanmar buyers/renters.

## 3. English Description
Write 3-5 professional English sentences.

## 4. Facebook Post
Write a Facebook-style post. Friendly, clear, casual but professional. Use emojis if it fits.

## 5. Key Selling Points
Give 5 short bullet points.

Use the requested language style: {language_style}
Use this tone: {tone}
"""
    return prompt.strip()


def generate_description(prompt):
    if not GEMINI_API_KEY:
        return """
ERROR: GEMINI_API_KEY is missing.


Fix:
1. Create a .env file in the same folder as app.py
2. Add this line:
   GEMINI_API_KEY=your_gemini_api_key_here
3. Save the file
4. Restart Streamlit
""".strip()

    try:
        response = client.chat.completions.create(
            model= "gemini-3.1-flash-lite",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior real estate marketing assistant specializing in crafting natural, engaging property descriptions in both Burmese and English."
                        "You leverage deep Myanmar market insights to attract buyers and renters while strictly adhering to provided details."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.7,
            max_tokens=2000,
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"API request failed:\n\n{error}"


# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="main-card">
        <div class="app-title">🏠 Property Description Generator</div>
        <p class="app-subtitle">
            အိမ်ခြံမြေ အချက်အလက် အနည်းငယ် ထည့်သွင်းရုံဖြင့် မြန်မာဘာသာ နှင့် အင်္ဂလိပ်ဘာသာ နှစ်မျိုးလုံးဖြင့် အိမ်ခြံမြေ ကြော်ငြာစာသားများ ရေးသားပေးနိုင်သော စနစ်
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Form section
# -----------------------------
st.markdown(
    '<h3 class="details-title">🏡 Property Details / အိမ်ခြံမြေ အချက်အလက်</h3>',
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="small-note">Fill in the property information below. Simple input is enough.</p>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    property_type = st.selectbox(
        "Property type / အမျိုးအစား",
        [
            "Apartment",
            "Condo",
            "House",
            "Land",
            "Commercial",
            "Office",
            "Shop",
        ],
    )

    location = st.text_input(
        "Location / တည်နေရာ",
        placeholder="Example: Sanchaung / စမ်းချောင်း",
    )

    bedrooms = st.number_input(
        "Bedrooms / အိပ်ခန်း",
        min_value=0,
        max_value=30,
        value=2,
        step=1,
    )

    bathrooms = st.number_input(
        "Bathrooms / ရေချိုးခန်း",
        min_value=0,
        max_value=20,
        value=1,
        step=1,
    )

with col2:
    area = st.text_input(
        "Area / အကျယ်အဝန်း",
        value="850 sqft",
        placeholder="Example: 850 sqft or 40x60 ft",
    )

    price = st.text_input(
        "Price / ဈေးနှုန်း",
        value="2500 lakh MMK",
        placeholder="Example: 2500 lakh MMK / ၂၅၀၀ သိန်း",
)

    language_style = st.selectbox(
        "Language style / ဘာသာစကားပုံစံ",
        [
            "Burmese + English",
            "Burmese only",
            "English only",
            "Facebook-style mixed",
        ],
    )

    tone = st.selectbox(
        "Tone / ရေးသားမှုပုံစံ",
        [
            "Professional",
            "Friendly",
            "Luxury",
            "Simple",
            "Facebook marketing",
        ],
    )

special_features = st.text_area(
    "Special features / ထူးခြားချက်များ",
    value="near school, lift, car parking",
    placeholder="Example: near school, lift, car parking, good sunlight, quiet street",
    height=100,
)


# -----------------------------
# Generate button
# -----------------------------
st.markdown("---")

generate_button = st.button("✨ Generate Property Description / ကြော်ငြာစာသားထုတ်ရန်")


# -----------------------------
# Preview section
# -----------------------------
st.markdown(
    '<h3 class="preview-title">📋 Property Preview / အချက်အလက် အကျဉ်းချုပ်</h3>',
    unsafe_allow_html=True,
)

safe_location = location if location else "Sanchaung / စမ်းချောင်း"

st.markdown(
    f"""
    <div class="preview-box">
        <strong>Type / အမျိုးအစား:</strong> {property_type}<br>
        <strong>Location / တည်နေရာ:</strong> {safe_location}<br>
        <strong>Bedrooms / အိပ်ခန်း:</strong> {bedrooms}<br>
        <strong>Bathrooms / ရေချိုးခန်း:</strong> {bathrooms}<br>
        <strong>Area / အကျယ်အဝန်း:</strong> {area}<br>
        <strong>Price / ဈေးနှုန်း:</strong> {price}<br>
        <strong>Features / ထူးခြားချက်များ:</strong> {special_features}<br>
        <strong>Style / ပုံစံ:</strong> {language_style} · {tone}
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Output section
# -----------------------------
if generate_button:
    prompt = build_prompt(
        property_type=property_type,
        location=safe_location,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        area=area,
        price=price,
        special_features=special_features,
        language_style=language_style,
        tone=tone,
    )

    with st.spinner("Generating property description..."):
        generated_text = generate_description(prompt)

    st.markdown(
        '<h3 class="output-title">✍️ Generated Description / ထုတ်လုပ်ထားသော ကြော်ငြာစာသား</h3>',
        unsafe_allow_html=True,
    )

    st.markdown(generated_text)
    st.session_state.history.append(generated_text)

    st.download_button(
        label="⬇️Download Description",
        data=generated_text,
        file_name="property_description.txt",
        mime="text/plain"
        )

st.subheader("Previous Descriptions")

for i, item in enumerate(reversed(st.session_state.history)):
    with st.expander(f"Description {i + 1}"):
        st.write(item)

if st.button("Clear History"):
    st.session_state.history = []
    st.success("History cleared.")
