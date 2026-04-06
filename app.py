import streamlit as st
import pandas as pd

# 1. PAGE CONFIG & THEME
st.set_page_config(page_title="Edli | The Bias-Free Engine", page_icon="🛡️", layout="wide")

# Custom CSS for "The Aesthetic" (Navy, White, and Gold)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #fcfcfc;
    }
    
    /* Hero Section */
    .hero {
        background-color: #001f3f;
        padding: 60px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 40px;
    }
    
    /* POC Cards */
    .poc-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: 0.3s;
    }
    .poc-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        border-color: #FFD700;
    }

    /* Typography */
    h1, h2, h3 { font-family: 'Inter', sans-serif; }
    .gold-text { color: #FFD700; font-weight: bold; }
    
    /* Buttons */
    .stButton>button {
        background-color: #FFD700 !important;
        color: #001f3f !important;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. HERO SECTION
st.markdown("""
    <div class="hero">
        <h1 style="font-size: 3.5rem; margin-bottom: 10px;">🛡️ Edli</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">
            The Anti-Consultant Engine. Transparent. Data-Driven. <span class="gold-text">Bias-Free.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

# 3. THE MISSION (The "What I am Making")
st.write("## 🚀 The Vision")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🚫 No Commissions
    Edli doesn't take 'referral fees' from colleges. Our data is pure and unbought.
    """)
with col2:
    st.markdown("""
    ### 📊 Real ROI
    We prioritize placements and fees over marketing brochures and expensive campuses.
    """)
with col3:
    st.markdown("""
    ### 🛰️ Deep-Tech
    Utilizing Geospatial-AI to understand urban trends and college accessibility.
    """)

st.divider()

# 4. THE POC (Proof of Concept)
st.write("## 🛠️ Proof of Concept (Live Demo)")
st.write("Try the logic I built during my 100-hour sprint.")

# Load Data (The same engine, but cleaner UI)
@st.cache_data
def get_data():
    try:
        df = pd.read_csv('colleges.csv')
        return df
    except:
        # Fallback if file isn't uploaded yet
        return pd.DataFrame({
            "College Name": ["Sample IIT", "Sample NIT"],
            "City": ["Delhi", "Mumbai"],
            "Highest CTC (LPA)": [120, 80],
            "CSE": ["Yes", "Yes"]
        })

df = get_data()

# Interactive Filter Card
with st.container():
    st.markdown('<div class="poc-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.write("### Filter Logic")
        city_input = st.multiselect("Target Cities", options=df['City'].unique(), default=df['City'].unique())
        min_ctc = st.slider("Min Placement (LPA)", 0, 200, 20)
        only_cse = st.toggle("Only with CSE")
    
    with c2:
        # Filtering Logic
        res = df[df['City'].isin(city_input)]
        res = res[res['Highest CTC (LPA)'] >= min_ctc]
        if only_cse:
            res = res[res['CSE'] == "Yes"]
            
        st.write(f"### Found {len(res)} matches")
        st.dataframe(res[['College Name', 'City', 'Highest CTC (LPA)']], use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 5. FOOTER
st.write("")
st.write("---")
st.caption("Built in public by an 18-year-old founder. Edli is 100% independent.")

# 2. DATA LOADING (IP Syllabus: Unit 1)
# @st.cache_data
def load_and_clean():
    df = pd.read_csv('colleges.csv')
    # Normalizing binary data for the logic
    cols = ['Cricket', 'Football', 'Aerospace', 'CSE', 'ECE']
    for c in cols:
        df[c] = df[c].astype(str).str.strip().str.capitalize()
    return df

df = load_and_clean()

# 3. THE 4-QUESTION FLOW (Updated for Multi-Choice)
st.subheader("Choose Your Preferences")

# Q1: Cities (Multiple)
all_cities = list(df['City'].unique())
q1_cities = st.multiselect("Q1: Which Cities are you considering?", options=all_cities)

# Q2: Sports
all_sports = ["Cricket","Football"]
q2_sport = st.multiselect("Q2: Preferred Sports Facility?", options=all_sports)

# Q3: CTC
q3_ctc = st.select_slider("Q3: Minimum Highest CTC (LPA)?", 
                         options=[0, 10, 20, 30, 40, 50, 100, 200], value=10)

# Q4: Branches (Multiple)
available_branches = ["CSE", "ECE", "Aerospace"]
q4_branches = st.multiselect("Q4: Which branches are you interested in?", options=available_branches)

# 4. THE UPDATED FILTERING LOGIC (IP Syllabus: .isin() and All-Match)
filtered = df.copy()

# Filter by Multiple Cities
filtered = filtered[filtered['City'].isin(q1_cities)]

# Filter by Minimum CTC
filtered = filtered[filtered['Highest CTC (LPA)'] >= q3_ctc]

# Filter by Sports
if q2_sport:
    for sport in q2_sport:
        filtered = filtered[filtered[sport] == "Yes"]

# Filter by Multiple Branches (The 'AND' logic)
if q4_branches:
    for branch in q4_branches:
        filtered = filtered[filtered[branch] == "Yes"]

# 5. THE REVEAL
st.divider()
st.subheader("🎯 Recommended Colleges")

if not filtered.empty:
    # Displaying selected columns for a clean look
    display_cols = ['College Name', 'City', 'Highest CTC (LPA)']
    st.table(filtered[display_cols].sort_values(by='Highest CTC (LPA)', ascending=False))
else:
    st.error("No colleges match all your criteria. Try lowering the CTC or changing the city.")

st.info("Note: This data is sourced directly to bypass agent commissions.")
