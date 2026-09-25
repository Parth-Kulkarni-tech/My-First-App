import os
import time
import streamlit as st
from google import genai
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="Parth's AI Travel App",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GEMINI SETUP
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

try:
    if not api_key:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    st.error(
        "🔑 Gemini API key is missing.\n\n"
        "For local use, add GEMINI_API_KEY to your .env file.\n"
        "For Streamlit Cloud, add it under App Settings → Secrets."
    )
    st.stop()

client = genai.Client(api_key=api_key)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("✈️ VoyageAI")
    st.caption("Your personal AI travel planner")

    st.divider()

    # Destination
    st.subheader("📍 Destination")

    location = st.text_input(
        "Where do you want to go?",
        placeholder="e.g. Paris, Tokyo, Goa...",
    )

    # Duration
    st.subheader("📅 Duration")

    days = st.number_input(
        "How many days?",
        min_value=1,
        max_value=30,
        value=5,
        step=1,
    )

    # Budget
    st.subheader("💰 Budget")

    budget = st.selectbox(
        "Select your budget",
        [
            "Budget",
            "Moderate",
            "Luxury",
        ],
    )

    # Travel group
    st.subheader("👥 Travelling With")

    travel_type = st.radio(
        "Who are you travelling with?",
        [
            "Solo",
            "Friends",
            "Family",
            "Couple",
        ],
    )

    # Interests
    st.subheader("✨ Interests")

    interests = st.multiselect(
        "Select your interests",
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
    )

    st.divider()

    plan_trip = st.button(
        "🚀 Plan My Trip",
        use_container_width=True,
        type="primary",
    )

    st.divider()

    st.caption("Built with ❤️ by Parth")
    st.caption("Powered by Streamlit + Gemini")


# ============================================================
# HERO
# ============================================================

st.title("✈️ VoyageAI")

st.subheader("🌍 Your AI-Powered Travel Assistant")

st.write(
    "Plan unforgettable journeys with your personal AI travel companion. "
    "Discover amazing destinations, local food, hidden gems, exciting "
    "activities and personalized itineraries."
)

st.info(
    "✨ **How it works:** Choose your destination and preferences "
    "from the sidebar, then click **Plan My Trip**."
)


# ============================================================
# QUICK FEATURES
# ============================================================

st.divider()

st.header("✨ What VoyageAI Can Do")

feature1, feature2, feature3, feature4 = st.columns(4)

with feature1:
    with st.container(border=True):
        st.markdown("### 🗺️ Smart Itineraries")
        st.write(
            "Get a structured day-by-day travel plan."
        )

with feature2:
    with st.container(border=True):
        st.markdown("### 🍜 Local Experiences")
        st.write(
            "Discover food, culture and authentic experiences."
        )

with feature3:
    with st.container(border=True):
        st.markdown("### 💎 Hidden Gems")
        st.write(
            "Find interesting places beyond the usual tourist spots."
        )

with feature4:
    with st.container(border=True):
        st.markdown("### 💰 Budget Planning")
        st.write(
            "Plan your trip around your preferred budget."
        )


# ============================================================
# DESTINATION INSPIRATION
# ============================================================

st.divider()

st.header("🌎 Get Inspired")

st.caption(
    "Need an idea? Here are a few popular destinations."
)

destination1, destination2, destination3, destination4 = st.columns(4)

with destination1:
    with st.container(border=True):
        st.markdown("## 🗼 Paris")
        st.caption("🇫🇷 France")
        st.write("🎨 Art")
        st.write("🥐 Food")
        st.write("💕 Romance")

with destination2:
    with st.container(border=True):
        st.markdown("## 🗻 Tokyo")
        st.caption("🇯🇵 Japan")
        st.write("🍣 Food")
        st.write("⛩️ Culture")
        st.write("🤖 Technology")

with destination3:
    with st.container(border=True):
        st.markdown("## 🏝️ Bali")
        st.caption("🇮🇩 Indonesia")
        st.write("🏖️ Beaches")
        st.write("🌿 Nature")
        st.write("🧘 Relaxation")

with destination4:
    with st.container(border=True):
        st.markdown("## 🏙️ Dubai")
        st.caption("🇦🇪 UAE")
        st.write("💎 Luxury")
        st.write("🛍️ Shopping")
        st.write("🏜️ Adventure")


# ============================================================
# TRIP PREVIEW
# ============================================================

st.divider()

st.header("📊 Your Trip Preview")

preview1, preview2, preview3, preview4 = st.columns(4)

with preview1:
    st.metric(
        "📅 Duration",
        f"{days} days",
    )

with preview2:
    st.metric(
        "💰 Budget",
        budget,
    )

with preview3:
    st.metric(
        "👥 Travelling",
        travel_type,
    )

with preview4:
    st.metric(
        "✨ Interests",
        len(interests),
    )


# ============================================================
# CURRENT SELECTION
# ============================================================

if location.strip():

    st.divider()

    st.header("📍 Your Current Plan")

    st.success(
        f"You're planning a **{days}-day {budget.lower()} trip "
        f"to {location}** with **{travel_type.lower()}** travel."
    )

    if interests:

        st.write("**Your interests:**")

        interest_columns = st.columns(
            min(len(interests), 4)
        )

        for index, interest in enumerate(interests):

            with interest_columns[index % len(interest_columns)]:
                st.info(interest)


# ============================================================
# AI TRIP GENERATION
# ============================================================

if plan_trip:

    if not location.strip():

        st.warning(
            "📍 Please enter a destination in the sidebar first."
        )

    else:

        if interests:
            interest_text = ", ".join(interests)
        else:
            interest_text = (
                "General sightseeing, local experiences and exploration"
            )

        # ====================================================
        # PROMPT
        # ====================================================

        prompt = f"""
You are VoyageAI, a professional travel planner.

Create a detailed, practical and personalized travel itinerary.

TRAVEL INFORMATION

Destination:
{location}

Trip duration:
{days} days

Budget:
{budget}

Travelling with:
{travel_type}

Interests:
{interest_text}


YOUR RESPONSE MUST USE THIS STRUCTURE:

# ✈️ {location} Travel Guide

## 🌟 Trip Overview

Give a personalized introduction to the destination.

## 🗓️ Day-by-Day Itinerary

Create an itinerary for every day.

For each day use:

### Day 1

**🌅 Morning**
Activities and sightseeing.

**🍴 Lunch**
Food suggestions.

**🗺️ Afternoon**
Activities and places.

**🌆 Evening**
Evening activities.

**🍽️ Dinner**
Local food recommendations.

Repeat for every day.

## 🏛️ Must-Visit Places

List important attractions with a short explanation.

## 🍜 Food & Local Experiences

Recommend local dishes, restaurants/types of places,
markets and authentic experiences.

## 💎 Hidden Gems

Recommend interesting less-touristy experiences.

## 💰 Estimated Budget

Give approximate costs for:

- 🏨 Accommodation
- 🍴 Food
- 🚕 Transportation
- 🎟️ Activities
- 🛍️ Miscellaneous

Adjust recommendations to the selected budget.

## 🎒 Travel Tips

Include:

- Transportation
- Safety
- Local customs
- Areas to stay
- Booking advice
- Common tourist mistakes

## 🌦️ Best Time to Visit

Explain weather and seasonal considerations.

## 🧳 Packing Checklist

Create a useful destination-specific packing list.

## ⭐ Final Recommendations

End with personalized travel advice.

IMPORTANT:

- Make the itinerary specific to the destination.
- Consider the budget.
- Consider the travel group.
- Consider the interests.
- Keep the itinerary realistic.
- Avoid generic filler.
- Do not invent live prices.
- Do not invent opening hours.
- Label prices as approximate.
- Do not claim real-time availability.
- Use Markdown.
- Do not use HTML.
"""


        # ====================================================
        # GENERATION STATUS
        # ====================================================

        with st.status(
            "✈️ VoyageAI is preparing your trip...",
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
                    label="✅ Your itinerary is ready!",
                    state="complete",
                    expanded=False,
                )

            except Exception as error:

                status.update(
                    label="❌ Something went wrong",
                    state="error",
                    expanded=True,
                )

                st.error(
                    f"Gemini could not generate your itinerary.\n\n"
                    f"{error}"
                )

                st.stop()


        # ====================================================
        # RESULTS
        # ====================================================

        st.divider()

        st.header("🗺️ Your Personalized Travel Plan")

        st.success(
            f"🎉 Your {days}-day adventure in {location} is ready!"
        )

        st.markdown(response.text)


        # ====================================================
        # DOWNLOAD
        # ====================================================

        st.divider()

        st.header("📥 Save Your Travel Plan")

        st.write(
            "Keep a copy of your itinerary for your trip."
        )

        st.download_button(
            label="📄 Download Itinerary",
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

st.caption(
    "✈️ Parth's AI Travel App • "
    "Powered by Gemini • "
    "Built with Streamlit"
)