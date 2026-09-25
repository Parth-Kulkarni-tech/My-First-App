import streamlit as st
from google import genai
from dotenv import load_dotenv

# ============================================================
# SETUP
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="VoyageAI | Smart Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Gemini client
client = genai.Client()


# ============================================================
# CUSTOM CSS
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
                circle at 90% 10%,
                rgba(139, 92, 246, 0.12),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #f8fafc 0%,
                #eef6ff 50%,
                #faf5ff 100%
            );
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Hide Streamlit menu/footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ======================================================
       ANIMATIONS
       ====================================================== */

    @keyframes floatPlane {
        0% {
            transform: translateY(0px) rotate(-4deg);
        }

        50% {
            transform: translateY(-12px) rotate(4deg);
        }

        100% {
            transform: translateY(0px) rotate(-4deg);
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

    @keyframes glow {
        0%, 100% {
            opacity: 0.55;
        }

        50% {
            opacity: 1;
        }
    }

    /* ======================================================
       HERO
       ====================================================== */

    .voyage-hero {
        position: relative;
        overflow: hidden;

        padding: 3rem 3rem 2.8rem;

        border-radius: 30px;

        background:
            linear-gradient(
                125deg,
                #0f172a,
                #1e3a8a,
                #4338ca,
                #581c87
            );

        background-size: 300% 300%;

        animation: gradientMove 12s ease infinite;

        color: white;

        box-shadow:
            0 25px 60px rgba(15, 23, 42, 0.25);

        margin-bottom: 2rem;
    }

    .voyage-hero::before {
        content: "✈️";

        position: absolute;

        right: 7%;
        top: 10%;

        font-size: 7rem;

        opacity: 0.13;

        animation: floatPlane 5s ease-in-out infinite;
    }

    .voyage-hero::after {
        content: "🌍";

        position: absolute;

        right: 27%;
        bottom: -30px;

        font-size: 7rem;

        opacity: 0.08;

        animation: floatPlane 8s ease-in-out infinite;
    }

    .hero-badge {
        display: inline-block;

        padding: 0.45rem 0.9rem;

        border-radius: 999px;

        background: rgba(255,255,255,0.12);

        border: 1px solid rgba(255,255,255,0.2);

        font-size: 0.75rem;

        font-weight: 700;

        letter-spacing: 1.2px;

        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 3.6rem;

        font-weight: 900;

        line-height: 1;

        margin: 0;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #bae6fd,
                #ddd6fe,
                #ffffff
            );

        background-size: 300% 300%;

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        animation: gradientMove 8s ease infinite;
    }

    .hero-subtitle {
        max-width: 760px;

        font-size: 1.1rem;

        line-height: 1.7;

        color: rgba(255,255,255,0.78);

        margin-top: 1rem;
    }

    /* ======================================================
       SECTION HEADERS
       ====================================================== */

    .section-title {
        font-size: 1.6rem;

        font-weight: 850;

        color: #0f172a;

        margin-top: 1.2rem;

        margin-bottom: 0.2rem;
    }

    .section-subtitle {
        color: #64748b;

        font-size: 0.95rem;

        margin-bottom: 1.2rem;
    }

    /* ======================================================
       INFO CARDS
       ====================================================== */

    .travel-card {
        background: rgba(255,255,255,0.75);

        border: 1px solid rgba(148,163,184,0.18);

        border-radius: 20px;

        padding: 1.2rem;

        min-height: 125px;

        box-shadow:
            0 10px 30px rgba(15,23,42,0.06);

        backdrop-filter: blur(15px);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .travel-card:hover {
        transform: translateY(-4px);

        box-shadow:
            0 18px 35px rgba(15,23,42,0.10);
    }

    .travel-icon {
        font-size: 2rem;

        margin-bottom: 0.4rem;
    }

    .travel-card-title {
        font-weight: 800;

        color: #0f172a;

        font-size: 1rem;
    }

    .travel-card-text {
        color: #64748b;

        font-size: 0.82rem;

        margin-top: 0.25rem;
    }

    /* ======================================================
       DESTINATION PREVIEW
       ====================================================== */

    .destination-preview {
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.95),
                rgba(239,246,255,0.9)
            );

        border-radius: 24px;

        padding: 1.5rem;

        border: 1px solid rgba(59,130,246,0.12);

        box-shadow:
            0 15px 40px rgba(30,64,175,0.08);

        margin: 1.5rem 0;
    }

    .destination-name {
        font-size: 2rem;

        font-weight: 900;

        color: #0f172a;
    }

    .tag {
        display: inline-block;

        padding: 0.35rem 0.7rem;

        margin: 0.5rem 0.3rem 0 0;

        border-radius: 999px;

        background: #e0f2fe;

        color: #0369a1;

        font-size: 0.75rem;

        font-weight: 700;
    }

    /* ======================================================
       METRICS
       ====================================================== */

    .metric-box {
        text-align: center;

        background: rgba(255,255,255,0.8);

        border-radius: 18px;

        padding: 1rem;

        border: 1px solid rgba(148,163,184,0.15);

        box-shadow:
            0 8px 25px rgba(15,23,42,0.05);
    }

    .metric-value {
        font-size: 1.5rem;

        font-weight: 850;

        color: #2563eb;
    }

    .metric-label {
        font-size: 0.7rem;

        color: #64748b;

        text-transform: uppercase;

        letter-spacing: 0.8px;

        margin-top: 0.25rem;
    }

    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #f8fafc,
                #eef6ff
            );
    }

    /* ======================================================
       BUTTON
       ====================================================== */

    .stButton > button {
        width: 100%;

        border: none;

        border-radius: 14px;

        padding: 0.8rem 1rem;

        font-weight: 800;

        background:
            linear-gradient(
                90deg,
                #2563eb,
                #7c3aed
            );

        color: white;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 12px 25px rgba(37,99,235,0.25);
    }

    /* ======================================================
       FOOTER
       ====================================================== */

    .voyage-footer {
        text-align: center;

        color: #94a3b8;

        font-size: 0.8rem;

        padding-top: 3rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="voyage-hero">

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

    st.markdown("## 🧭 Trip Planner")

    st.caption("Customize your perfect adventure.")

    st.divider()

    location = st.text_input(
        "📍 Where are you going?",
        placeholder="Tokyo, Paris, Goa..."
    )

    days = st.slider(
        "📅 How many days?",
        min_value=1,
        max_value=30,
        value=5
    )

    budget = st.selectbox(
        "💰 What's your budget?",
        [
            "Budget",
            "Moderate",
            "Luxury"
        ]
    )

    travel_type = st.selectbox(
        "👥 Who are you travelling with?",
        [
            "Solo",
            "Couple",
            "Friends",
            "Family"
        ]
    )

    st.markdown("### ✨ What do you love?")

    interests = st.multiselect(
        "Select your interests",
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
        default=[
            "🍜 Food & Cuisine",
            "📸 Photography"
        ],
        label_visibility="collapsed"
    )

    travel_pace = st.select_slider(
        "🚶 Travel pace",
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

        Tell VoyageAI about your interests to get a more personalized
        itinerary.
        """
    )


# ============================================================
# MAIN SECTION
# ============================================================

st.markdown(
    '<div class="section-title">🌍 Design Your Journey</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Choose a destination and let AI create your adventure.</div>',
    unsafe_allow_html=True
)


# ============================================================
# QUICK DESTINATIONS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="travel-card">
            <div class="travel-icon">🗼</div>
            <div class="travel-card-title">Paris</div>
            <div class="travel-card-text">Romance & culture</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="travel-card">
            <div class="travel-icon">🏯</div>
            <div class="travel-card-title">Tokyo</div>
            <div class="travel-card-text">Tradition & technology</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="travel-card">
            <div class="travel-icon">🌴</div>
            <div class="travel-card-title">Bali</div>
            <div class="travel-card-text">Beaches & nature</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="travel-card">
            <div class="travel-icon">🏔️</div>
            <div class="travel-card-title">Switzerland</div>
            <div class="travel-card-text">Mountains & adventure</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DESTINATION PREVIEW
# ============================================================

if location.strip():

    st.markdown(
        f"""
        <div class="destination-preview">

            <div class="destination-name">
                📍 {location}
            </div>

            <div>
                <span class="tag">📅 {days} Days</span>
                <span class="tag">💰 {budget}</span>
                <span class="tag">👥 {travel_type}</span>
                <span class="tag">🚶 {travel_pace}</span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# GENERATE BUTTON
# ============================================================

st.markdown("### ✈️ Ready for takeoff?")

generate = st.button(
    "🚀 Generate My Dream Itinerary",
    use_container_width=True
)


# ============================================================
# AI GENERATION
# ============================================================

if generate:

    if not location.strip():

        st.warning(
            "📍 Please enter a destination in the sidebar first."
        )

    else:

        if interests:
            interest_text = ", ".join(interests)
        else:
            interest_text = "General sightseeing and exploration"

        prompt = f"""
You are VoyageAI, an expert international travel planner.

The traveler wants a personalized trip.

DESTINATION:
{location}

TRIP LENGTH:
{days} days

BUDGET:
{budget}

TRAVELING WITH:
{travel_type}

INTERESTS:
{interest_text}

TRAVEL PACE:
{travel_pace}

Create a practical, exciting and personalized travel itinerary.

IMPORTANT:
- Do not pretend to have live information.
- Do not invent exact current prices, opening hours or transportation schedules.
- If information can change frequently, tell the traveler to verify it before traveling.
- Make the itinerary realistic rather than trying to visit too many places in one day.
- Consider the traveler's group type, budget and interests.

FORMAT YOUR RESPONSE WITH THESE SECTIONS:

# 🌍 Trip Overview

Give a short description of the destination and explain why it suits this traveler.

# 🗓️ Day-by-Day Itinerary

For each day provide:

## Day X

☀️ Morning
- Activity
- Why it is worth visiting

🌤️ Afternoon
- Activity
- Food suggestion

🌙 Evening
- Activity
- Evening recommendation

🚆 Getting Around
- Practical transportation suggestion

💡 Local Tip
- One useful tip

Also provide one optional alternative activity for each day.

# 🏆 Must-See Experiences

Give 5-8 experiences that should not be missed.

# 💎 Hidden Gems

Suggest several less-obvious experiences suitable for this traveler.

# 🍜 Food Guide

Include:
- Local dishes
- Street food
- Foods to try
- Restaurant types to look for
- Dining etiquette if relevant

# 💰 Budget Guide

Break the expected spending into:

🏨 Accommodation
🍜 Food
🚆 Transportation
🎟️ Attractions
🛍️ Miscellaneous

Use approximate ranges rather than pretending exact prices.

# 🎒 Packing List

Create a destination-appropriate packing checklist.

# 📸 Best Photo Opportunities

Suggest memorable places or types of locations for photography.

# 🧠 Travel Smart

Include:
- Local etiquette
- Transport advice
- Common tourist mistakes
- Safety considerations
- Useful practical advice

# ⭐ Final Travel Tips

End with 5 concise tips that make the trip easier and more enjoyable.
"""

        try:

            with st.status(
                "✈️ VoyageAI is preparing your adventure...",
                expanded=True
            ) as status:

                st.write("🧠 Understanding your preferences...")
                st.write("🗺️ Designing your route...")
                st.write("🍜 Planning food experiences...")
                st.write("💎 Finding hidden-gem ideas...")
                st.write("✨ Personalizing your itinerary...")

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

                status.update(
                    label="🌟 Your journey is ready!",
                    state="complete",
                    expanded=False
                )

            # =================================================
            # SUCCESS
            # =================================================

            st.success(
                f"🎉 Your {days}-day {location} adventure is ready!"
            )

            # =================================================
            # TRIP METRICS
            # =================================================

            metric1, metric2, metric3, metric4 = st.columns(4)

            with metric1:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-value">
                            {days}
                        </div>

                        <div class="metric-label">
                            Trip Days
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with metric2:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-value">
                            {budget}
                        </div>

                        <div class="metric-label">
                            Budget
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with metric3:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-value">
                            {travel_type}
                        </div>

                        <div class="metric-label">
                            Travelers
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with metric4:
                st.markdown(
                    """
                    <div class="metric-box">
                        <div class="metric-value">
                            ✨
                        </div>

                        <div class="metric-label">
                            AI Planned
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.divider()

            # =================================================
            # ITINERARY
            # =================================================

            st.markdown("## 🗺️ Your Personalized Journey")

            st.markdown(
                response.text
            )

            # =================================================
            # DOWNLOAD
            # =================================================

            st.divider()

            st.markdown("### 📥 Save Your Adventure")

            filename = (
                location
                .strip()
                .replace(" ", "_")
                .replace("/", "_")
                + "_VoyageAI_Itinerary.txt"
            )

            st.download_button(
                label="📥 Download Itinerary",
                data=response.text,
                file_name=filename,
                mime="text/plain",
                use_container_width=True
            )

        except Exception as error:

            st.error(
                "⚠️ VoyageAI couldn't generate your itinerary."
            )

            st.info(
                "Please check your Gemini API key, internet connection, "
                "and model availability."
            )

            with st.expander("🔧 Technical Details"):

                st.code(
                    str(error)
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="voyage-footer">

        ✈️ <b>VoyageAI</b>

        <br>

        Travel smarter · Explore farther · Create unforgettable memories 🌍

        <br><br>

        Built with ❤️ using Streamlit + Gemini

    </div>
    """,
    unsafe_allow_html=True
)