import os
import time
import streamlit as st
from google import genai
from dotenv import load_dotenv

# ============================================================
# CONFIG
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="Parth's AI Travel App",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# GEMINI API
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

try:
    if not api_key and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    st.error(
        "🔑 Gemini API key not found. "
        "Add GEMINI_API_KEY to your .env file or Streamlit Secrets."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- PAGE ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 0% 0%,
                rgba(59,130,246,0.14),
                transparent 30%
            ),
            radial-gradient(
                circle at 100% 10%,
                rgba(139,92,246,0.15),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #f8fbff 0%,
                #eef5ff 50%,
                #f7f2ff 100%
            );
    }

    .block-container {
        max-width: 1350px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0f172a 0%,
                #172554 45%,
                #312e81 100%
            );
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: white !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15);
    }

    /* ---------- HERO ---------- */

    .voyage-hero {
        position: relative;
        overflow: hidden;
        padding: 3.5rem 3rem;
        border-radius: 32px;
        background:
            linear-gradient(
                135deg,
                #0f172a 0%,
                #172554 40%,
                #3730a3 72%,
                #6d28d9 100%
            );
        box-shadow:
            0 25px 70px rgba(30,41,59,0.25);
        margin-bottom: 2.5rem;
    }

    .voyage-hero:before {
        content: "";
        position: absolute;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: rgba(96,165,250,0.18);
        right: -100px;
        top: -120px;
        filter: blur(4px);
    }

    .voyage-hero:after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        border-radius: 50%;
        background: rgba(192,132,252,0.14);
        left: 40%;
        bottom: -150px;
    }

    .hero-content {
        position: relative;
        z-index: 2;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.45rem 0.95rem;
        border-radius: 50px;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.20);
        color: #dbeafe;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        margin: 0;
        color: white;
        font-size: 4.7rem;
        line-height: 0.95;
        font-weight: 900;
        letter-spacing: -4px;
    }

    .hero-title span {
        color: #93c5fd;
    }

    .hero-description {
        margin-top: 1.2rem;
        max-width: 760px;
        color: #dbeafe;
        font-size: 1.12rem;
        line-height: 1.7;
    }

    .hero-features {
        display: flex;
        flex-wrap: wrap;
        gap: 0.7rem;
        margin-top: 1.6rem;
    }

    .hero-feature {
        padding: 0.5rem 0.85rem;
        border-radius: 50px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.13);
        color: #f8fafc;
        font-size: 0.82rem;
    }

    /* ---------- SECTION TITLES ---------- */

    .section-heading {
        font-size: 1.8rem;
        font-weight: 850;
        color: #111827;
        margin-top: 0.7rem;
        margin-bottom: 0.2rem;
    }

    .section-description {
        color: #64748b;
        font-size: 0.98rem;
        margin-bottom: 1.2rem;
    }

    /* ---------- DESTINATION CARDS ---------- */

    .destination-card {
        background: rgba(255,255,255,0.86);
        border: 1px solid rgba(148,163,184,0.20);
        border-radius: 22px;
        padding: 1.35rem;
        min-height: 170px;
        box-shadow:
            0 10px 30px rgba(15,23,42,0.06);
        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease;
    }

    .destination-card:hover {
        transform: translateY(-5px);
        box-shadow:
            0 18px 40px rgba(37,99,235,0.12);
    }

    .destination-icon {
        font-size: 2rem;
    }

    .destination-name {
        color: #111827;
        font-size: 1.15rem;
        font-weight: 800;
        margin-top: 0.5rem;
    }

    .destination-country {
        color: #6366f1;
        font-size: 0.8rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }

    .destination-text {
        color: #64748b;
        font-size: 0.86rem;
        line-height: 1.5;
        margin-top: 0.7rem;
    }

    /* ---------- METRIC CARDS ---------- */

    .custom-metric {
        background: rgba(255,255,255,0.9);
        border: 1px solid rgba(148,163,184,0.18);
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        box-shadow:
            0 8px 25px rgba(15,23,42,0.06);
    }

    .metric-icon {
        font-size: 1.45rem;
    }

    .metric-number {
        color: #111827;
        font-size: 1.25rem;
        font-weight: 850;
        margin-top: 0.3rem;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.8px;
        margin-top: 0.2rem;
    }

    /* ---------- BUTTON ---------- */

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
            0 8px 22px rgba(79,70,229,0.28);
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 13px 30px rgba(79,70,229,0.38);
    }

    /* ---------- INPUTS ---------- */

    .stTextInput input,
    .stNumberInput input {
        border-radius: 12px;
    }

    .stSelectbox > div > div {
        border-radius: 12px;
    }

    /* ---------- DOWNLOAD ---------- */

    .stDownloadButton > button {
        border-radius: 13px;
        font-weight: 750;
        border: 1px solid #c7d2fe;
        background: #eef2ff;
        color: #3730a3;
    }

    .stDownloadButton > button:hover {
        background: #e0e7ff;
    }

    /* ---------- ALERTS ---------- */

    div[data-testid="stAlert"] {
        border-radius: 15px;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 768px) {

        .voyage-hero {
            padding: 2.2rem 1.5rem;
            border-radius: 24px;
        }

        .hero-title {
            font-size: 3.1rem;
            letter-spacing: -2px;
        }

        .hero-description {
            font-size: 0.98rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HERO
# IMPORTANT:
# HTML IS INSIDE THIS MARKDOWN BLOCK ONLY.
# ============================================================

st.markdown(
    """
    <div class="voyage-hero">

        <div class="hero-content">

            <div class="hero-badge">
                ✨ AI-POWERED TRAVEL ASSISTANT
            </div>

            <div class="hero-title">
                Voyage<span>AI</span> ✈️
            </div>

            <div class="hero-description">
                Plan unforgettable journeys with your personal AI travel
                companion. Discover amazing destinations, local food,
                hidden gems, exciting activities and perfectly structured
                itineraries.
            </div>

            <div class="hero-features">
                <div class="hero-feature">🗺️ Smart Itineraries</div>
                <div class="hero-feature">🍜 Local Food</div>
                <div class="hero-feature">💎 Hidden Gems</div>
                <div class="hero-feature">💰 Budget Planning</div>
                <div class="hero-feature">🎒 Personalized Trips</div>
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("✈️ VoyageAI")

    st.caption("Build your perfect trip")

    st.divider()

    st.subheader("📍 Destination")

    location = st.text_input(
        "Destination",
        placeholder="Paris, Tokyo, Goa...",
        label_visibility="collapsed",
    )

    st.subheader("📅 Duration")

    days = st.number_input(
        "Trip duration",
        min_value=1,
        max_value=30,
        value=5,
        step=1,
        label_visibility="collapsed",
    )

    st.subheader("💰 Budget")

    budget = st.selectbox(
        "Budget",
        ["Budget", "Moderate", "Luxury"],
        label_visibility="collapsed",
    )

    st.subheader("👥 Travel Group")

    travel_type = st.radio(
        "Travel group",
        ["Solo", "Friends", "Family", "Couple"],
        label_visibility="collapsed",
    )

    st.subheader("✨ Interests")

    interests = st.multiselect(
        "Interests",
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
        default=[
            "🍜 Food",
            "🏛️ Culture",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    plan_trip = st.button(
        "🚀 CREATE MY TRIP",
        use_container_width=True,
    )

    st.divider()

    st.caption("Made with ❤️ by Parth")
    st.caption("Streamlit + Gemini")


# ============================================================
# DESIGN YOUR JOURNEY
# ============================================================

st.markdown(
    """
    <div class="section-heading">
        🌍 Design Your Journey
    </div>

    <div class="section-description">
        Tell VoyageAI what kind of adventure you're looking for.
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DESTINATION INSPIRATION
# ============================================================

st.markdown(
    """
    <div class="section-heading">
        ✨ Get Inspired
    </div>

    <div class="section-description">
        Some ideas for your next adventure.
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
        <div class="destination-card">
            <div class="destination-icon">🗼</div>
            <div class="destination-name">Paris</div>
            <div class="destination-country">🇫🇷 FRANCE</div>
            <div class="destination-text">
                Art, romance, cafés, museums and unforgettable cuisine.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="destination-card">
            <div class="destination-icon">🗻</div>
            <div class="destination-name">Tokyo</div>
            <div class="destination-country">🇯🇵 JAPAN</div>
            <div class="destination-text">
                Ancient culture, futuristic cities, anime and amazing food.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="destination-card">
            <div class="destination-icon">🏝️</div>
            <div class="destination-name">Bali</div>
            <div class="destination-country">🇮🇩 INDONESIA</div>
            <div class="destination-text">
                Tropical beaches, temples, waterfalls and peaceful escapes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        """
        <div class="destination-card">
            <div class="destination-icon">🏙️</div>
            <div class="destination-name">Dubai</div>
            <div class="destination-country">🇦🇪 UAE</div>
            <div class="destination-text">
                Luxury, shopping, architecture and desert adventures.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# TRIP PREVIEW
# ============================================================

st.markdown(
    """
    <div class="section-heading">
        📊 Trip Preview
    </div>

    <div class="section-description">
        Your current travel preferences.
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="custom-metric">
            <div class="metric-icon">📅</div>
            <div class="metric-number">{days}</div>
            <div class="metric-label">DAYS</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="custom-metric">
            <div class="metric-icon">💰</div>
            <div class="metric-number">{budget}</div>
            <div class="metric-label">BUDGET</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="custom-metric">
            <div class="metric-icon">👥</div>
            <div class="metric-number">{travel_type}</div>
            <div class="metric-label">TRAVEL STYLE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        f"""
        <div class="custom-metric">
            <div class="metric-icon">✨</div>
            <div class="metric-number">{len(interests)}</div>
            <div class="metric-label">INTERESTS</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# DESTINATION PREVIEW
# ============================================================

if location.strip():

    st.divider()

    st.subheader(f"📍 Ready for {location}?")

    st.info(
        f"You're planning a **{days}-day {budget.lower()} trip** "
        f"to **{location}**, travelling **{travel_type.lower()}**."
    )


# ============================================================
# GENERATE TRIP
# ============================================================

if plan_trip:

    if not location.strip():

        st.warning(
            "📍 Enter a destination in the sidebar first."
        )

    else:

        interest_text = (
            ", ".join(interests)
            if interests
            else "General sightseeing and local experiences"
        )

        prompt = f"""
You are VoyageAI, an expert professional travel planner.

Create a personalized travel itinerary.

DESTINATION:
{location}

DURATION:
{days} days

BUDGET:
{budget}

TRAVELLING WITH:
{travel_type}

INTERESTS:
{interest_text}

Create a practical, detailed and enjoyable itinerary.

Use Markdown.

Structure:

# ✈️ {location} Travel Guide

## 🌟 Trip Overview

Give a personalized overview.

## 🗓️ Day-by-Day Itinerary

Create a detailed itinerary for every day.

For each day include:

### Day X

🌅 Morning:
Activities and places.

🍴 Lunch:
Food suggestions.

🗺️ Afternoon:
Sightseeing and activities.

🌆 Evening:
Evening activities.

🍽️ Dinner:
Local food suggestions.

## 🏛️ Must-Visit Places

List important attractions with short explanations.

## 🍜 Food & Local Experiences

Recommend local dishes and authentic experiences.

## 💎 Hidden Gems

Suggest less touristy places or experiences.

## 💰 Estimated Budget

Give approximate estimates for:

🏨 Accommodation
🍴 Food
🚕 Transportation
🎟️ Activities
🛍️ Miscellaneous

Adjust everything for the selected budget.

## 🎒 Travel Tips

Include transportation, safety, local customs,
areas to stay and useful booking advice.

## 🌦️ Best Time to Visit

Explain weather and seasonal considerations.

## 🧳 Packing Checklist

Create a practical packing list.

## ⭐ Final Recommendations

Finish with personalized recommendations.

IMPORTANT:
- Make everything specific to the destination.
- Consider the budget.
- Consider the travel group.
- Consider the interests.
- Avoid generic filler.
- Do not invent live prices.
- Do not invent opening hours.
- Clearly label prices as approximate.
- Do not claim real-time availability.
- Use Markdown.
- Do not use HTML.
"""

        # ====================================================
        # GENERATION STATUS
        # ====================================================

        with st.status(
            "✈️ VoyageAI is planning your adventure...",
            expanded=True,
        ) as status:

            st.write(
                f"🔍 Exploring {location}..."
            )

            time.sleep(0.5)

            st.write(
                f"📅 Building your {days}-day itinerary..."
            )

            time.sleep(0.5)

            st.write(
                f"💰 Optimizing for your {budget.lower()} budget..."
            )

            time.sleep(0.5)

            st.write(
                f"🎒 Personalizing your {travel_type.lower()} adventure..."
            )

            time.sleep(0.5)

            st.write(
                "✨ Generating your travel guide..."
            )

            try:

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt,
                )

                status.update(
                    label="✅ Your adventure is ready!",
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
                    f"Gemini could not generate your itinerary:\n\n{error}"
                )

                st.stop()

        # ====================================================
        # RESULT
        # ====================================================

        st.divider()

        st.markdown(
            """
            <div class="section-heading">
                🗺️ Your Personalized Travel Plan
            </div>

            <div class="section-description">
                Your itinerary has been created by VoyageAI.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.success(
            f"🎉 Your {days}-day {location} adventure is ready!"
        )

        st.markdown(response.text)

        # ====================================================
        # DOWNLOAD
        # ====================================================

        st.divider()

        st.subheader("📥 Save Your Itinerary")

        st.download_button(
            "📄 Download Travel Plan",
            data=response.text,
            file_name=(
                f"{location.replace(' ', '_')}_travel_plan.md"
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
        padding:1.5rem;
        color:#64748b;
        font-size:0.9rem;
    ">
        ✈️ <b>Parth's AI Travel App</b>
        &nbsp; • &nbsp;
        Powered by Gemini
        &nbsp; • &nbsp;
        Built with Streamlit
        <br>
        <small>
            Plan smarter. Explore more. Travel unforgettable. 🌍
        </small>
    </div>
    """,
    unsafe_allow_html=True,
)