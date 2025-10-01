import streamlit as st
import random # Needed for random daily tips
import time # Needed for the reminder timer

# --- Configuration and Initial Setup ---

# Set up the page (Stage 6 Hint)
st.set_page_config(
    page_title="WaterBuddy: Your Daily Hydration Companion",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Friendly colours and theme (Stage 6 Hint)
st.markdown(
    """
    <style>
    .reportview-container {
        background: #F0F8FF; /* Light blue/aqua background */
    }
    /* Custom style for the progress bar to make it feel like water */
    .stProgress > div > div > div > div {
        background-color: #1E90FF; /* Dodger Blue for the fill */
    }
    h1 {
        color: #008B8B; /* Dark Cyan for heading */
        text-align: center;
    }
    .mascot-emoji {
        font-size: 5rem;
        text-align: center;
        display: block;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Hydration Logic (Stage 4 & 5) ---

# Recommended Daily Goals (in ml) based on age (Compulsory Feature)
AGE_GOALS = {
    "6-12 Years (Child)": 1600,
    "13-18 Years (Teen)": 2300,
    "19-50 Years (Adult)": 2500,
    "51-64 Years (Older Adult)": 2200,
    "65+ Years (Senior)": 2000
}

# Optional Creative Idea: Random daily hydration tips (Stage 5 Hint)
DAILY_TIPS = [
    "Did you know thirst is a sign you're already dehydrated? Drink before you feel thirsty!",
    "Keep a water bottle near you to remember to sip throughout the day.",
    "Try adding slices of lemon or cucumber to your water for a fresh taste.",
    "For every hour of exercise, drink an extra 500ml of water.",
    "A headache can sometimes be a sign of mild dehydration. Time for a drink!"
]

# Initialize session state for live data storage (Stage 4 Hint)
if 'total_intake' not in st.session_state:
    st.session_state.total_intake = 0
if 'daily_goal' not in st.session_state:
    st.session_state.daily_goal = AGE_GOALS["19-50 Years (Adult)"]
if 'age_selector' not in st.session_state:
    st.session_state.age_selector = "19-50 Years (Adult)"
if 'random_tip' not in st.session_state: # Store the daily tip so it doesn't change on every rerun
    st.session_state.random_tip = random.choice(DAILY_TIPS)

def update_goal():
    """Updates the goal based on the selected age group."""
    age_group = st.session_state.age_selector
    st.session_state.daily_goal = AGE_GOALS[age_group]

def log_water(amount):
    """Adds water to the total intake (Compulsory Feature)."""
    st.session_state.total_intake += amount
    if st.session_state.total_intake > 10000:
        st.session_state.total_intake = 10000

def reset_progress():
    """Resets the intake for a new day (Compulsory Feature)."""
    st.session_state.total_intake = 0
    # Also reset the tip when starting a fresh day
    st.session_state.random_tip = random.choice(DAILY_TIPS)
    st.toast("Progress reset! Start a fresh day. 💧")

# --- Sidebar Content (Optional Creative Idea: Pop-up Reminder Alternative) ---
with st.sidebar:
    st.header("Daily Tip & Reminders")

    # Random Daily Hydration Tips (Optional Creative Idea)
    st.info(f"💡 **Tip of the Day:** {st.session_state.random_tip}")

    st.subheader("Hydration Reminder Timer")
    st.write("Set a timer to remind you to drink!")
    
    # Simple timer setup (Tkinter alternative)
    reminder_duration = st.selectbox(
        "Set reminder interval:", 
        options=[30, 60, 90, 120], 
        format_func=lambda x: f"{x} minutes",
        index=1
    )
    
    if st.button("Start Reminder"):
        # This loop provides a visual countdown timer
        with st.empty():
            st.warning(f"Reminder set for every **{reminder_duration} minutes**.")
            st.info("You must keep this tab open!")
            start_time = time.time()
            
            while True:
                time_elapsed = int(time.time() - start_time)
                time_remaining = (reminder_duration * 60) - (time_elapsed % (reminder_duration * 60))
                
                # Convert seconds remaining to minutes and seconds for display
                mins = time_remaining // 60
                secs = time_remaining % 60
                
                st.markdown(f"**Next sip reminder in:** {mins:02d}m {secs:02d}s")
                time.sleep(1)
                
                if time_remaining <= 1:
                    st.toast("🔔 **REMINDER: Time to drink water!** 💦")
                    start_time = time.time() # Reset the timer

# --- Main Interface Setup (Stage 6) ---

st.title("WaterBuddy 💧")
st.header("Your Daily Hydration Companion")

# --- Section 3: Progress & Feedback (Compulsory Interface Section) ---
st.subheader("WaterBuddy Live Mascot")

# Compute calculations (Compulsory Calculation)
percentage_achieved = min(100, (st.session_state.total_intake / st.session_state.daily_goal) * 100)
remaining_water = max(0, st.session_state.daily_goal - st.session_state.total_intake)

# Dynamic Mascot Reaction (Optional Creative Idea: Turtle Graphics Alternative)
if percentage_achieved == 0:
    mascot_emoji = "😴" # Sleeping
    mascot_message = "👋 Hello! WaterBuddy is ready to start the day. Let's sip!"
elif percentage_achieved < 25:
    mascot_emoji = "🙂" # Waking up
    mascot_message = "💧 Good start! Every drop you log is a step toward your goal."
elif percentage_achieved < 50:
    mascot_emoji = "😄" # Happy
    mascot_message = "💪 Halfway there! You're building a great habit!"
elif percentage_achieved < 75:
    mascot_emoji = "🤩" # Excited
    mascot_message = "🌟 Almost there! WaterBuddy is getting excited for you!"
elif percentage_achieved < 100:
    mascot_emoji = "👏" # Clapping
    mascot_message = "🥳 Great job! You've nearly hit your goal—just a little more!"
elif percentage_achieved >= 100:
    mascot_emoji = "🏆" # Champion
    mascot_message = "🎉 GOAL ACHIEVED! Excellent hydration today! WaterBuddy is proud! 🎉"

# Display the mascot and message
st.markdown(f'<div class="mascot-emoji">{mascot_emoji}</div>', unsafe_allow_html=True)
st.success(mascot_message)

st.markdown("---") 

# --- Section 1: Goal Setting ---

st.subheader("1. Set Your Daily Goal")

# Let users select their age group (st.selectbox - Compulsory Feature)
age_group = st.selectbox(
    "Select your age group to get a recommended goal (age-aware prompt):",
    options=list(AGE_GOALS.keys()),
    index=list(AGE_GOALS.keys()).index(st.session_state.age_selector),
    key="age_selector",
    on_change=update_goal,
)
standard_goal = AGE_GOALS[age_group] # Get the standard goal based on selection

# Optional Creative Idea: Show standard target vs user-set goal side-by-side
col_standard, col_manual = st.columns(2)

with col_standard:
    st.metric(label="Standard Recommended Goal", value=f"{standard_goal} ml")

with col_manual:
    # Option to manually adjust the goal (st.number_input - Compulsory Feature)
    manual_goal = st.number_input(
        "Manually set your own custom goal (in ml):",
        min_value=500,
        max_value=5000,
        value=st.session_state.daily_goal,
        step=100,
        key="manual_goal_input"
    )
    st.session_state.daily_goal = manual_goal

st.markdown("---") 

# --- Unit Converter (Optional Creative Idea) ---
st.subheader("Quick Unit Converter (Cups ↔ ml)")
col_ml, col_cups = st.columns(2)
with col_ml:
    ml_input = st.number_input("Convert ml to Cups (using 250ml/cup):", min_value=0, value=250, step=50)
    cups_output = ml_input / 250
    st.write(f"**Result:** {cups_output:.2f} Cups")
with col_cups:
    cups_input = st.number_input("Convert Cups to ml (using 250ml/cup):", min_value=0.0, value=1.0, step=0.5)
    ml_output = cups_input * 250
    st.write(f"**Result:** {ml_output:.0f} ml")

st.markdown("---") 

# --- Section 2: Logging Intake (Compulsory Interface Section) ---

st.subheader("2. Log Your Water Intake")

# Use columns to group the log button neatly (Stage 6 Hint)
col_log, col_reset = st.columns([1.5, 1])

with col_log:
    # Quick log button (+250ml) (st.button - Compulsory Feature)
    if st.button("Log +250 ml", type="primary"):
        log_water(250)
        st.rerun() # Use st.rerun()

with col_reset:
    # Reset button (Compulsory Feature)
    if st.button("Reset Progress (New Day)", type="secondary"):
        reset_progress()
        st.rerun() # Use st.rerun()

st.markdown("---") 

# --- Section 4: Metrics and Progress Bars (Compulsory Visuals) ---

st.subheader("4. Daily Progress Visualization")

# Optional Creative Idea: Compare intake to standard age-based target visually
col_intake, col_comparison = st.columns(2)

with col_intake:
    st.metric(
        label=f"Your Logged Intake",
        value=f"{st.session_state.total_intake} ml",
        delta=f"Need {remaining_water} ml to reach goal!"
    )
    
with col_comparison:
    st.metric(
        label="Your Daily Goal",
        value=f"{st.session_state.daily_goal} ml",
        delta=f"Current Progress: {percentage_achieved:.0f}%"
    )

st.markdown("##### Progress to Your Custom Goal")
# Display a real-time progress bar (Compulsory Visual)
st.progress(percentage_achieved / 100, text=f"{percentage_achieved:.0f}% Achieved")

st.markdown("##### Comparison to Standard Goal")
standard_progress = min(100, (st.session_state.total_intake / standard_goal) * 100)
st.progress(standard_progress / 100, text=f"{standard_progress:.0f}% of Standard Goal ({standard_goal} ml)")

if st.session_state.total_intake >= standard_goal:
     st.success("You met the age-recommended standard! ✅")
