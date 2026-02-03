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
    initial_sidebar_state="expanded"
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

# ================= 3. ADVANCED COLORFUL CSS (The Design Engine) =================
st.markdown("""
<style>
    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@300;400;600;700&family=Poppins:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Poppins', 'Hind Siliguri', sans-serif;
        background-color: #f0f2f5;
    }

    /* Sidebar Design */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #e6f7ff 100%);
        border-right: 2px solid #cceeff;
    }

    /* Hero Title Gradient */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #0061ff, #60efff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 0px 4px 10px rgba(0, 97, 255, 0.2);
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
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        height: 100%;
        cursor: pointer;
    }
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0, 97, 255, 0.15);
        border-color: #0061ff;
    }

    /* Metric/Stat Box */
    .stat-box {
        background: linear-gradient(135deg, #0061ff, #00c6ff);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0, 97, 255, 0.3);
    }
    .stat-box h2 { color: white; margin: 0; font-size: 2.5rem; }
    .stat-box p { color: #e0f0ff; margin: 0; font-size: 1rem; }

    /* Custom Select Box Styling */
    .stSelectbox label {
        color: #0061ff !important;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
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
# LIST OF ALL 64 DISTRICTS (Hardcoded for accuracy)
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
    # Load CSVs gracefully
    try: df_h = pd.read_csv("hospitals_64.csv")
    except: df_h = pd.DataFrame(columns=["District"])
    
    try: df_d = pd.read_csv("doctors_64.csv")
    except: df_d = pd.DataFrame(columns=["District"])
    
    return df_h, df_d

df_h, df_d = load_data()

# ================= 5. SIDEBAR NAVIGATION =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063205.png", width=70)
    st.markdown("### HealthPlus BD")
    st.caption("আপনার ডিজিটাল স্বাস্থ্য সঙ্গী")
    
    st.divider()
    
    # --- 64 DISTRICT SELECTOR ---
    # ডিফল্ট হিসেবে 'Dhaka' থাকবে, কিন্তু লিস্টে ৬৪টি জেলা থাকবে
    selected_district = st.selectbox("📍 জেলা নির্বাচন করুন:", ALL_DISTRICTS, index=ALL_DISTRICTS.index("Dhaka"))
    
    st.divider()
    
    menu = st.radio("মেনু:", 
        ["🏠 হোম (Home)", "🏥 হাসপাতাল", "👨‍⚕️ ডাক্তার", "🚑 অ্যাম্বুলেন্স", "🩸 ব্লাড ব্যাংক", "📊 BMI ক্যালকুলেটর"]
    )
    
    st.markdown("---")
    st.success("📞 ইমার্জেন্সি: **999**")

# ================= 6. MAIN CONTENT (HOME PAGE FOCUS) =================

if menu == "🏠 হোম (Home)":
    # Hero Section
    st.markdown("<div class='hero-title'>HealthPlus Bangladesh</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-subtitle'>বর্তমানে নির্বাচিত জেলা: <b>{selected_district}</b> | সঠিক তথ্য, সঠিক চিকিৎসা</div>", unsafe_allow_html=True)
    
    # Animation & Intro
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        st.markdown("""
        ### 👋 স্বাগতম!
        **HealthPlus BD** বাংলাদেশের প্রথম পূর্ণাঙ্গ অ্যানিমেটেড হেলথ পোর্টাল। 
        আমরা ৬৪ জেলার মানুষের স্বাস্থ্যসেবা নিশ্চিত করতে কাজ করছি।
        
        **আপনি এখানে পাবেন:**
        * ✅ আপনার জেলার সেরা হাসপাতালের তালিকা ও ম্যাপ
        * ✅ বিশেষজ্ঞ ডাক্তারদের চেম্বার ও অ্যাপয়েন্টমেন্ট নম্বর
        * ✅ ইমার্জেন্সি ব্লাড ডোনার ও অ্যাম্বুলেন্স সেবা
        * ✅ স্বাস্থ্য সচেতনতা ও ফিটনেস টুলস
        """)
        
        # Dynamic Stats based on CSV Data (or placeholders)
        h_count = len(df_h[df_h['District'] == selected_district])
        d_count = len(df_d[df_d['District'] == selected_district])
        
        st.write("") # Spacer
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f"<div class='stat-box'><h2>{h_count}</h2><p>হাসপাতাল</p></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='stat-box'><h2>{d_count}</h2><p>ডাক্তার</p></div>", unsafe_allow_html=True)
        with s3: st.markdown(f"<div class='stat-box'><h2>24/7</h2><p>সার্ভিস</p></div>", unsafe_allow_html=True)

    with c2:
        if anim_welcome: st_lottie(anim_welcome, height=350, key="home_anim")

    # Services Grid (The Colourful Part)
    st.markdown("---")
    st.subheader("🚀 আমাদের সেবাসমূহ")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="border-bottom: 5px solid #FF4B4B;">
            <h1 style="font-size: 3rem;">🏥</h1>
            <h3 style="color:#333;">হাসপাতাল</h3>
            <p style="color:#777;">ম্যাপ ও লোকেশন</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card" style="border-bottom: 5px solid #4F8BF9;">
            <h1 style="font-size: 3rem;">👨‍⚕️</h1>
            <h3 style="color:#333;">ডাক্তার</h3>
            <p style="color:#777;">স্পেশালিস্ট খুঁজুন</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card" style="border-bottom: 5px solid #28a745;">
            <h1 style="font-size: 3rem;">🚑</h1>
            <h3 style="color:#333;">অ্যাম্বুলেন্স</h3>
            <p style="color:#777;">জরুরী সেবা</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="feature-card" style="border-bottom: 5px solid #ffc107;">
            <h1 style="font-size: 3rem;">🩸</h1>
            <h3 style="color:#333;">ব্লাড ব্যাংক</h3>
            <p style="color:#777;">ডোনার কানেকশন</p>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class='footer'>
        <p>© 2026 HealthPlus BD | Developed for Humanity ❤️</p>
    </div>
    """, unsafe_allow_html=True)

# Placeholder for other pages (To be upgraded next)
else:
    st.markdown(f"<div class='hero-title'>{menu}</div>", unsafe_allow_html=True)
    st.info("🚧 এই পেজটি আপগ্রেড করা হচ্ছে... শীঘ্রই আসছে!")
    if anim_dashboard: st_lottie(anim_dashboard, height=300)
