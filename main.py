import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import time
import folium
from streamlit_folium import folium_static

# ================= 1. PAGE CONFIGURATION =================
st.set_page_config(
    page_title="HealthPlus BD | Premium",
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
        .stApp { background-color: #000000; }
        .intro-box {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 90vh;
            animation: zoomIn 2s ease-out;
        }
        .dev-title {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(to right, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }
        .uni-sub {
            font-size: 2rem;
            color: #e0e0e0;
            font-weight: 600;
        }
        .college-sub {
            font-size: 1.2rem;
            color: #a0a0a0;
            font-style: italic;
            margin-top: 10px;
        }
        @keyframes zoomIn {
            0% { transform: scale(0.5); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }
    </style>
    <div class="intro-box">
        <div class="dev-title">MD NAHID MAHMUD</div>
        <div class="uni-sub">Southeast University</div>
        <div class="college-sub">Former Student: Cantonment College Jashore</div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(4)
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

anim_home = load_lottie("https://assets10.lottiefiles.com/packages/lf20_pnycZg.json")
anim_doc = load_lottie("https://assets10.lottiefiles.com/packages/lf20_5njp3vgg.json")
anim_amb = load_lottie("https://assets9.lottiefiles.com/packages/lf20_z4cshyhf.json")
anim_symptom = load_lottie("https://lottie.host/58819173-0740-4a80-9646-7a8311145491/6S5u5Q0D32.json")
anim_bmi = load_lottie("https://assets2.lottiefiles.com/packages/lf20_wopcsux6.json")

# ================= 4. ADVANCED DARK THEME CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    
    /* --- DARK BLUE ANIMATED BACKGROUND --- */
    @keyframes gradientDark {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #0f0c29);
        background-size: 400% 400%;
        animation: gradientDark 15s ease infinite;
        color: white;
        font-family: 'Poppins', sans-serif;
    }

    /* --- SIDEBAR (Dark Glass) --- */
    [data-testid="stSidebar"] {
        background: rgba(15, 32, 39, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    /* Radio Buttons */
    .stRadio > div > label {
        background-color: rgba(255, 255, 255, 0.1);
        color: white !important;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        transition: 0.3s;
    }
    .stRadio > div > label:hover {
        background-color: #00c6ff;
        color: black !important;
    }
    div[role="radiogroup"] > label > div:first-of-type {
        background-color: #00c6ff !important;
    }

    /* --- CARDS (Dark Glassmorphism) --- */
    .feature-card, .doc-card, .hosp-card, .sym-card, .amb-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
        animation: fadeInUp 0.8s ease;
    }
    .feature-card:hover, .doc-card:hover {
        transform: translateY(-5px);
        border-color: #00c6ff;
    }
    
    /* Text Colors inside Cards */
    h1, h2, h3, h4, h5, p, div, span {
        color: white !important;
    }
    
    /* Specific Colors */
    .highlight-text { color: #00c6ff !important; font-weight: bold; }
    .warning-text { color: #ff6b6b !important; font-weight: bold; }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white !important;
        border-radius: 50px;
        font-weight: bold;
        border: none;
        padding: 12px 25px;
        width: 100%;
        transition: 0.3s;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.5);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(0, 198, 255, 0.8);
    }

    /* Animation Keyframes */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
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
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063205.png", width=80)
    st.markdown("### HealthPlus BD")
    st.write("স্মার্ট হেলথ পার্টনার")
    
    st.divider()
    
    selected_district = st.selectbox("📍 জেলা নির্বাচন করুন:", ALL_DISTRICTS, index=ALL_DISTRICTS.index("Dhaka"))
    
    st.write("")
    menu = st.radio("মেনু নেভিগেশন:", 
        ["🏠 হোম পেজ", "🤒 প্রাথমিক চিকিৎসা", "🏥 হাসপাতাল ও ম্যাপ", "👨‍⚕️ ডাক্তার খুঁজুন", "🚑 অ্যাম্বুলেন্স", "📊 BMI ও ডায়েট"]
    )
    st.divider()
    st.markdown("<div style='text-align:center; padding:10px; background:rgba(255,0,0,0.2); border-radius:10px;'>🚨 জরুরী: <b>999</b></div>", unsafe_allow_html=True)

# ================= 7. MAIN CONTENT (DETAILED & EXPANDED) =================

# --- HOME ---
if menu == "🏠 হোম পেজ":
    st.markdown("<h1 style='text-align:center; font-size:3.5rem; text-shadow:0 0 20px #00c6ff;'>HealthPlus Bangladesh</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>জেলা: <b class='highlight-text'>{selected_district}</b> | আপনার বিশ্বস্ত স্বাস্থ্য সাথী</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        st.write("### 👋 স্বাগতম!")
        st.write("""
        HealthPlus BD অ্যাপে আপনাকে স্বাগতম। এটি বাংলাদেশের সবচেয়ে আধুনিক স্বাস্থ্য সেবা অ্যাপ।
        আমরা শুধুমাত্র তথ্য দিচ্ছি না, আমরা দিচ্ছি পূর্ণাঙ্গ গাইডলাইন।
        """)
        
        st.markdown("""
        **কেন এই অ্যাপটি সেরা?**
        * ✅ ৬৪ জেলার যাচাইকৃত তথ্য
        * ✅ রোগের বিস্তারিত প্রাথমিক চিকিৎসা
        * ✅ BMI অনুযায়ী ডায়েট চার্ট
        * ✅ ২৪/৭ অ্যাম্বুলেন্স সাপোর্ট
        """)
        
        # Stats with Glass Cards
        s1, s2 = st.columns(2)
        h_n = len(df_h[df_h['District']==selected_district])
        d_n = len(df_d[df_d['District']==selected_district])
        with s1: st.markdown(f"<div class='feature-card'><h2 class='highlight-text'>{h_n}</h2><p>হাসপাতাল</p></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='feature-card'><h2 class='highlight-text'>{d_n}</h2><p>ডাক্তার</p></div>", unsafe_allow_html=True)

    with c2:
        if anim_home: st_lottie(anim_home, height=300)

    st.markdown("---")
    st.subheader("🚀 কুইক ফিচারস")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown("<div class='feature-card'><h1>🤒</h1><h4>Symptom</h4><p>প্রাথমিক চিকিৎসা</p></div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='feature-card'><h1>👨‍⚕️</h1><h4>Doctor</h4><p>অ্যাপয়েন্টমেন্ট</p></div>", unsafe_allow_html=True)
    with col3: st.markdown("<div class='feature-card'><h1>🚑</h1><h4>Ambulance</h4><p>জরুরী কল</p></div>", unsafe_allow_html=True)
    with col4: st.markdown("<div class='feature-card'><h1>📊</h1><h4>Diet Plan</h4><p>ফিটনেস গাইড</p></div>", unsafe_allow_html=True)

# --- SYMPTOM CHECKER (HUGE UPDATE) ---
elif menu == "🤒 প্রাথমিক চিকিৎসা":
    st.markdown("## 🤒 বিস্তারিত প্রাথমিক চিকিৎসা")
    st.write("আপনার সমস্যা নির্বাচন করুন এবং পূর্ণাঙ্গ গাইডলাইন পান।")
    
    c_anim, c_sel = st.columns([1, 2])
    with c_anim: 
        if anim_symptom: st_lottie(anim_symptom, height=200)
    with c_sel:
        symptom = st.selectbox("কোন সমস্যাটি হচ্ছে?", 
            ["বাছাই করুন...", "জ্বর (Fever)", "গ্যাস্ট্রিক/বুক জ্বালা", "মাথা ব্যথা", "শরীরে কাটা/ক্ষত", "পুড়ে যাওয়া (Burn)", "ডায়রিয়া", "উচ্চ রক্তচাপ (High BP)"]
        )

    if symptom != "বাছাই করুন...":
        st.markdown("---")
        st.markdown(f"### 🩺 পরামর্শ: <span class='highlight-text'>{symptom}</span>", unsafe_allow_html=True)
        
        # Comprehensive Data Dictionary
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
        
        # Using Tabs for Details
        t1, t2, t3, t4 = st.tabs(["💊 ঔষধ ও করণীয়", "apple: খাবার তালিকা", "🚫 বর্জনীয়", "🚨 কখন ডাক্তার দেখাবেন?"])
        
        with t1:
            st.markdown(f"<div class='feature-card'><h4>💊 প্রাথমিক ঔষধ</h4><p>{info.get('med')}</p></div>", unsafe_allow_html=True)
        with t2:
            st.markdown(f"<div class='feature-card'><h4>🍲 কী খাবেন?</h4><p>{info.get('food')}</p></div>", unsafe_allow_html=True)
        with t3:
            st.markdown(f"<div class='feature-card'><h4>❌ কী খাবেন না?</h4><p>{info.get('avoid')}</p></div>", unsafe_allow_html=True)
        with t4:
            st.markdown(f"<div class='feature-card'><h4 class='warning-text'>🚨 বিপদ চিহ্ন</h4><p>{info.get('warning')}</p></div>", unsafe_allow_html=True)

# --- HOSPITAL (ENHANCED CARDS) ---
elif menu == "🏥 হাসপাতাল ও ম্যাপ":
    st.markdown(f"## 🏥 {selected_district}-এর হাসপাতাল")
    
    filtered_hosp = df_h[df_h['District'] == selected_district]
    
    if not filtered_hosp.empty:
        tab1, tab2 = st.tabs(["📋 হাসপাতালের তালিকা", "🗺️ লাইভ লোকেশন ম্যাপ"])
        with tab1:
            for _, row in filtered_hosp.iterrows():
                st.markdown(f"""
                <div class="hosp-card">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <h3 style="margin:0;">{row['Name']}</h3>
                            <p style="color:#bbb;">📍 {row['Location']}</p>
                            <span style="background:#ff4b4b; padding:2px 8px; border-radius:5px; font-size:0.8rem;">Emergency 24/7</span>
                        </div>
                        <div style="align-self:center;">
                            <a href="tel:{row['Phone']}"><button style="background:#ff4b4b; border:none; padding:10px 20px; border-radius:50px; color:white; cursor:pointer;">📞 কল করুন</button></a>
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

# --- DOCTOR (PREMIUM CARDS) ---
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
                <div class="doc-card">
                    <div style="display:flex; align-items:center;">
                        <img src="https://cdn-icons-png.flaticon.com/512/3774/3774299.png" width="50" style="margin-right:15px;">
                        <div>
                            <h4 style="margin:0;">{row['Name']}</h4>
                            <span style="color:#00c6ff; font-weight:bold; font-size:0.9rem;">{row['Specialty']}</span>
                            <p style="font-size:0.8rem; margin:5px 0;">🏥 {row['Hospital']}</p>
                        </div>
                    </div>
                    <a href="tel:{row['Phone']}"><button style="margin-top:10px; background:linear-gradient(90deg, #11998e, #38ef7d);">📞 অ্যাপয়েন্টমেন্ট নিন</button></a>
                </div>
                """, unsafe_allow_html=True)

# --- AMBULANCE (WITH TIPS) ---
elif menu == "🚑 অ্যাম্বুলেন্স":
    st.markdown("## 🚑 অ্যাম্বুলেন্স সার্ভিস")
    
    c1, c2 = st.columns([1, 1])
    with c1: st_lottie(anim_amb, height=200)
    with c2:
        st.markdown("""
        <div class="feature-card" style="border-left:5px solid #ff4b4b;">
            <h3 class="warning-text">কল করার আগে প্রস্তুতি নিন:</h3>
            <ul>
                <li>রোগীর বর্তমান অবস্থা বলুন।</li>
                <li>সঠিক লোকেশন এবং ল্যান্ডমার্ক দিন।</li>
                <li>রোগীর বয়স এবং জেন্ডার জানান।</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    filtered_amb = df_a[(df_a['District'] == selected_district) | (df_a['District'] == 'All BD')]
    if not filtered_amb.empty:
        for _, row in filtered_amb.iterrows():
            st.markdown(f"""
            <div class="amb-card" style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h3>🚑 {row['ServiceName']}</h3>
                    <h2 class="warning-text">{row['Contact']}</h2>
                </div>
                <a href="tel:{row['Contact']}"><button style="background:#ff4b4b; width:auto;">📞 কল করুন</button></a>
            </div>
            """, unsafe_allow_html=True)

# --- BMI & DIET PLAN (NEW FEATURE) ---
elif menu == "📊 BMI ও ডায়েট":
    st.markdown("## 📊 ফিটনেস চেক ও ডায়েট প্ল্যান")
    
    col_in, col_res = st.columns([1, 1])
    with col_in:
        st.write("আপনার তথ্য দিন:")
        weight = st.number_input("ওজন (kg):", 30.0, 150.0, 60.0)
        c1, c2 = st.columns(2)
        with c1: feet = st.number_input("উচ্চতা (ফুট):", 2, 8, 5)
        with c2: inch = st.number_input("ইঞ্চি:", 0, 11, 6)
        calc = st.button("হিসাব করুন ও ডায়েট চার্ট দেখুন 🥗")

    if calc:
        h_m = ((feet*12)+inch)*0.0254
        bmi = weight/(h_m**2)
        
        status, color, diet = "", "", ""
        
        if bmi < 18.5:
            status = "⚠️ ওজন কম (Underweight)"
            color = "#f0ad4e"
            diet = """
            * **সকাল:** ২টা ডিম, ২টা রুটি, ১ গ্লাস দুধ, কলা।
            * **দুপুর:** মুরগির মাংস/মাছ, ঘন ডাল, বেশি করে ভাত, সবজি।
            * **রাত:** ১ গ্লাস দুধ, খেজুর, রুটি/ভাত।
            * **পরামর্শ:** প্রোটিন ও কার্বোহাইড্রেট বেশি খান।
            """
        elif 18.5 <= bmi < 24.9:
            status = "✅ সুস্বাস্থ্য (Healthy)"
            color = "#5cb85c"
            diet = """
            * **সকাল:** ১টা রুটি/ওটস, সবজি, ১টা ডিম।
            * **দুপুর:** ১ কাপ ভাত, মাছ/মাংস, সালাদ, ডাল।
            * **রাত:** হালকা খাবার, সুপ বা রুটি।
            * **পরামর্শ:** বর্তমান রুটিন মেনে চলুন, নিয়মিত ব্যায়াম করুন।
            """
        else:
            status = "🚨 ওজন বেশি (Overweight)"
            color = "#d9534f"
            diet = """
            * **সকাল:** ওটস/লাল আটার রুটি (চিনি ছাড়া), গ্রিন টি।
            * **দুপুর:** ১ কাপ ভাত, প্রচুর সবজি, ছোট মাছ (তেল কম)।
            * **রাত:** সালাদ, সুপ বা ১টা রুটি।
            * **পরামর্শ:** চিনি ও ভাজাপোড়া বাদ দিন। প্রতিদিন ৪৫ মিনিট হাঁটুন।
            """

        with col_res:
            st.markdown(f"""
            <div style="background:{color}; padding:20px; border-radius:15px; text-align:center;">
                <h1>BMI: {bmi:.1f}</h1>
                <h3>{status}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🥗 আপনার জন্য ডায়েট চার্ট:")
        st.info(diet)
