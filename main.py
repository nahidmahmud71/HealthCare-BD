import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import time
import folium
from streamlit_folium import folium_static

# ================= 1. PAGE CONFIGURATION =================
st.set_page_config(
    page_title="HealthPlus BD | Smart Health Hub",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. SPLASH SCREEN (INTRO ANIMATION) =================
if 'splash_shown' not in st.session_state:
    st.session_state.splash_shown = False

if not st.session_state.splash_shown:
    st.markdown("""
    <style>
        .stApp { background-color: #000000; }
        .intro-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 90vh;
            animation: fadeIn 2s ease-in-out;
        }
        .dev-name {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(to right, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-transform: uppercase;
            text-align: center;
        }
        .uni-name {
            font-size: 1.8rem;
            color: #ffffff;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .college-name {
            font-size: 1.2rem;
            color: #b0b0b0;
            font-style: italic;
            letter-spacing: 1px;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
    <div class="intro-container">
        <div class="dev-name">MD NAHID MAHMUD</div>
        <div class="uni-name">Southeast University</div>
        <div class="college-name">Former Student: Cantonment College Jashore</div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(4)
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

# Premium Animations for EVERY Page
anim_home = load_lottie("https://assets10.lottiefiles.com/packages/lf20_pnycZg.json")
anim_hosp = load_lottie("https://assets3.lottiefiles.com/packages/lf20_s5id889b.json") # Map
anim_doc = load_lottie("https://assets10.lottiefiles.com/packages/lf20_5njp3vgg.json") # Doctor
anim_amb = load_lottie("https://assets9.lottiefiles.com/packages/lf20_z4cshyhf.json") # Ambulance
anim_bmi = load_lottie("https://assets2.lottiefiles.com/packages/lf20_wopcsux6.json") # Fitness

# --- ADVANCED CSS (Animations & Fixes) ---
st.markdown("""
<style>
    /* Global Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #f0f2f5;
    }

    /* Sidebar Design */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 2px solid #e0e0e0;
    }
    [data-testid="stSidebar"] * {
        color: #333333 !important; /* Sidebar text always dark */
    }

    /* CARD ANIMATION (Slide Up Effect) */
    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* --- DOCTOR CARD FIX (TEXT VISIBILITY) --- */
    .doc-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #0061ff;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        transition: 0.3s;
        animation: slideUp 0.6s ease-in-out; /* Animation added */
    }
    .doc-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 97, 255, 0.2);
    }
    .doc-card h4 {
        color: #000000 !important; /* Name is STRICTLY Black */
        font-weight: 800;
        margin: 0;
        font-size: 1.2rem;
    }
    .doc-card p {
        color: #555555 !important;
        margin: 2px 0;
    }

    /* --- HOSPITAL CARD --- */
    .hosp-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #FF4B4B;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        animation: slideUp 0.6s ease-in-out;
        transition: 0.3s;
    }
    .hosp-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(255, 75, 75, 0.2); }
    .hosp-card h3 { color: #000000 !important; }

    /* --- AMBULANCE CARD --- */
    .amb-card {
        background: linear-gradient(135deg, #fff0f0, #ffe6e6);
        border: 2px solid #ffcccc;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 15px;
        animation: slideUp 0.6s ease-in-out;
    }
    .amb-card h3 { color: #333; }
    .amb-card h1 { color: #FF4B4B; }

    /* --- HOME FEATURE CARDS --- */
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        height: 100%;
        cursor: pointer;
        border: 1px solid #eee;
        animation: slideUp 0.8s ease-in-out;
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
        animation: slideUp 1s ease-in-out;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0061ff, #00c6ff);
        color: white;
        border-radius: 50px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# ================= 4. DATA LOADING =================
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
    try: df_a = pd.read_csv("ambulances_64.csv")
    except: df_a = pd.DataFrame(columns=["District"])
    return df_h, df_d, df_a

df_h, df_d, df_a = load_data()

# ================= 5. SIDEBAR NAVIGATION =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063205.png", width=80)
    st.markdown("### HealthPlus BD")
    
    st.divider()
    
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

# --- 🏠 HOME PAGE ---
if menu == "🏠 হোম (Home)":
    # Header
    st.markdown("<h1 style='text-align:center; background:linear-gradient(to right, #0061ff, #60efff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:3.5rem; font-weight:800;'>HealthPlus Bangladesh</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#555;'>বর্তমান জেলা: <b>{selected_district}</b></p>", unsafe_allow_html=True)
    
    # Intro Section with Animation
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        st.markdown(f"""
        ### 👋 স্বাগতম!
        **HealthPlus BD** আপনার বিশ্বস্ত স্বাস্থ্য সঙ্গী।
        আমরা বাংলাদেশের ৬৪ জেলার ইমার্জেন্সি স্বাস্থ্যসেবা তথ্য প্রদান করছি।
        
        **একনজরে {selected_district}:**
        """)
        
        h_count = len(df_h[df_h['District'] == selected_district])
        d_count = len(df_d[df_d['District'] == selected_district])
        
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f"<div class='stat-box'><h2>{h_count}</h2><p>হাসপাতাল</p></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='stat-box'><h2>{d_count}</h2><p>ডাক্তার</p></div>", unsafe_allow_html=True)
        with s3: st.markdown(f"<div class='stat-box'><h2>24/7</h2><p>সার্ভিস</p></div>", unsafe_allow_html=True)

    with c2:
        if anim_home: st_lottie(anim_home, height=300)

    # Feature Grid
    st.markdown("---")
    st.subheader("🚀 সেবা সমূহ")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="feature-card" style="border-bottom: 5px solid #FF4B4B;"><h1>🏥</h1><h3>হাসপাতাল</h3></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="feature-card" style="border-bottom: 5px solid #4F8BF9;"><h1>👨‍⚕️</h1><h3>ডাক্তার</h3></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="feature-card" style="border-bottom: 5px solid #28a745;"><h1>🚑</h1><h3>অ্যাম্বুলেন্স</h3></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="feature-card" style="border-bottom: 5px solid #ffc107;"><h1>🩸</h1><h3>ব্লাড ব্যাংক</h3></div>""", unsafe_allow_html=True)

    st.markdown("<br><br><p style='text-align:center; color:#ccc;'>© 2026 HealthPlus BD</p>", unsafe_allow_html=True)

# --- 🏥 HOSPITAL PAGE ---
elif menu == "🏥 হাসপাতাল ও ম্যাপ":
    c_head, c_anim = st.columns([2, 1])
    with c_head: st.markdown(f"## 🏥 {selected_district}-এর হাসপাতাল")
    with c_anim: 
        if anim_hosp: st_lottie(anim_hosp, height=120)

    filtered_hosp = df_h[df_h['District'] == selected_district]
    
    if not filtered_hosp.empty:
        tab1, tab2 = st.tabs(["📋 তালিকা (List)", "🗺️ ম্যাপ (Live)"])
        with tab1:
            for _, row in filtered_hosp.iterrows():
                st.markdown(f"""
                <div class="hosp-card">
                    <h3 style="margin:0;">{row['Name']}</h3>
                    <p style="margin:0; color:#666;">📍 {row['Location']}</p>
                    <a href="tel:{row['Phone']}" style="text-decoration:none;">
                        <h4 style="margin:10px 0 0 0; color:#FF4B4B;">📞 {row['Phone']}</h4>
                    </a>
                </div>
                """, unsafe_allow_html=True)
        with tab2:
            avg_lat, avg_lon = filtered_hosp['Lat'].mean(), filtered_hosp['Lon'].mean()
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)
            for _, row in filtered_hosp.iterrows():
                folium.Marker([row['Lat'], row['Lon']], popup=row['Name'], icon=folium.Icon(color="red", icon="plus-sign")).add_to(m)
            folium_static(m)
    else:
        st.warning("ডাটা শীঘ্রই আসছে...")

# --- 👨‍⚕️ DOCTOR PAGE (FIXED VISIBILITY) ---
elif menu == "👨‍⚕️ ডাক্তার খুঁজুন":
    c_head, c_anim = st.columns([2, 1])
    with c_head: st.markdown(f"## 👨‍⚕️ {selected_district}-এর ডাক্তার")
    with c_anim: 
        if anim_doc: st_lottie(anim_doc, height=150)

    filtered_docs = df_d[df_d['District'] == selected_district]
    
    if not filtered_docs.empty:
        specs = ["সকল বিভাগ"] + sorted(filtered_docs['Specialty'].unique().tolist())
        choice = st.selectbox("বিভাগ ফিল্টার করুন:", specs)
        if choice != "সকল বিভাগ": filtered_docs = filtered_docs[filtered_docs['Specialty'] == choice]
        
        st.divider()
        cols = st.columns(2)
        for i, (index, row) in enumerate(filtered_docs.iterrows()):
            with cols[i % 2]:
                # DOCTOR CARD WITH FIXED BLACK TEXT
                st.markdown(f"""
                <div class="doc-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <h4>{row['Name']}</h4>
                            <span style="background:#e3f2fd; color:#0061ff; padding:2px 8px; border-radius:10px; font-size:12px; font-weight:bold;">{row['Specialty']}</span>
                            <p>🏥 {row['Hospital']}</p>
                        </div>
                        <div style="text-align:right;">
                            <a href="tel:{row['Phone']}" style="text-decoration:none;">
                                <button style="background:#28a745; color:white; border:none; padding:8px 15px; border-radius:50px; cursor:pointer;">📞</button>
                            </a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("ডাক্তারের তালিকা আপডেট হচ্ছে...")

# --- 🚑 AMBULANCE PAGE ---
elif menu == "🚑 অ্যাম্বুলেন্স":
    c_head, c_anim = st.columns([2, 1])
    with c_head: st.markdown(f"## 🚑 অ্যাম্বুলেন্স সার্ভিস")
    with c_anim: 
        if anim_amb: st_lottie(anim_amb, height=150)

    filtered_amb = df_a[(df_a['District'] == selected_district) | (df_a['District'] == 'All BD')]
    if not filtered_amb.empty:
        for _, row in filtered_amb.iterrows():
            st.markdown(f"""
            <div class="amb-card">
                <h3>🚑 {row['ServiceName']}</h3>
                <h1>{row['Contact']}</h1>
                <a href="tel:{row['Contact']}"><button>কল করুন</button></a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("জরুরী সেবা: **999**")

# --- 📊 BMI PAGE ---
elif menu == "📊 BMI ক্যালকুলেটর":
    c_head, c_anim = st.columns([2, 1])
    with c_head: st.markdown("## 📊 BMI চেক করুন")
    with c_anim: 
        if anim_bmi: st_lottie(anim_bmi, height=150)
        
    w = st.number_input("ওজন (kg):", 30, 150, 60)
    h_ft = st.number_input("উচ্চতা (ft):", 2, 8, 5)
    h_in = st.number_input("উচ্চতা (inch):", 0, 11, 6)
    
    if st.button("হিসাব করুন"):
        h_m = ((h_ft*12)+h_in)*0.0254
        bmi = w/(h_m**2)
        if bmi < 18.5: st.warning(f"আপনার ওজন কম: {bmi:.2f}")
        elif bmi < 25: st.success(f"আপনি সুস্থ আছেন: {bmi:.2f}")
        else: st.error(f"আপনার ওজন বেশি: {bmi:.2f}")
