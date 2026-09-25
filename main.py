import os
import time
import streamlit as st
from google import genai
from dotenv import load_dotenv

# =========================================================
# CONFIG
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="VOYAGEAI | SMART TRAVEL PLANNER",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# GEMINI API
# =========================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

if not api_key:
    st.error(
        "🔑 Gemini API key not found. "
        "Set GEMINI_API_KEY in your .env file or Streamlit Secrets."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# =========================================================
# CUSTOM STREAMLIT STYLING
# =========================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #f8fbff 0%,
            #eef6ff 45%,
            #f8f4ff 100%
        );
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #111827 0%,
            #172554 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 14px;
        border: none;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        font-weight: 700;
        background: linear-gradient(
            90deg,
            #2563eb,
            #7c3aed
        );
        color: white;
        transition: 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
    }

    /* Text input */
    .stTextInput input {
        border-radius: 12px;
    }

    /* Select boxes */
    .stSelectbox > div > div {
        border-radius: 12px;
    }

    /* Number input */
    .stNumberInput input {
        border-radius: 12px;
    }

    /* Radio */
    div[role="radiogroup"] {
        gap: 0.5rem;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: white;
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
    }

    /* Success */
    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HERO SECTION
# =========================================================

st.title("✈️ VoyageAI")

st.subheader("🌍 Your AI-Powered Travel Assistant")

st.write(
    "Plan unforgettable journeys, discover hidden gems, explore local food, "
    "find exciting activities and create personalized itineraries with AI."
)

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🎒 Trip Planner")

    st.caption("Tell VoyageAI what kind of adventure you want.")

    location = st.text_input(
        "📍 Destination",
        placeholder="e.g. Paris, Tokyo, Goa..."
    )

    days = st.number_input(
        "📅 Trip Duration",
        min_value=1,
        max_value=30,
        value=5,
        step=1
    )

    budget = st.selectbox(
        "💰 Budget",
        [
            "Budget",
            "Moderate",
            "Luxury"
        ]
    )

    travel_type = st.radio(
        "👥 Travelling With",
        [
            "Solo",
            "Friends",
            "Family",
            "Couple"
        ]
    )

    interests = st.multiselect(
        "✨ Interests",
        [
            "Adventure",
            "Food",
            "Culture",
            "Nature",
            "Shopping",
            "Nightlife",
            "History",
            "Photography",
            "Relaxation"
        ],
        default=["Food", "Culture"]
    )

    st.divider()

    plan_trip = st.button(
        "🚀 Plan My Trip"
    )

    st.divider()

    st.caption(
        "Built with ❤️ using Streamlit + Gemini"
    )

# =========================================================
# MAIN INTRO
# =========================================================

st.header("🌍 Design Your Journey")

st.caption(
    "Choose your destination and let AI create a personalized adventure."
)

# =========================================================
# INSPIRATION CARDS
# =========================================================

st.subheader("✨ Popular Inspirations")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.markdown("### 🗼 Paris")
        st.caption("France")
        st.write("Art • Food • Romance")

with col2:
    with st.container(border=True):
        st.markdown("### 🗻 Tokyo")
        st.caption("Japan")
        st.write("Culture • Food • Technology")

with col3:
    with st.container(border=True):
        st.markdown("### 🏝️ Bali")
        st.caption("Indonesia")
        st.write("Beaches • Nature • Relaxation")

with col4:
    with st.container(border=True):
        st.markdown("### 🕌 Dubai")
        st.caption("UAE")
        st.write("Luxury • Shopping • Adventure")

# =========================================================
# TRIP PREVIEW
# =========================================================

st.divider()

st.subheader("📊 Your Trip Preview")

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric(
        "📅 Days",
        days
    )

with metric2:
    st.metric(
        "💰 Budget",
        budget
    )

with metric3:
    st.metric(
        "👥 Travelling",
        travel_type
    )

with metric4:
    st.metric(
        "✨ Interests",
        len(interests)
    )

# =========================================================
# DESTINATION PREVIEW
# =========================================================

if location.strip():

    st.divider()

    st.subheader("📍 Destination Selected")

    st.info(
        f"Your adventure is being planned for **{location}** "
        f"with a **{days}-day {budget.lower()} trip** for **{travel_type.lower()} travel**."
    )

# =========================================================
# AI TRIP GENERATION
# =========================================================

if plan_trip:

    if not location.strip():

        st.warning(
            "📍 Please enter a destination first!"
        )

    else:

        interest_text = (
            ", ".join(interests)
            if interests
            else "General sightseeing and local experiences"
        )

        prompt = f"""
You are VoyageAI, an expert professional travel planner.

Create a highly useful and realistic travel itinerary.

TRIP DETAILS
-------------
Destination: {location}
Duration: {days} days
Budget: {budget}
Travelling with: {travel_type}
Interests: {interest_text}

IMPORTANT INSTRUCTIONS
----------------------
Create the itinerary in a beautiful, easy-to-read Markdown format.

Start with:

# ✈️ {location} Travel Plan

Then include:

## 🌟 Trip Overview
Give a short description of the destination and why it suits this traveler.

## 🗓️ Day-by-Day Itinerary
For every day provide:

### Day 1
- 🌅 Morning:
- 🍴 Lunch:
- 🗺️ Afternoon:
- 🌆 Evening:
- 🍽️ Dinner:

Continue for every day of the trip.

## 🍜 Food & Local Experiences
Recommend local dishes, food experiences and places/types of places to try.

## 📸 Must-Visit Places
List the most interesting attractions and explain briefly why each is worth visiting.

## 💎 Hidden Gems
Suggest less touristy experiences when appropriate.

## 💰 Estimated Budget
Give approximate spending categories:
- 🏨 Accommodation
- 🍴 Food
- 🚕 Transportation
- 🎟️ Activities
- 💵 Miscellaneous

Keep the estimates appropriate for the selected budget.

## 🎒 Travel Tips
Include useful practical advice about:
- Transportation
- Local customs
- Safety
- Best areas to stay
- Booking advice
- Common tourist mistakes

## 🌦️ Best Time & Weather
Explain the generally suitable travel periods and weather considerations.

## 🧳 Packing Checklist
Create a useful checklist based on the destination and activities.

## ⭐ Final Tips
End with a concise list of personalized recommendations.

Make the itinerary practical rather than generic.

Do not invent specific opening hours, prices, transportation schedules,
or other highly time-sensitive facts unless clearly marked as approximate.

Use emojis naturally but do not overuse them.
"""

        # -------------------------------------------------
        # GENERATION STATUS
        # -------------------------------------------------

        with st.status(
            "✈️ VoyageAI is planning your adventure...",
            expanded=True
        ) as status:

            st.write(
                f"🔍 Exploring **{location}**..."
            )

            time.sleep(0.5)

            st.write(
                f"📅 Building a **{days}-day itinerary**..."
            )

            time.sleep(0.5)

            st.write(
                f"💰 Optimizing for a **{budget.lower()} budget**..."
            )

            time.sleep(0.5)

            st.write(
                f"🎒 Personalizing the trip for **{travel_type.lower()} travel**..."
            )

            time.sleep(0.5)

            st.write(
                "✨ Generating your personalized travel guide..."
            )

            try:

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt,
                )

                status.update(
                    label="✅ Your itinerary is ready!",
                    state="complete",
                    expanded=False
                )

            except Exception as e:

                status.update(
                    label="❌ Something went wrong",
                    state="error",
                    expanded=True
                )

                st.error(
                    f"Unable to generate the itinerary.\n\n{e}"
                )

                st.stop()

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        st.success(
            "🎉 Your personalized adventure is ready!"
        )

        st.divider()

        st.header(
            f"🗺️ {location} Travel Guide"
        )

        st.markdown(
            response.text
        )

        # -------------------------------------------------
        # DOWNLOAD
        # -------------------------------------------------

        st.divider()

        st.subheader("📥 Save Your Travel Plan")

        st.download_button(
            label="📄 Download Itinerary",
            data=response.text,
            file_name=f"{location.replace(' ', '_')}_travel_plan.md",
            mime="text/markdown"
        )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "✈️ Parth's AI Travel App • Powered by Streamlit & Gemini • "
    "Plan smarter. Travel better. 🌍"
)