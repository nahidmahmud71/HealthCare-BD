import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import time

# ================= 1. PAGE CONFIGURATION =================
st.set_page_config(
    page_title="HealthPlus BD | Smart Health Hub",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"  # FIXED: Sidebar will always show now
)

# ================= 2. ASSETS & ANIMATIONS =================
@st.cache_data
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Animations
anim_welcome = load_lottie("https://assets10.lottiefiles.com/packages/lf20_pnycZg.json")
anim_dashboard = load_lottie("https://lottie.host/020092f6-3c58-4c12-9c17-1ba3595b1213/102c7G1v9A.json")

# ================= 3. ADVANCED CSS (DESIGN ENGINE) =================
st.markdown("""
<style>
    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@300;400;600;700&family=Poppins:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Poppins', 'Hind Siliguri', sans-serif;
    }

    /* --- SIDEBAR DESIGN (FIXED VISIBILITY) --- */
    [data-testid="stSidebar"] {
        background-color: #f0f8ff; /* Light AliceBlue background */
        border-right: 2px solid #dbe9f6;
    }
    
    /* Sidebar Text Color Fix */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #004085 !important; /* Dark Blue Text for high contrast */
        font-weight: 600;
    }

    /* Sidebar Radio Buttons Styling */
    div[role="radiogroup"] > label > div:first-of-type {
        background-color: #e3f2fd; /* Light bubble background */
        border-radius: 5px;
    }
    
    /* --- MAIN CONTENT DESIGN --- */
    
    /* Hero Title Gradient */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #0061ff, #60efff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 0px 4px 10px rgba(0, 97, 255, 0.1);
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 40px;
        font-weight: 500;
    }

    /* Glassmorphism Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        border-bottom: 5px solid #0061ff;
        transition: all 0.3s ease;
        height: 100%;
        cursor: pointer;
    }
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 97, 255, 0.2);
        background: #ffffff;
    }

    /* Metric/Stat Box */
    .stat-box {
        background: linear-gradient(135deg, #0061ff, #00c6ff);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0, 97, 255, 0.3);
        margin-bottom: 10px;
    }
    .stat-box h2 { color: white; margin: 0; font-size: 2.2rem; }
    .stat-box p { color: #e0f0ff; margin: 0; font-size: 1rem; }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #888;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# ================= 4. DATA LOADING =================
# LIST OF ALL 64 DISTRICTS
ALL_DISTRICTS = sorted([
    "Bagerhat", "Bandarban", "Barguna", "Barisal", "Bhola", "Bogra", "Brahmanbaria", "Chandpur", 
    "Chapainawabganj", "Chittagong", "Chuadanga", "Comilla", "Cox's Bazar", "Dhaka", "Dinajpur", 
    "Faridpur", "Feni", "Gaibandha", "Gazipur", "Gopalganj", "Habiganj", "Jamalpur", "Jessore", 
    "Jhalokati", "Jhenaidah", "Joypurhat", "Khagrachari", "Khulna", "Kishoreganj", "Kurigram", 
    "Kushtia", "Lakshmipur", "Lalmonirhat", "Madaripur", "Magura", "Manikganj", "Meherpur", 
    "Moulvibazar", "Munshiganj", "Mymensingh", "Naogaon", "Narail", "Narayanganj", "Narsingdi", 
    "Natore", "Netrokona", "Nilphamari", "Noakhali", "Pabna", "Panchagarh", "Patuakhali", 
    "Pirojpur", "Rajbari", "Rajshahi", "Rangamati", "Rangpur", "Satkhira", "Shariatpur", 
    "Sherpur", "Sirajganj", "Sunamganj", "Sylhet", "Tangail", "Thakurgaon"
])

@st.cache_data
def load_data():
    try: df_h = pd.read_csv("hospitals_64.csv")
    except: df_h = pd.DataFrame(columns=["District"])
    
    try: df_d = pd.read_csv("doctors_64.csv")
    except: df_d = pd.DataFrame(columns=["District"])
    
    return df_h, df_d

df_h, df_d = load_data()

# ================= 5. SIDEBAR NAVIGATION (FIXED VISIBILITY) =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063205.png", width=70)
    st.markdown("### HealthPlus BD")
    st.markdown("**আপনার ডিজিটাল স্বাস্থ্য সঙ্গী**")
    
    st.divider()
    
    # --- 64 DISTRICT SELECTOR ---
    selected_district = st.selectbox(
        "📍 জেলা নির্বাচন করুন:", 
        ALL_DISTRICTS, 
        index=ALL_DISTRICTS.index("Dhaka")
    )
    
    st.divider()
    
    # Navigation Menu
    menu = st.radio("মেনু:", 
        ["🏠 হোম (Home)", "🏥 হাসপাতাল", "👨‍⚕️ ডাক্তার", "🚑 অ্যাম্বুলেন্স", "🩸 ব্লাড ব্যাংক", "📊 BMI ক্যালকুলেটর"]
    )
    
    st.divider()
    st.warning("📞 ইমার্জেন্সি: **999**")

# ================= 6. MAIN CONTENT =================

if menu == "🏠 হোম (Home)":
    # Hero Section
    st.markdown("<div class='hero-title'>HealthPlus Bangladesh</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-subtitle'>বর্তমানে নির্বাচিত জেলা: <b>{selected_district}</b> | সঠিক তথ্য, সঠিক চিকিৎসা</div>", unsafe_allow_html=True)
    
    # Animation & Intro
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        st.markdown(f"""
        ### 👋 স্বাগতম!
        **HealthPlus BD** বাংলাদেশের প্রতিটি জেলার মানুষের স্বাস্থ্যসেবা নিশ্চিত করতে তৈরি করা হয়েছে।
        
        বর্তমানে আপনি **{selected_district}** জেলার তথ্য দেখছেন। বাম পাশের মেনু থেকে হাসপাতাল, ডাক্তার বা অ্যাম্বুলেন্স সেবা নির্বাচন করুন।
        """)
        
        st.write("") # Spacer
        
        # Dynamic Stats
        h_count = len(df_h[df_h['District'] == selected_district])
        d_count = len(df_d[df_d['District'] == selected_district])
        
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f"<div class='stat-box'><h2>{h_count}</h2><p>হাসপাতাল</p></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='stat-box'><h2>{d_count}</h2><p>ডাক্তার</p></div>", unsafe_allow_html=True)
        with s3: st.markdown(f"<div class='stat-box'><h2>24/7</h2><p>সার্ভিস</p></div>", unsafe_allow_html=True)

    with c2:
        if anim_welcome: st_lottie(anim_welcome, height=350, key="home_anim")

    # Services Grid (Features)
    st.markdown("---")
    st.subheader("🚀 আমাদের সেবাসমূহ")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="border-bottom-color: #FF4B4B;">
            <h1 style="font-size: 3.5rem; margin:0;">🏥</h1>
            <h3 style="color:#333; margin:10px 0;">হাসপাতাল</h3>
            <p style="color:#777;">লোকেশন ও ম্যাপ</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card" style="border-bottom-color: #4F8BF9;">
            <h1 style="font-size: 3.5rem; margin:0;">👨‍⚕️</h1>
            <h3 style="color:#333; margin:10px 0;">ডাক্তার</h3>
            <p style="color:#777;">স্পেশালিস্ট খুঁজুন</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card" style="border-bottom-color: #28a745;">
            <h1 style="font-size: 3.5rem; margin:0;">🚑</h1>
            <h3 style="color:#333; margin:10px 0;">অ্যাম্বুলেন্স</h3>
            <p style="color:#777;">জরুরী সেবা</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="feature-card" style="border-bottom-color: #ffc107;">
            <h1 style="font-size: 3.5rem; margin:0;">🩸</h1>
            <h3 style="color:#333; margin:10px 0;">ব্লাড ব্যাংক</h3>
            <p style="color:#777;">ডোনার কানেকশন</p>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class='footer'>
        <p>© 2026 HealthPlus BD | Developed for Humanity ❤️</p>
    </div>
    """, unsafe_allow_html=True)

# Placeholder for other pages
else:
    st.markdown(f"<div class='hero-title'>{menu}</div>", unsafe_allow_html=True)
    st.info(f"🚧 আপনি এখন **{menu}** পেজে আছেন। আমরা ধাপে ধাপে প্রতিটি সেকশন ডিজাইন করছি।")
    if anim_dashboard: st_lottie(anim_dashboard, height=300)
