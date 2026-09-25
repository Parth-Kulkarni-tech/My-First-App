import os
import time
import streamlit as st
from google import genai
from dotenv import load_dotenv

# ============================================================
# APP CONFIGURATION
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="Parth's AI Travel App",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# GEMINI API CONFIGURATION
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

try:
    if not api_key and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    st.error(
        "🔑 Gemini API key is missing.\n\n"
        "For local use, add GEMINI_API_KEY to your .env file. "
        "For Streamlit Cloud, add GEMINI_API_KEY to Secrets."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# ============================================================
# PREMIUM VISUAL STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(59, 130, 246, 0.12),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(168, 85, 247, 0.13),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #f8fbff 0%,
                #eef5ff 48%,
                #f7f1ff 100%
            );
    }

    .block-container {
        max-width: 1350px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0f172a 0%,
                #172554 48%,
                #312e81 100%
            );
        border-right: 1px solid rgba(255,255,255,0.12);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15);
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero-box {
        padding: 3rem 3rem 2.8rem 3rem;
        border-radius: 30px;
        background:
            linear-gradient(
                135deg,
                #0f172a 0%,
                #172554 45%,
                #4c1d95 100%
            );
        box-shadow:
            0 25px 60px rgba(30, 41, 59, 0.22);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }

    .hero-box::before {
        content: "";
        position: absolute;
        width: 250px;
        height: 250px;
        border-radius: 50%;
        background: rgba(96, 165, 250, 0.18);
        top: -100px;
        right: -50px;
        filter: blur(5px);
    }

    .hero-box::after {
        content: "";
        position: absolute;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: rgba(192, 132, 252, 0.15);
        bottom: -80px;
        left: 20%;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.45rem 0.9rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);
        color: #dbeafe;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 4.4rem;
        line-height: 1;
        font-weight: 900;
        color: white;
        letter-spacing: -3px;
        margin-bottom: 0.8rem;
    }

    .hero-subtitle {
        color: #dbeafe;
        font-size: 1.15rem;
        line-height: 1.7;
        max-width: 760px;
    }

    /* ======================================================
       SECTION HEADERS
       ====================================================== */

    .section-title {
        color: #111827;
        font-size: 1.8rem;
        font-weight: 800;
        margin-top: 1.5rem;
        margin-bottom: 0.25rem;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }

    /* ======================================================
       CARDS
       ====================================================== */

    .travel-card {
        background: rgba(255,255,255,0.86);
        border: 1px solid rgba(148,163,184,0.18);
        border-radius: 20px;
        padding: 1.35rem;
        min-height: 145px;
        box-shadow:
            0 8px 25px rgba(15,23,42,0.06);
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .travel-card:hover {
        transform: translateY(-4px);
        box-shadow:
            0 15px 35px rgba(37,99,235,0.12);
    }

    .travel-card-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.3rem;
    }

    .travel-card-location {
        color: #6366f1;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }

    .travel-card-text {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* ======================================================
       METRIC CARDS
       ====================================================== */

    .metric-box {
        background: rgba(255,255,255,0.9);
        border: 1px solid rgba(148,163,184,0.18);
        border-radius: 18px;
        padding: 1.15rem;
        text-align: center;
        box-shadow:
            0 7px 22px rgba(15,23,42,0.06);
    }

    .metric-icon {
        font-size: 1.4rem;
        margin-bottom: 0.3rem;
    }

    .metric-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: #111827;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.78rem;
        margin-top: 0.2rem;
    }

    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        border: none;
        border-radius: 14px;
        min-height: 3rem;
        font-weight: 800;
        color: white;
        background:
            linear-gradient(
                135deg,
                #2563eb,
                #4f46e5,
                #7c3aed
            );
        box-shadow:
            0 8px 20px rgba(79,70,229,0.25);
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 12px 28px rgba(79,70,229,0.35);
    }

    /* ======================================================
       INPUTS
       ====================================================== */

    .stTextInput input,
    .stNumberInput input {
        border-radius: 12px;
        border: 1px solid #dbe3f0;
        background: rgba(255,255,255,0.9);
    }

    .stSelectbox > div > div {
        border-radius: 12px;
        background: rgba(255,255,255,0.9);
    }

    /* ======================================================
       ALERTS
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 15px;
    }

    /* ======================================================
       METRICS
       ====================================================== */

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.88);
        border-radius: 18px;
        padding: 1rem;
        border: 1px solid rgba(148,163,184,0.16);
        box-shadow:
            0 7px 22px rgba(15,23,42,0.05);
    }

    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {
        border-color: rgba(148,163,184,0.2);
    }

    /* ======================================================
       DOWNLOAD BUTTON
       ====================================================== */

    .stDownloadButton > button {
        width: 100%;
        border-radius: 13px;
        border: 1px solid #c7d2fe;
        background: #eef2ff;
        color: #3730a3;
        font-weight: 700;
    }

    .stDownloadButton > button:hover {
        background: #e0e7ff;
        border-color: #818cf8;
    }

    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 768px) {

        .hero-box {
            padding: 2rem 1.4rem;
            border-radius: 22px;
        }

        .hero-title {
            font-size: 3rem;
            letter-spacing: -2px;
        }

        .hero-subtitle {
            font-size: 1rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-box">

        <div class="hero-badge">
            ✨ AI-POWERED TRAVEL ASSISTANT
        </div>

        <div class="hero-title">
            VoyageAI
        </div>

        <div class="hero-subtitle">
            Plan unforgettable journeys with your personal AI travel
            companion. Discover amazing places, local food, hidden gems,
            activities and perfectly structured itineraries.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ✈️ VoyageAI")

    st.caption("Your personal AI travel planner")

    st.divider()

    st.markdown("### 📍 Destination")

    location = st.text_input(
        "Where are you going?",
        placeholder="Paris, Tokyo, Goa...",
        label_visibility="collapsed",
    )

    st.markdown("### 📅 Duration")

    days = st.number_input(
        "Number of days",
        min_value=1,
        max_value=30,
        value=5,
        step=1,
        label_visibility="collapsed",
    )

    st.markdown("### 💰 Budget")

    budget = st.selectbox(
        "Choose your budget",
        ["Budget", "Moderate", "Luxury"],
        label_visibility="collapsed",
    )

    st.markdown("### 👥 Travel Style")

    travel_type = st.radio(
        "Who are you travelling with?",
        ["Solo", "Friends", "Family", "Couple"],
        label_visibility="collapsed",
    )

    st.markdown("### ✨ Interests")

    interests = st.multiselect(
        "What do you enjoy?",
        [
            "🍜 Food",
            "🏛️ Culture",
            "🌿 Nature",
            "🏔️ Adventure",
            "🛍️ Shopping",
            "🌃 Nightlife",
            "📸 Photography",
            "🏖️ Relaxation",
            "📚 History",
        ],
        default=["🍜 Food", "🏛️ Culture"],
        label_visibility="collapsed",
    )

    st.divider()

    plan_trip = st.button(
        "🚀 Create My Trip",
        use_container_width=True,
    )

    st.divider()

    st.caption("Built with ❤️ by Parth")
    st.caption("Powered by Streamlit + Gemini")

# ============================================================
# MAIN SECTION
# ============================================================

st.markdown(
    '<div class="section-title">🌍 Design Your Journey</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">'
    'Choose your destination and preferences. VoyageAI will handle the rest.'
    '</div>',
    unsafe_allow_html=True,
)

# ============================================================
# INSPIRATION
# ============================================================

st.markdown(
    '<div class="section-title">✨ Get Inspired</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">'
    'A few destinations to spark your imagination.'
    '</div>',
    unsafe_allow_html=True,
)

card1, card2, card3, card4 = st.columns(4)

with card1:
    st.markdown(
        """
        <div class="travel-card">
            <div class="travel-card-title">🗼 Paris</div>
            <div class="travel-card-location">🇫🇷 France</div>
            <div class="travel-card-text">
                Art, romance, cafés, museums and unforgettable cuisine.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with card2:
    st.markdown(
        """
        <div class="travel-card">
            <div class="travel-card-title">🗻 Tokyo</div>
            <div class="travel-card-location">🇯🇵 Japan</div>
            <div class="travel-card-text">
                Futuristic cities, ancient culture, anime and amazing food.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with card3:
    st.markdown(
        """
        <div class="travel-card">
            <div class="travel-card-title">🏝️ Bali</div>
            <div class="travel-card-location">🇮🇩 Indonesia</div>
            <div class="travel-card-text">
                Tropical beaches, temples, waterfalls and peaceful escapes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with card4:
    st.markdown(
        """
        <div class="travel-card">
            <div class="travel-card-title">🏙️ Dubai</div>
            <div class="travel-card-location">🇦🇪 UAE</div>
            <div class="travel-card-text">
                Luxury, architecture, shopping, desert adventures and nightlife.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# TRIP PREVIEW
# ============================================================

st.markdown(
    '<div class="section-title">📊 Trip Preview</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">'
    'Your selected preferences at a glance.'
    '</div>',
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-icon">📅</div>
            <div class="metric-value">{days}</div>
            <div class="metric-label">DAYS</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-icon">💰</div>
            <div class="metric-value">{budget}</div>
            <div class="metric-label">BUDGET</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-icon">👥</div>
            <div class="metric-value">{travel_type}</div>
            <div class="metric-label">TRAVEL STYLE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-icon">✨</div>
            <div class="metric-value">{len(interests)}</div>
            <div class="metric-label">INTERESTS</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# SELECTED DESTINATION
# ============================================================

if location.strip():

    st.markdown(
        '<div class="section-title">📍 Your Destination</div>',
        unsafe_allow_html=True,
    )

    st.info(
        f"You're planning a **{days}-day {budget.lower()} trip to "
        f"{location}** with a **{travel_type.lower()}** travel style."
    )

# ============================================================
# AI GENERATION
# ============================================================

if plan_trip:

    if not location.strip():

        st.warning(
            "📍 Please enter a destination in the sidebar first."
        )

    else:

        interest_text = (
            ", ".join(interests)
            if interests
            else "General sightseeing and local experiences"
        )

        prompt = f"""
You are VoyageAI, a world-class professional travel planner.

Create a personalized travel itinerary using the following information:

DESTINATION
{location}

TRIP LENGTH
{days} days

BUDGET
{budget}

TRAVEL GROUP
{travel_type}

INTERESTS
{interest_text}

Create a detailed but practical itinerary.

Use Markdown.

Structure your answer exactly around these sections:

# ✈️ {location} Travel Guide

## 🌟 Trip Overview

Give a personalized overview of the destination.

## 🗓️ Day-by-Day Itinerary

Create a plan for every day.

For each day include:

### Day X

**🌅 Morning**
Activities and places.

**🍴 Lunch**
Food suggestions.

**🗺️ Afternoon**
Activities and sightseeing.

**🌆 Evening**
Things to do.

**🍽️ Dinner**
Local food suggestions.

## 🏛️ Must-Visit Attractions

List important attractions and briefly explain them.

## 🍜 Food & Local Experiences

Recommend local dishes, food experiences and authentic activities.

## 💎 Hidden Gems

Suggest less touristy experiences when appropriate.

## 💰 Estimated Budget

Break down approximate costs for:

- 🏨 Accommodation
- 🍜 Food
- 🚕 Transportation
- 🎟️ Activities
- 🛍️ Miscellaneous

Keep recommendations appropriate for the selected budget.

## 🎒 Travel Tips

Include:

- Transportation
- Local customs
- Safety
- Areas to stay
- Booking advice
- Tourist mistakes to avoid

## 🌦️ Best Time to Visit

Explain weather and seasonal considerations.

## 🧳 Packing Checklist

Give a practical packing list.

## ⭐ Final Recommendations

Give a concise personalized summary.

IMPORTANT:

- Make the plan specific to {location}.
- Do not give generic filler.
- Consider the travel group.
- Consider the budget.
- Consider the selected interests.
- Keep the itinerary realistic.
- Do not invent exact opening hours or live prices.
- If prices are mentioned, clearly describe them as approximate.
- Do not claim real-time availability.
- Use emojis naturally.
"""

        # ====================================================
        # GENERATION STATUS
        # ====================================================

        with st.status(
            "✈️ VoyageAI is preparing your adventure...",
            expanded=True,
        ) as status:

            st.write(
                f"🔍 Exploring **{location}**..."
            )

            time.sleep(0.6)

            st.write(
                f"📅 Building your **{days}-day itinerary**..."
            )

            time.sleep(0.6)

            st.write(
                f"💰 Optimizing for your **{budget.lower()} budget**..."
            )

            time.sleep(0.6)

            st.write(
                f"🎒 Personalizing the trip for **{travel_type.lower()} travel**..."
            )

            time.sleep(0.6)

            st.write(
                "✨ Generating your AI travel guide..."
            )

            try:

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt,
                )

                status.update(
                    label="✅ Your trip is ready!",
                    state="complete",
                    expanded=False,
                )

            except Exception as error:

                status.update(
                    label="❌ Generation failed",
                    state="error",
                    expanded=True,
                )

                st.error(
                    f"Something went wrong while generating your trip:\n\n{error}"
                )

                st.stop()

        # ====================================================
        # RESULT HEADER
        # ====================================================

        st.markdown(
            '<div class="section-title">🗺️ Your AI Travel Plan</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">'
            'Your personalized itinerary has been generated by VoyageAI.'
            '</div>',
            unsafe_allow_html=True,
        )

        st.success(
            f"🎉 Your {days}-day {location} adventure is ready!"
        )

        # ====================================================
        # ITINERARY
        # ====================================================

        st.markdown(response.text)

        # ====================================================
        # DOWNLOAD
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">📥 Save Your Adventure</div>',
            unsafe_allow_html=True,
        )

        st.caption(
            "Download your itinerary and keep it with you during your trip."
        )

        st.download_button(
            label="📄 Download Travel Plan",
            data=response.text,
            file_name=(
                f"{location.strip().replace(' ', '_')}_travel_plan.md"
            ),
            mime="text/markdown",
            use_container_width=True,
        )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:1.5rem 0;
        color:#64748b;
        font-size:0.9rem;
    ">
        ✈️ <b>Parth's AI Travel App</b>
        &nbsp; • &nbsp;
        Powered by Gemini
        &nbsp; • &nbsp;
        Built with Streamlit
        <br>
        <span style="font-size:0.8rem;">
            Plan smarter. Explore more. Travel unforgettable. 🌍
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)