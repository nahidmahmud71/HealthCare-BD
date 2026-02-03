import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import time
import folium
from streamlit_folium import folium_static

# ================= 1. PAGE CONFIGURATION =================
st.set_page_config(
    page_title="HealthPlus BD | Ultimate",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. SPLASH SCREEN (INTRO ANIMATION) =================
if 'splash_shown' not in st.session_state:
    st.session_state.splash_shown = False

if not st.session_state.splash_shown:
    st.markdown("""
    <style>
        .stApp { background-color: #000015; } /* Deepest Blue Black */
        .intro-box {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 90vh;
            animation: zoomIn 2.5s ease-out;
        }
        .dev-title {
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(to right, #00c6ff, #0072ff, #00c6ff);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 15px;
            animation: shine 3s linear infinite;
            text-shadow: 0 0 30px rgba(0, 198, 255, 0.6);
        }
        .uni-sub { font-size: 2.2rem; color: #ffffff; font-weight: 700; }
        .college-sub { font-size: 1.3rem; color: #b0b0b0; font-style: italic; margin-top: 10px; }
        
        @keyframes zoomIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        @keyframes shine { to { background-position: 200% center; } }
    </style>
    <div class="intro-box">
        <div class="dev-title">MD NAHID MAHMUD</div>
        <div class="uni-sub">Southeast University</div>
        <div class="college-sub">Former Student: Cantonment College Jashore</div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(4.5)
    st.session_state.splash_shown = True
    st.rerun()

# ================= 3. ASSETS & ANIMATIONS =================
@st.cache_data
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Lottie Files
anim_home = load_lottie("https://assets10.lottiefiles.com/packages/lf20_pnycZg.json")
anim_doc = load_lottie("https://assets10.lottiefiles.com/packages/lf20_5njp3vgg.json")
anim_amb = load_lottie("https://assets9.lottiefiles.com/packages/lf20_z4cshyhf.json")
anim_symptom = load_lottie("https://lottie.host/58819173-0740-4a80-9646-7a8311145491/6S5u5Q0D32.json")
anim_bmi = load_lottie("https://assets2.lottiefiles.com/packages/lf20_wopcsux6.json")

# ================= 4. ULTIMATE DARK BLUE CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    
    /* --- DEEP BLUE GALAXY BACKGROUND --- */
    @keyframes gradientDeepBlue {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    [data-testid="stAppViewContainer"] {
        /* Rich Deep Blue Gradient */
        background: linear-gradient(-45deg, #000428, #004e92, #021b79, #000000);
        background-size: 400% 400%;
        animation: gradientDeepBlue 12s ease infinite;
        color: white;
        font-family: 'Poppins', sans-serif;
    }

    /* --- SIDEBAR (Deep Glass) --- */
    [data-testid="stSidebar"] {
        background: rgba(0, 10, 30, 0.9);
        border-right: 1px solid rgba(0, 198, 255, 0.2);
        box-shadow: 5px 0 20px rgba(0,0,0,0.5);
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #ffffff !important;
        text-shadow: 0 0 5px rgba(0,0,0,0.5);
    }
    
    /* Radio Buttons Style */
    .stRadio > div > label {
        background-color: rgba(255, 255, 255, 0.05);
        color: white !important;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 8px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Bouncy transition */
        border: 1px solid transparent;
    }
    .stRadio > div > label:hover {
        background-color: rgba(0, 198, 255, 0.2);
        border-color: #00c6ff;
        transform: translateX(10px) scale(1.02);
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.4);
    }
    div[role="radiogroup"] > label > div:first-of-type {
        background-color: #00c6ff !important;
        box-shadow: 0 0 15px #00c6ff;
    }

    /* --- ULTRA ANIMATED CARDS (Glassmorphism + Glow) --- */
    .feature-card, .doc-card, .hosp-card, .sym-card, .amb-card {
        background: rgba(0, 20, 50, 0.6); /* Darker blue transparent */
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 25px;
        border: 1px solid rgba(0, 198, 255, 0.15);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
        transition: all 0.4s ease;
        animation: slideInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
    }
    
    /* HOVER EFFECT - The Magic Happens Here */
    .feature-card:hover, .doc-card:hover, .hosp-card:hover, .sym-card:hover, .amb-card:hover {
        transform: translateY(-10px) scale(1.03);
        border-color: #00c6ff;
        box-shadow: 0 20px 50px rgba(0, 198, 255, 0.3), inset 0 0 20px rgba(0, 198, 255, 0.1);
        z-index: 10;
    }
    
    /* Text Colors inside Cards */
    h1, h2, h3, h4, h5, p, div, span { color: white !important; }
    .highlight-text { color: #00c6ff !important; font-weight: bold; text-shadow: 0 0 10px rgba(0, 198, 255, 0.5); }
    .warning-text { color: #ff4b4b !important; font-weight: bold; text-shadow: 0 0 10px rgba(255, 75, 75, 0.5); }
    
    /* Buttons with Ripple Glow */
    .stButton>button {
        background: linear-gradient(90deg, #0061ff, #00c6ff);
        color: white !important;
        border-radius: 50px;
        font-weight: bold;
        border: none;
        padding: 12px 25px;
        width: 100%;
        transition: 0.4s;
        box-shadow: 0 0 20px rgba(0, 97, 255, 0.4);
        position: relative;
        overflow: hidden;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 40px rgba(0, 198, 255, 0.7);
    }

    /* --- CUSTOM ANIMATIONS --- */
    @keyframes slideInUp {
        0% { transform: translateY(50px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 20px 10px rgba(255, 75, 75, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
    }
    .pulse-anim {
        animation: pulse 2s infinite;
    }

</style>
""", unsafe_allow_html=True)

# ================= 5. DATA LOADING =================
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

# ================= 6. SIDEBAR =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063205.png", width=90)
    st.markdown("<h2 style='color:#00c6ff !important; text-shadow:0 0 10px #00c6ff;'>HealthPlus BD</h2>", unsafe_allow_html=True)
    st.write("আপনার ডিজিটাল স্বাস্থ্য সঙ্গী")
    
    st.divider()
    
    selected_district = st.selectbox("📍 জেলা নির্বাচন করুন:", ALL_DISTRICTS, index=ALL_DISTRICTS.index("Dhaka"))
    
    st.write("")
    menu = st.radio("মেনু নেভিগেশন:", 
        ["🏠 হোম পেজ", "🤒 প্রাথমিক চিকিৎসা", "🏥 হাসপাতাল ও ম্যাপ", "👨‍⚕️ ডাক্তার খুঁজুন", "🚑 অ্যাম্বুলেন্স", "📊 BMI ও ডায়েট"]
    )
    st.divider()
    # Pulse animation on emergency number
    st.markdown("<div class='pulse-anim' style='text-align:center; padding:15px; background:linear-gradient(45deg, #ff4b4b, #d32f2f); border-radius:15px; font-weight:bold; font-size:1.2rem;'>🚨 জরুরী হটলাইন: 999</div>", unsafe_allow_html=True)

# ================= 7. MAIN CONTENT =================

# --- HOME ---
if menu == "🏠 হোম পেজ":
    st.markdown("<h1 style='text-align:center; font-size:4rem; text-shadow:0 0 30px #00c6ff; letter-spacing:2px;'>HealthPlus Bangladesh</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:1.3rem; margin-bottom:40px;'>জেলা: <b class='highlight-text' style='font-size:1.5rem;'>{selected_district}</b> | উন্নত স্বাস্থ্য সেবা</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        st.write("### 👋 স্বাগতম!")
        st.markdown("""
        <div style='background:rgba(0,0,0,0.2); padding:20px; border-radius:20px; border:1px solid rgba(0,198,255,0.1);'>
        HealthPlus BD-তে আপনাকে স্বাগতম। এটি বাংলাদেশের সবচেয়ে আধুনিক এবং অ্যানিমেটেড হেলথ পোর্টাল। 
        আমরা আপনার জেলার স্বাস্থ্যসেবাকে আপনার হাতের মুঠোয় নিয়ে এসেছি।
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        # Stats with Glow
        s1, s2 = st.columns(2)
        h_n = len(df_h[df_h['District']==selected_district])
        d_n = len(df_d[df_d['District']==selected_district])
        with s1: st.markdown(f"<div class='feature-card' style='border-bottom:4px solid #00c6ff;'><h1 class='highlight-text' style='font-size:3.5rem;'>{h_n}</h1><p>হাসপাতাল</p></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='feature-card' style='border-bottom:4px solid #00c6ff;'><h1 class='highlight-text' style='font-size:3.5rem;'>{d_n}</h1><p>ডাক্তার</p></div>", unsafe_allow_html=True)

    with c2:
        if anim_home: st_lottie(anim_home, height=320)

    st.markdown("---")
    st.subheader("🚀 কুইক ফিচারস")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown("<div class='feature-card' style='text-align:center;'><h1>🤒</h1><h4>Symptom</h4><p>প্রাথমিক চিকিৎসা</p></div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='feature-card' style='text-align:center;'><h1>👨‍⚕️</h1><h4>Doctor</h4><p>অ্যাপয়েন্টমেন্ট</p></div>", unsafe_allow_html=True)
    with col3: st.markdown("<div class='feature-card' style='text-align:center;'><h1>🚑</h1><h4>Ambulance</h4><p>জরুরী কল</p></div>", unsafe_allow_html=True)
    with col4: st.markdown("<div class='feature-card' style='text-align:center;'><h1>📊</h1><h4>Diet Plan</h4><p>ফিটনেস গাইড</p></div>", unsafe_allow_html=True)

# --- SYMPTOM CHECKER (DETAILED) ---
elif menu == "🤒 প্রাথমিক চিকিৎসা":
    st.markdown("## 🤒 বিস্তারিত প্রাথমিক চিকিৎসা")
    c_anim, c_sel = st.columns([1, 2])
    with c_anim: if anim_symptom: st_lottie(anim_symptom, height=220)
    with c_sel:
        st.markdown("""<div style='background:rgba(255,75,75,0.1); padding:15px; border-radius:15px; border:1px solid #ff4b4b;'>
        ⚠️ <b>সতর্কতা:</b> এই পরামর্শগুলো শুধুমাত্র প্রাথমিক ধারণার জন্য। সমস্যা গুরুতর হলে অবশ্যই দ্রুত ডাক্তারের পরামর্শ নিন।
        </div>""", unsafe_allow_html=True)
        st.write("")
        symptom = st.selectbox("কোন সমস্যাটি হচ্ছে?", 
            ["বাছাই করুন...", "জ্বর (Fever)", "গ্যাস্ট্রিক/বুক জ্বালা", "মাথা ব্যথা", "শরীরে কাটা/ক্ষত", "পুড়ে যাওয়া (Burn)", "ডায়রিয়া", "উচ্চ রক্তচাপ (High BP)"]
        )

    if symptom != "বাছাই করুন...":
        st.markdown("---")
        st.markdown(f"### 🩺 পরামর্শ: <span class='highlight-text'>{symptom}</span>", unsafe_allow_html=True)
        
        # Data Dictionary (Same as before)
        data = {
            "জ্বর (Fever)": {
                "med": "প্যারাসিটামল (Napa/Ace) ৫০০ মিগ্রা। প্রাপ্তবয়স্কদের জন্য দিনে ৩ বার খাওয়ার পর।",
                "food": "প্রচুর পানি, ফলের রস (কমলা/মাল্টা), পাতলা স্যুপ, জাউভাত।",
                "avoid": "ঠান্ডা পানি, আইসক্রিম, ভাজাপোড়া খাবার, অতিরিক্ত তেলযুক্ত খাবার।",
                "warning": "জ্বর ১০৩° এর বেশি হলে, শরীরে র‍্যাশ উঠলে বা ৩ দিনের বেশি স্থায়ী হলে দ্রুত ডাক্তার দেখান।"
            },
            "গ্যাস্ট্রিক/বুক জ্বালা": {
                "med": "এন্টাসিড সিরাপ (Antacid) ২ চামচ অথবা ওমিপ্রাজল (Seclo 20mg) খাওয়ার আধা ঘণ্টা আগে।",
                "food": "শসা, ডাবের পানি, ঠান্ডা দুধ, পাকা কলা, পেঁপে।",
                "avoid": "ঝাল, মশলাদার খাবার, ধূমপান, চা-কফি, খালি পেটে থাকা।",
                "warning": "বুকে তীব্র ব্যথা হলে (যা পিঠের দিকে ছড়ায়) এবং ঘাম হলে এটি হার্ট অ্যাটাক হতে পারে। দ্রুত হাসপাতালে যান।"
            },
            "মাথা ব্যথা": {
                "med": "প্যারাসিটামল (Napa Extra) অথবা Tufnil (মাইগ্রেন হলে)।",
                "food": "আদা চা, প্রচুর পানি, বাদাম, ম্যাগনেসিয়াম সমৃদ্ধ খাবার।",
                "avoid": "অতিরিক্ত স্ক্রিন টাইম (মোবাইল/ল্যাপটপ), কড়া রোদ, অনিদ্রা।",
                "warning": "মাথা ব্যথার সাথে বমি, চোখে ঝাপসা দেখা বা কথা জড়িয়ে গেলে নিউরোলোজিস্ট দেখান।"
            },
            "ডায়রিয়া": {
                "med": "খাওয়ার স্যালাইন (Orsaline-N) প্রতিবার পায়খানার পর। জিংক ট্যাবলেট খেতে পারেন।",
                "food": "জাউভাত, কাঁচাকলা ভর্তা, ডাবের পানি, চিড়ার পানি।",
                "avoid": "দুধ, শাক, আঁশযুক্ত খাবার, বাইরের খোলা খাবার।",
                "warning": "প্রস্রাব বন্ধ হয়ে গেলে বা চোখ গর্তে ঢুকে গেলে দ্রুত হাসপাতালে স্যালাইন দিতে হবে।"
            },
             "শরীরে কাটা/ক্ষত": {
                "med": "স্যাভলন বা পovidone Iodine দিয়ে পরিষ্কার করুন। অ্যান্টিবায়োটিক মলম লাগাতে পারেন।",
                "food": "প্রোটিন সমৃদ্ধ খাবার (ডিম, মাছ) যা ক্ষত শুকাতে সাহায্য করে।",
                "avoid": "কাটা স্থানে পানি লাগানো (প্রথম ২৪ ঘণ্টা)।",
                "warning": "রক্তপাত ১০ মিনিটের বেশি স্থায়ী হলে সেলাই লাগতে পারে।"
            },
            "পুড়ে যাওয়া (Burn)": {
                "med": "বার্নল (Burnol) বা সিলভারজিন ক্রিম লাগান।",
                "food": "ভিটামিন সি যুক্ত ফল।",
                "avoid": "বরফ ঘষা, টুথপেস্ট লাগানো, ফোসকা গলিয়ে দেওয়া।",
                "warning": "শরীরের বড় অংশ পুড়ে গেলে বা কাপড় চামড়ায় লেগে গেলে দ্রুত হাসপাতালে নিন।"
            },
            "উচ্চ রক্তচাপ (High BP)": {
                "med": "ডাক্তারের পরামর্শ ছাড়া ঔষধ খাবেন না। তাৎক্ষণিক বিশ্রামে যান।",
                "food": "টক দই, লেবুর শরবত (চিনি ছাড়া), রসুন।",
                "avoid": "লবণ (কাঁচা বা পাতে), গরুর মাংস, ধুমপান, টেনশন।",
                "warning": "ঘাড় ব্যথা, বুকে চাপ অনুভব করলে দ্রুত প্রেশার মাপান এবং হাসপাতালে যান।"
            }
        }
        info = data.get(symptom, {})
        
        t1, t2, t3, t4 = st.tabs(["💊 ঔষধ ও করণীয়", "🍲 খাবার তালিকা", "🚫 বর্জনীয়", "🚨 বিপদ চিহ্ন"])
        with t1: st.markdown(f"<div class='sym-card'><h4>💊 প্রাথমিক ঔষধ</h4><p>{info.get('med')}</p></div>", unsafe_allow_html=True)
        with t2: st.markdown(f"<div class='sym-card'><h4>🍲 কী খাবেন?</h4><p>{info.get('food')}</p></div>", unsafe_allow_html=True)
        with t3: st.markdown(f"<div class='sym-card'><h4>❌ কী খাবেন না?</h4><p>{info.get('avoid')}</p></div>", unsafe_allow_html=True)
        with t4: st.markdown(f"<div class='sym-card' style='border-color:#ff4b4b;'><h4 class='warning-text'>🚨 কখন ডাক্তার দেখাবেন?</h4><p>{info.get('warning')}</p></div>", unsafe_allow_html=True)

# --- HOSPITAL ---
elif menu == "🏥 হাসপাতাল ও ম্যাপ":
    st.markdown(f"## 🏥 {selected_district}-এর হাসপাতাল")
    filtered_hosp = df_h[df_h['District'] == selected_district]
    
    if not filtered_hosp.empty:
        tab1, tab2 = st.tabs(["📋 হাসপাতালের তালিকা", "🗺️ লাইভ লোকেশন ম্যাপ"])
        with tab1:
            for _, row in filtered_hosp.iterrows():
                st.markdown(f"""
                <div class="hosp-card" style="border-left: 5px solid #ff4b4b;">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <h3 style="margin:0;">{row['Name']}</h3>
                            <p style="color:#bbb; margin-top:5px;">📍 {row['Location']}</p>
                        </div>
                        <div style="align-self:center;">
                            <a href="tel:{row['Phone']}"><button style="background:#ff4b4b; box-shadow:0 0 15px rgba(255,75,75,0.5);">📞 কল করুন</button></a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        with tab2:
            avg_lat, avg_lon = filtered_hosp['Lat'].mean(), filtered_hosp['Lon'].mean()
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=13)
            for _, row in filtered_hosp.iterrows():
                folium.Marker([row['Lat'], row['Lon']], popup=row['Name'], icon=folium.Icon(color="red", icon="plus-sign")).add_to(m)
            folium_static(m)
    else:
        st.warning("এই জেলার হাসপাতালের তথ্য আপডেট করা হচ্ছে...")

# --- DOCTOR ---
elif menu == "👨‍⚕️ ডাক্তার খুঁজুন":
    st.markdown(f"## 👨‍⚕️ {selected_district}-এর বিশেষজ্ঞ ডাক্তার")
    c1, c2 = st.columns([2, 1])
    with c2: st_lottie(anim_doc, height=150)
    
    filtered_docs = df_d[df_d['District'] == selected_district]
    
    if not filtered_docs.empty:
        specs = ["সকল বিভাগ"] + sorted(filtered_docs['Specialty'].unique().tolist())
        choice = st.selectbox("বিভাগ ফিল্টার করুন:", specs)
        if choice != "সকল বিভাগ": filtered_docs = filtered_docs[filtered_docs['Specialty'] == choice]
        
        st.markdown("---")
        cols = st.columns(2)
        for i, (index, row) in enumerate(filtered_docs.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="doc-card" style="border-left: 5px solid #00c6ff;">
                    <div style="display:flex; align-items:center; margin-bottom:15px;">
                        <img src="https://cdn-icons-png.flaticon.com/512/3774/3774299.png" width="60" style="margin-right:15px; filter: drop-shadow(0 0 5px #00c6ff);">
                        <div>
                            <h3 style="margin:0; font-weight:800;">{row['Name']}</h3>
                            <span style="color:#00c6ff; font-weight:bold; letter-spacing:1px;">{row['Specialty']}</span>
                        </div>
                    </div>
                    <p style="font-size:0.9rem; margin:5px 0;">🏥 {row['Hospital']}</p>
                    <a href="tel:{row['Phone']}"><button style="margin-top:10px;">📞 অ্যাপয়েন্টমেন্ট নিন</button></a>
                </div>
                """, unsafe_allow_html=True)

# --- AMBULANCE ---
elif menu == "🚑 অ্যাম্বুলেন্স":
    st.markdown("## 🚑 অ্যাম্বুলেন্স সার্ভিস")
    
    c1, c2 = st.columns([1, 1])
    with c1: st_lottie(anim_amb, height=220)
    with c2:
        st.markdown("""
        <div class="feature-card" style="border-left:5px solid #ff4b4b; background:rgba(255, 75, 75, 0.1);">
            <h3 class="warning-text" style="margin-top:0;">⚠️ কল করার আগে প্রস্তুতি নিন:</h3>
            <ul style="padding-left:20px;">
                <li>রোগীর বর্তমান অবস্থা পরিষ্কারভাবে বলুন।</li>
                <li>সঠিক লোকেশন এবং ল্যান্ডমার্ক দিন।</li>
                <li>রোগীর বয়স এবং জেন্ডার জানান।</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    filtered_amb = df_a[(df_a['District'] == selected_district) | (df_a['District'] == 'All BD')]
    if not filtered_amb.empty:
        for _, row in filtered_amb.iterrows():
            st.markdown(f"""
            <div class="amb-card" style="display:flex; justify-content:space-between; align-items:center; border-color:#ff4b4b;">
                <div>
                    <h3>🚑 {row['ServiceName']}</h3>
                    <h2 class="warning-text" style="text-shadow:0 0 10px #ff4b4b;">{row['Contact']}</h2>
                </div>
                <a href="tel:{row['Contact']}"><button style="background:#ff4b4b; width:auto; box-shadow:0 0 15px rgba(255,75,75,0.5);">📞 কল করুন</button></a>
            </div>
            """, unsafe_allow_html=True)

# --- BMI & DIET PLAN ---
elif menu == "📊 BMI ও ডায়েট":
    st.markdown("## 📊 ফিটনেস চেক ও ডায়েট প্ল্যান")
    c_anim, c_in = st.columns([1, 2])
    with c_anim: if anim_bmi: st_lottie(anim_bmi, height=200)
    with c_in:
        st.write("আপনার তথ্য দিন এবং পুর্নাঙ্গ ডায়েট চার্ট নিন।")
        weight = st.number_input("ওজন (kg):", 30.0, 150.0, 60.0)
        c1, c2 = st.columns(2)
        with c1: feet = st.number_input("উচ্চতা (ফুট):", 2, 8, 5)
        with c2: inch = st.number_input("ইঞ্চি:", 0, 11, 6)
        calc = st.button("হিসাব করুন ও ডায়েট চার্ট দেখুন 🥗")

    if calc:
        h_m = ((feet*12)+inch)*0.0254
        bmi = weight/(h_m**2)
        
        status, color, diet, anim_res = "", "", "", ""
        
        if bmi < 18.5:
            status = "⚠️ ওজন কম (Underweight)"
            color = "#f0ad4e"
            diet = """* **সকাল:** ২টা ডিম, ২টা রুটি, ১ গ্লাস দুধ, কলা।\n* **দুপুর:** মুরগির মাংস/মাছ, ঘন ডাল, বেশি করে ভাত, সবজি।\n* **রাত:** ১ গ্লাস দুধ, খেজুর, রুটি/ভাত।"""
        elif 18.5 <= bmi < 24.9:
            status = "✅ সুস্বাস্থ্য (Healthy)"
            color = "#5cb85c"
            diet = """* **সকাল:** ১টা রুটি/ওটস, সবজি, ১টা ডিম।\n* **দুপুর:** ১ কাপ ভাত, মাছ/মাংস, সালাদ, ডাল।\n* **রাত:** হালকা খাবার, সুপ বা রুটি।"""
        else:
            status = "🚨 ওজন বেশি (Overweight)"
            color = "#d9534f"
            diet = """* **সকাল:** ওটস/লাল আটার রুটি (চিনি ছাড়া), গ্রিন টি।\n* **দুপুর:** ১ কাপ ভাত, প্রচুর সবজি, ছোট মাছ (তেল কম)।\n* **রাত:** সালাদ, সুপ বা ১টা রুটি।"""

        st.markdown("---")
        c_res, c_diet = st.columns([1, 2])
        with c_res:
            st.markdown(f"""
            <div class="feature-card" style="background:{color}; border:none; box-shadow:0 0 30px {color};">
                <h1>BMI: {bmi:.1f}</h1>
                <h3>{status}</h3>
            </div>
            """, unsafe_allow_html=True)
        with c_diet:
             st.markdown(f"""<div class="feature-card"><h3>🥗 আপনার জন্য ডায়েট চার্ট:</h3>{diet}</div>""", unsafe_allow_html=True)
