import streamlit as st
from google import genai
from dotenv import load_dotenv
import re

# =========================================================
# CONFIG
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="VoyageAI | Smart Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

client = genai.Client()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(56,189,248,.12), transparent 25%),
            radial-gradient(circle at 90% 20%, rgba(168,85,247,.12), transparent 25%),
            linear-gradient(135deg, #f8fafc 0%, #eef6ff 50%, #faf5ff 100%);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- ANIMATIONS ---------- */

    @keyframes float {
        0%, 100% {
            transform: translateY(0px) rotate(0deg);
        }

        50% {
            transform: translateY(-10px) rotate(2deg);
        }
    }

    @keyframes gradientMove {
        0% {
            background-position: 0% 50%;
        }

        50% {
            background-position: 100% 50%;
        }

        100% {
            background-position: 0% 50%;
        }
    }

    @keyframes pulseGlow {
        0%, 100% {
            box-shadow: 0 0 0 rgba(59,130,246,0);
        }

        50% {
            box-shadow: 0 0 35px rgba(59,130,246,.25);
        }
    }

    /* ---------- HERO ---------- */

    .hero {
        position: relative;
        overflow: hidden;
        padding: 3rem 3rem 2.5rem;
        border-radius: 30px;
        margin-bottom: 2rem;

        background:
            linear-gradient(
                120deg,
                rgba(15,23,42,.97),
                rgba(30,64,175,.94),
                rgba(88,28,135,.94)
            );

        color: white;
        box-shadow: 0 25px 60px rgba(15,23,42,.18);
    }

    .hero::before {
        content: "✈";
        position: absolute;
        right: 8%;
        top: 15%;
        font-size: 7rem;
        opacity: .10;
        animation: float 5s ease-in-out infinite;
    }

    .hero::after {
        content: "🌍";
        position: absolute;
        right: 25%;
        bottom: -25px;
        font-size: 6rem;
        opacity: .08;
        animation: float 7s ease-in-out infinite;
    }

    .hero-badge {
        display: inline-block;
        padding: .4rem .8rem;
        border-radius: 999px;
        background: rgba(255,255,255,.12);
        border: 1px solid rgba(255,255,255,.18);
        font-size: .8rem;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 3.4rem;
        font-weight: 900;
        line-height: 1.05;
        margin: 0;
        background: linear-gradient(
            90deg,
            #ffffff,
            #bae6fd,
            #ddd6fe,
            #ffffff
        );
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientMove 7s ease infinite;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: rgba(255,255,255,.78);
        max-width: 720px;
        margin-top: 1rem;
        line-height: 1.7;
    }

    /* ---------- SECTION TITLES ---------- */

    .section-title {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 1rem;
        margin-bottom: .25rem;
    }

    .section-subtitle {
        color: #64748b;
        margin-bottom: 1.3rem;
    }

    /* ---------- CARDS ---------- */

    .info-card {
        background: rgba(255,255,255,.72);
        border: 1px solid rgba(148,163,184,.20);
        border-radius: 22px;
        padding: 1.3rem;
        box-shadow: 0 10px 30px rgba(15,23,42,.07);
        backdrop-filter: blur(15px);
        margin-bottom: 1rem;
    }

    .info-card:hover {
        animation: pulseGlow 2s infinite;
    }

    .card-icon {
        font-size: 2rem;
        margin-bottom: .4rem;
    }

    .card-title {
        font-size: 1.05rem;
        font-weight: 750;
        color: #0f172a;
    }

    .card-text {
        color: #64748b;
        font-size: .9rem;
    }

    /* ---------- DESTINATION CARD ---------- */

    .destination-card {
        padding: 1.8rem;
        border-radius: 24px;
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,.95),
                rgba(239,246,255,.85)
            );

        border: 1px solid rgba(59,130,246,.12);
        box-shadow: 0 15px 40px rgba(30,64,175,.08);
        margin-bottom: 1.5rem;
    }

    .destination-name {
        font-size: 2rem;
        font-weight: 850;
        color: #0f172a;
    }

    .destination-tag {
        display: inline-block;
        margin-top: .5rem;
        margin-right: .4rem;
        padding: .3rem .7rem;
        border-radius: 999px;
        background: #e0f2fe;
        color: #0369a1;
        font-size: .75rem;
        font-weight: 700;
    }

    /* ---------- METRICS ---------- */

    .metric-card {
        text-align: center;
        padding: 1rem;
        border-radius: 18px;
        background: rgba(255,255,255,.7);
        border: 1px solid rgba(148,163,184,.15);
    }

    .metric-number {
        font-size: 1.7rem;
        font-weight: 850;
        color: #2563eb;
    }

    .metric-label {
        font-size: .78rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: .7px;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: .8rem;
        padding: 2rem 0 1rem;
    }

    /* ---------- BUTTON ---------- */

    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 14px;
        padding: .75rem 1rem;
        font-weight: 750;
        background: linear-gradient(
            90deg,
            #2563eb,
            #7c3aed
        );
        color: white;
        transition: all .2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(37,99,235,.25);
    }

    /* ---------- INPUTS ---------- */

    div[data-baseweb="input"] {
        border-radius: 12px;
    }

    div[data-baseweb="select"] > div {
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✨ AI-POWERED TRAVEL PLANNER
        </div>

        <h1 class="hero-title">
            VoyageAI
        </h1>

        <p class="hero-subtitle">
            Your intelligent travel companion for unforgettable adventures.
            Build personalized itineraries, discover hidden gems, explore local
            food and travel smarter — all in seconds.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🧭 Trip Controls")

    st.caption("Customize your adventure")

    location = st.text_input(
        "📍 Destination",
        placeholder="e.g. Tokyo, Paris, Goa..."
    )

    days = st.slider(
        "📅 Trip Duration",
        min_value=1,
        max_value=30,
        value=5
    )

    budget = st.selectbox(
        "💰 Budget Style",
        [
            "Budget",
            "Moderate",
            "Luxury"
        ]
    )

    travel_type = st.selectbox(
        "👥 Travel Group",
        [
            "Solo",
            "Couple",
            "Friends",
            "Family"
        ]
    )

    interests = st.multiselect(
        "✨ Interests",
        [
            "🏛️ History & Culture",
            "🍜 Food & Cuisine",
            "🏔️ Adventure",
            "🏖️ Beaches",
            "🌿 Nature",
            "🛍️ Shopping",
            "🎨 Art & Museums",
            "🌃 Nightlife",
            "📸 Photography"
        ],
        default=["🍜 Food & Cuisine", "📸 Photography"]
    )

    travel_pace = st.select_slider(
        "🚶 Travel Pace",
        options=[
            "Relaxed",
            "Balanced",
            "Packed"
        ],
        value="Balanced"
    )

    st.divider()

    st.markdown(
        """
        ### 💡 Voyage Tip

        The more specific your interests are, the more personalized your
        itinerary becomes.
        """
    )


# =========================================================
# MAIN CONTENT
# =========================================================

st.markdown(
    '<div class="section-title">🌍 Design Your Journey</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Tell VoyageAI what kind of adventure you want.</div>',
    unsafe_allow_html=True
)


# Quick destination examples

cols = st.columns(4)

quick_destinations = [
    ("🗼", "Paris"),
    ("🏯", "Tokyo"),
    ("🌴", "Bali"),
    ("🏔️", "Switzerland"),
]

for col, (emoji, name) in zip(cols, quick_destinations):

    with col:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="card-icon">{emoji}</div>
                <div class="card-title">{name}</div>
                <div class="card-text">Explore the world</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# TRIP SUMMARY
# =========================================================

if location:

    st.markdown(
        f"""
        <div class="destination-card">

            <div class="destination-name">
                📍 {location}
            </div>

            <span class="destination-tag">
                📅 {days} Days
            </span>

            <span class="destination-tag">
                💰 {budget}
            </span>

            <span class="destination-tag">
                👥 {travel_type}
            </span>

            <span class="destination-tag">
                🚶 {travel_pace}
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# GENERATION BUTTON
# =========================================================

st.markdown("### ✈️ Ready for takeoff?")

plan_trip = st.button(
    "🚀 Generate My Dream Itinerary"
)


# =========================================================
# AI GENERATION
# =========================================================

if plan_trip:

    if not location.strip():

        st.error(
            "📍 Please enter a destination before launching your trip."
        )

    else:

        interest_text = ", ".join(interests)

        prompt = f"""
You are VoyageAI, an expert international travel planner.

Create a highly personalized travel plan for:

Destination:
{location}

Duration:
{days} days

Budget:
{budget}

Travel group:
{travel_type}

Interests:
{interest_text}

Travel pace:
{travel_pace}

Your response must be practical, visually organized and easy to follow.

Include:

1. 🌍 TRIP OVERVIEW
   - Destination personality
   - Best experiences for this traveler
   - Overall travel strategy

2. 🗓️ DAY-BY-DAY ITINERARY
   For every day include:
   - Morning
   - Afternoon
   - Evening
   - Food recommendation
   - Approximate local travel time
   - One optional alternative

3. 🏆 TOP EXPERIENCES
   Give 5-8 must-do experiences.

4. 💎 HIDDEN GEMS
   Give lesser-known places that fit the travel style.

5. 🍜 FOOD GUIDE
   Include:
   - Local dishes
   - Street food
   - Restaurant styles
   - Foods to try

6. 💰 BUDGET GUIDE
   Provide approximate spending categories:
   - Accommodation
   - Food
   - Local transport
   - Attractions
   - Miscellaneous

7. 🎒 PACKING LIST
   Make it appropriate for the destination and trip.

8. 🚨 TRAVEL SMART
   Include practical advice such as:
   - Local etiquette
   - Transport tips
   - Common tourist mistakes
   - Safety considerations

9. 📸 PHOTO SPOTS
   Suggest scenic or memorable photography locations.

10. 🌟 FINAL TIPS
   Give a concise list of things that will make the trip smoother.

Do not invent exact opening hours, ticket prices, transport schedules,
or current events. Clearly indicate when information should be checked
locally.
"""

        try:

            with st.status(
                "✈️ VoyageAI is planning your adventure...",
                expanded=True
            ) as status:

                st.write("🧠 Understanding your travel preferences...")
                st.write("🗺️ Building the perfect route...")
                st.write("🍜 Finding food experiences...")
                st.write("💎 Searching for hidden-gem ideas...")
                st.write("✨ Personalizing your itinerary...")

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt,
                )

                status.update(
                    label="🌟 Your journey is ready!",
                    state="complete",
                    expanded=False
                )

            # =================================================
            # RESULTS
            # =================================================

            st.balloons()

            st.success(
                f"🎉 Your {days}-day {location} adventure is ready!"
            )

            # Summary metrics

            m1, m2, m3, m4 = st.columns(4)

            with m1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-number">{days}</div>
                        <div class="metric-label">Days</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with m2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-number">{budget}</div>
                        <div class="metric-label">Budget</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with m3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-number">{travel_type}</div>
                        <div class="metric-label">Travel Style</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with m4:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-number">✨</div>
                        <div class="metric-label">AI Planned</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.divider()

            # AI response

            st.markdown(
                "## 🗺️ Your Personalized Journey"
            )

            st.markdown(response.text)

            # Download itinerary

            st.download_button(
                label="📥 Download Itinerary",
                data=response.text,
                file_name=f"{location.replace(' ', '_')}_VoyageAI_Itinerary.txt",
                mime="text/plain",
            )

        except Exception as e:

            st.error(
                "⚠️ Something went wrong while generating your itinerary."
            )

            st.caption(
                "Please check your Gemini API configuration and try again."
            )

            with st.expander("Technical details"):
                st.code(str(e))


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        ✈️ <b>VoyageAI</b> · Travel smarter. Explore farther. 🌍

        <br><br>

        Built with ❤️ using Streamlit + Gemini

    </div>
    """,
    unsafe_allow_html=True
)