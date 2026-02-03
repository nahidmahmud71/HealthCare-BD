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

# ================= 2. SPLASH SCREEN (INTRO ANIMATION) =================
# অ্যাপ ওপেন হলে এই ইন্ট্রো একবার দেখাবে, তারপর মেইন পেজে যাবে
if 'splash_shown' not in st.session_state:
    st.session_state.splash_shown = False

if not st.session_state.splash_shown:
    st.markdown("""
    <style>
        .stApp { background-color: #000000; }
        .intro-wrapper {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 90vh;
            animation: fadeIn 2s ease-in-out;
        }
        .dev-name {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(to right, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        .uni-name {
            font-size: 2rem;
            color: #ffffff;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .college-name {
            font-size: 1.5rem;
            color: #aaaaaa;
            font-style: italic;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: scale(0.8); }
            100% { opacity: 1; transform: scale(1); }
        }
    </style>
    <div class="intro-wrapper">
        <div class="dev-name">MD NAHID MAHMUD</div>
        <div class="uni-name">Southeast University</div>
        <div class="college-name">Ex: Cantonment College Jashore</div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(4) # ৪ সেকেন্ড পর মেইন পেজ আসবে
    st.session_state.splash_shown = True
    st.rerun()

# ================= 3. ASSETS & STYLING =================
@st.cache_data
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Animations
anim_welcome = load_lottie("https://assets10.lottiefiles.com/packages/lf20_pnycZg.json")
anim_map = load_lottie("https://assets3.lottiefiles.com/packages/lf20_s5id889b.json")
anim_doc = load_lottie("https://assets10.lottiefiles.com/packages/lf20_5njp3vgg.json")

import folium
from streamlit_folium import folium_static

# --- ADVANCED CSS (SIDEBAR FIX & COLORFUL DESIGN) ---
st.markdown("""
<style>
    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #f4f7f6;
    }

    /* --- SIDEBAR VISIBILITY FIX --- */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 2px solid #e0e0e0;
    }
    
    /* সাইডবারের লেখাগুলো কালো/গাঢ় নীল করা হলো যাতে দেখা যায় */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #004085 !important;
    }
    [data-testid="stSidebar"] label {
        color: #333333 !important;
        font-weight: bold;
    }
    [data-testid="stSidebar"] .stRadio div[role='radiogroup'] label {
        color: #333333 !important;
        font-weight: 500;
    }
    /* নির্বাচিত মেনু হাইলাইট */
    div[role="radiogroup"] > label > div:first-of-type {
        background-color: #e3f2fd;
    }

    /* --- MAIN PAGE DESIGN --- */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #0061ff, #60efff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 0px 5px 15px rgba(0, 97, 255, 0.2);
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 40px;
    }

    /* COLORFUL FEATURE CARDS */
    .feature-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        height: 100%;
        cursor: pointer;
        border: 1px solid #eee;
    }
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    /* Stats Box */
    .stat-box {
        background: linear-gradient(135deg, #0061ff, #00c6ff);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0, 97, 255, 0.3);
    }

    /* Hospital/Doctor Cards */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #FF4B4B;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .info-card:hover { transform: translateX(5px); box-shadow: 0 8px 25px rgba(255, 75, 75, 0.2); }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0061ff, #00c6ff);
        color: white;
        border-radius: 50px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover { transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# ================= 4. DATA LOADING =================
# 64 District List
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
    except: df_h = pd.DataFrame(columns=["District", "Name", "Location", "Phone", "Lat", "Lon"])
    try: df_d = pd.read_csv("doctors_64.csv")
    except: df_d = pd.DataFrame(columns=["District", "Name", "Specialty", "Hospital", "Phone"])
    try: df_a = pd.read_csv("ambulances_64.csv")
    except: df_a = pd.DataFrame(columns=["District", "ServiceName", "Contact"])
    return df_h, df_d, df_a

df_h, df_d, df_a = load_data()

# ================= 5. SIDEBAR NAVIGATION =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063205.png", width=80)
    st.markdown("### HealthPlus BD")
    
    st.divider()
    
    # জেলা নির্বাচন
    selected_district = st.selectbox(
        "📍 জেলা নির্বাচন করুন:", 
        ALL_DISTRICTS, 
        index=ALL_DISTRICTS.index("Dhaka")
    )
    
    st.divider()
    menu = st.radio("মেনু:", 
        ["🏠 হোম (Home)", "🏥 হাসপাতাল ও ম্যাপ", "👨‍⚕️ ডাক্তার খুঁজুন", "🚑 অ্যাম্বুলেন্স", "📊 BMI ক্যালকুলেটর"]
    )
    st.markdown("---")
    st.error("জরুরী হটলাইন: **999**")

# ================= 6. MAIN CONTENT =================

if menu == "🏠 হোম (Home)":
    # Hero Title
    st.markdown("<div class='hero-title'>HealthPlus Bangladesh</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-subtitle'>আপনার জেলা: <b>{selected_district}</b> | স্মার্ট স্বাস্থ্য সেবা</div>", unsafe_allow_html=True)
    
    # Welcome Section
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        st.markdown(f"""
        ### 👋 স্বাগতম!
        **HealthPlus BD** বাংলাদেশের প্রতিটি জেলার মানুষের জন্য একটি পূর্ণাঙ্গ স্বাস্থ্য সেবা অ্যাপ।
        
        **একনজরে {selected_district}:**
        """)
        
        # Live Stats
        h_count = len(df_h[df_h['District'] == selected_district])
        d_count = len(df_d[df_d['District'] == selected_district])
        
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f"<div class='stat-box'><h2>{h_count}</h2><p>হাসপাতাল</p></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='stat-box'><h2>{d_count}</h2><p>ডাক্তার</p></div>", unsafe_allow_html=True)
        with s3: st.markdown(f"<div class='stat-box'><h2>24/7</h2><p>সার্ভিস</p></div>", unsafe_allow_html=True)

    with c2:
        if anim_welcome: st_lottie(anim_welcome, height=300, key="home_anim")

    # COLORFUL SERVICES GRID
    st.markdown("---")
    st.subheader("🚀 আমাদের সেবাসমূহ")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="border-bottom: 5px solid #FF4B4B;">
            <h1 style="font-size: 3.5rem; margin:0;">🏥</h1>
            <h3 style="color:#333;">হাসপাতাল</h3>
            <p style="color:#777;">লোকেশন ও ম্যাপ</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card" style="border-bottom: 5px solid #4F8BF9;">
            <h1 style="font-size: 3.5rem; margin:0;">👨‍⚕️</h1>
            <h3 style="color:#333;">ডাক্তার</h3>
            <p style="color:#777;">বিশেষজ্ঞ খুঁজুন</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card" style="border-bottom: 5px solid #28a745;">
            <h1 style="font-size: 3.5rem; margin:0;">🚑</h1>
            <h3 style="color:#333;">অ্যাম্বুলেন্স</h3>
            <p style="color:#777;">জরুরী সেবা</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="feature-card" style="border-bottom: 5px solid #ffc107;">
            <h1 style="font-size: 3.5rem; margin:0;">🩸</h1>
            <h3 style="color:#333;">ব্লাড ব্যাংক</h3>
            <p style="color:#777;">ডোনার কানেকশন</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br><div style='text-align:center; color:#ccc;'>© 2026 HealthPlus BD</div>", unsafe_allow_html=True)

# --- HOSPITAL PAGE ---
elif menu == "🏥 হাসপাতাল ও ম্যাপ":
    st.markdown(f"## 🏥 {selected_district}-এর হাসপাতাল")
    filtered_hosp = df_h[df_h['District'] == selected_district]
    
    if not filtered_hosp.empty:
        tab1, tab2 = st.tabs(["📋 তালিকা (List)", "🗺️ লাইভ ম্যাপ (Map)"])
        with tab1:
            for _, row in filtered_hosp.iterrows():
                st.markdown(f"""
                <div class="info-card">
                    <h3 style="margin:0; color:#333;">{row['Name']}</h3>
                    <p style="margin:0; color:#666;">📍 {row['Location']}</p>
                    <a href="tel:{row['Phone']}" style="text-decoration:none;">
                        <h4 style="margin:10px 0 0 0; color:#FF4B4B;">📞 {row['Phone']}</h4>
                    </a>
                </div>
                """, unsafe_allow_html=True)
        with tab2:
            st.write("### 🗺️ লোকেশন দেখুন")
            avg_lat, avg_lon = filtered_hosp['Lat'].mean(), filtered_hosp['Lon'].mean()
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)
            for _, row in filtered_hosp.iterrows():
                folium.Marker([row['Lat'], row['Lon']], popup=row['Name'], icon=folium.Icon(color="red", icon="plus-sign")).add_to(m)
            folium_static(m)
    else:
        st.warning(f"⚠️ {selected_district}-এর হাসপাতাল ডাটা শীঘ্রই যুক্ত হবে।")
        if anim_map: st_lottie(anim_map, height=200)

# --- DOCTOR PAGE ---
elif menu == "👨‍⚕️ ডাক্তার খুঁজুন":
    st.markdown(f"## 👨‍⚕️ {selected_district}-এর বিশেষজ্ঞ ডাক্তার")
    filtered_docs = df_d[df_d['District'] == selected_district]
    
    if not filtered_docs.empty:
        specs = ["সকল বিভাগ"] + sorted(filtered_docs['Specialty'].unique().tolist())
        choice = st.selectbox("বিভাগ ফিল্টার করুন:", specs)
        if choice != "সকল বিভাগ": filtered_docs = filtered_docs[filtered_docs['Specialty'] == choice]
        
        st.divider()
        cols = st.columns(2)
        for i, (index, row) in enumerate(filtered_docs.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="info-card" style="border-left-color: #0061ff;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <h4 style="margin:0;">{row['Name']}</h4>
                            <span style="background:#e3f2fd; color:#0061ff; padding:2px 8px; border-radius:10px; font-size:12px;">{row['Specialty']}</span>
                            <p style="margin:5px 0 0 0; font-size:13px; color:#555;">🏥 {row['Hospital']}</p>
                        </div>
                        <div style="text-align:right;">
                            <a href="tel:{row['Phone']}" style="text-decoration:none;">
                                <button style="background:#28a745; color:white; border:none; padding:8px 15px; border-radius:50px; cursor:pointer;">📞 কল</button>
                            </a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info(f"দুঃখিত, {selected_district}-এর ডাক্তার তালিকা এখনো আপডেট করা হয়নি।")
        if anim_doc: st_lottie(anim_doc, height=200)

# --- AMBULANCE PAGE ---
elif menu == "🚑 অ্যাম্বুলেন্স":
    st.markdown(f"## 🚑 অ্যাম্বুলেন্স সার্ভিস")
    filtered_amb = df_a[(df_a['District'] == selected_district) | (df_a['District'] == 'All BD')]
    if not filtered_amb.empty:
        for _, row in filtered_amb.iterrows():
            st.error(f"🚑 {row['ServiceName']}: {row['Contact']}")
    else:
        st.error("জাতীয় জরুরী সেবা: **999**")

# --- BMI PAGE ---
elif menu == "📊 BMI ক্যালকুলেটর":
    st.markdown("## 📊 BMI চেক করুন")
    w = st.number_input("ওজন (kg):", 30, 150, 60)
    h_ft = st.number_input("উচ্চতা (ft):", 2, 8, 5)
    h_in = st.number_input("উচ্চতা (inch):", 0, 11, 6)
    if st.button("হিসাব করুন"):
        h_m = ((h_ft*12)+h_in)*0.0254
        bmi = w/(h_m**2)
        if bmi < 18.5: st.warning(f"আপনার ওজন কম: {bmi:.2f}")
        elif bmi < 25: st.success(f"আপনি সুস্থ আছেন: {bmi:.2f}")
        else: st.error(f"আপনার ওজন বেশি: {bmi:.2f}")
