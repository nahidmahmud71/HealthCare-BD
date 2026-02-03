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

# ================= 2. SPLASH SCREEN (INTRO) =================
if 'splash_shown' not in st.session_state:
    st.session_state.splash_shown = False

if not st.session_state.splash_shown:
    st.markdown("""
    <style>
        .stApp { background-color: #000000; }
        .intro-box {
            height: 90vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            animation: fadeIn 2s ease-in-out;
        }
        .name-title {
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(to right, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 15px;
            text-shadow: 0 0 30px rgba(0, 198, 255, 0.6);
        }
        .uni-sub { font-size: 2.2rem; color: white; font-weight: 700; }
        .college-sub { font-size: 1.3rem; color: #bbb; font-style: italic; margin-top: 10px; }
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
    </style>
    <div class="intro-box">
        <div class="name-title">MD NAHID MAHMUD</div>
        <div class="uni-sub">Southeast University</div>
        <div class="college-sub">Former Student: Cantonment College Jashore</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(4.5)
    st.session_state.splash_shown = True
    st.rerun()

# ================= 3. ASSETS =================
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

# ================= 4. DARK GALAXY THEME CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    
    /* --- ANIMATED BACKGROUND --- */
    @keyframes galaxy {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    [data-testid="stAppViewContainer"] {
        /* Deep Dark Blue Galaxy Gradient */
        background: linear-gradient(-45deg, #020024, #002c5f, #000814, #010b1c);
        background-size: 400% 400%;
        animation: galaxy 15s ease infinite;
        color: white;
        font-family: 'Poppins', sans-serif;
    }

    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 5, 20, 0.95);
        border-right: 1px solid rgba(0, 198, 255, 0.1);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* --- GLASS CARDS --- */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }
    
    .feature-card, .doc-card, .hosp-card, .sym-card, .amb-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
        transition: 0.3s;
        animation: float 6s ease-in-out infinite;
    }
    
    .feature-card:hover, .doc-card:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: #00d4ff;
        transform: scale(1.02);
    }

    /* Text Colors */
    h1, h2, h3, h4, h5, p, div, span, label { color: white !important; }
    .highlight { color: #00d4ff !important; font-weight: bold; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5); }
    .warning { color: #ff6b6b !important; font-weight: bold; }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff, #005bea);
        color: white !important;
        border: none;
        border-radius: 50px;
        padding: 12px 25px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.8);
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
    st.divider()
    selected_district = st.selectbox("📍 জেলা নির্বাচন করুন:", ALL_DISTRICTS, index=ALL_DISTRICTS.index("Dhaka"))
    st.write("")
    menu = st.radio("মেনু:", ["🏠 হোম পেজ", "🤒 প্রাথমিক চিকিৎসা", "🏥 হাসপাতাল ও ম্যাপ", "👨‍⚕️ ডাক্তার খুঁজুন", "🚑 অ্যাম্বুলেন্স", "📊 BMI ও ডায়েট"])
    st.divider()
    st.info("🚨 জরুরী: **999**")

# ================= 7. MAIN CONTENT =================

# --- HOME ---
if menu == "🏠 হোম পেজ":
    st.markdown("<h1 style='text-align:center; font-size:3.5rem; text-shadow:0 0 20px #00d4ff;'>HealthPlus Bangladesh</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>জেলা: <b class='highlight'>{selected_district}</b> | স্মার্ট স্বাস্থ্য সেবা</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        st.write("### 👋 স্বাগতম!")
        st.write("HealthPlus BD অ্যাপে আপনাকে স্বাগতম। আমরা দিচ্ছি ৬৪ জেলার পূর্ণাঙ্গ স্বাস্থ্য সেবা।")
        
        # Stats
        h_cnt = len(df_h[df_h['District'] == selected_district])
        d_cnt = len(df_d[df_d['District'] == selected_district])
        
        s1, s2 = st.columns(2)
        with s1: st.markdown(f"<div class='feature-card'><h1 class='highlight'>{h_cnt}</h1><p>হাসপাতাল</p></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='feature-card'><h1 class='highlight'>{d_cnt}</h1><p>ডাক্তার</p></div>", unsafe_allow_html=True)

    with c2:
        if anim_home: st_lottie(anim_home, height=280)

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown("<div class='feature-card'><h1>🤒</h1><h4>Symptom</h4></div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='feature-card'><h1>👨‍⚕️</h1><h4>Doctor</h4></div>", unsafe_allow_html=True)
    with col3: st.markdown("<div class='feature-card'><h1>🚑</h1><h4>Ambulance</h4></div>", unsafe_allow_html=True)
    with col4: st.markdown("<div class='feature-card'><h1>📊</h1><h4>Diet</h4></div>", unsafe_allow_html=True)

# --- SYMPTOM CHECKER (DETAILED) ---
elif menu == "🤒 প্রাথমিক চিকিৎসা":
    st.markdown("## 🤒 বিস্তারিত প্রাথমিক চিকিৎসা")
    c1, c2 = st.columns([1, 2])
    with c1: 
        if anim_symptom: st_lottie(anim_symptom, height=200)
    with c2:
        symptom = st.selectbox("কোন সমস্যাটি হচ্ছে?", 
            ["বাছাই করুন...", "জ্বর (Fever)", "ঠান্ডা/সর্দি (Common Cold)", "গ্যাস্ট্রিক/বুক জ্বালা", "মাথা ব্যথা", "শরীরে কাটা/ক্ষত", "পুড়ে যাওয়া (Burn)", "ডায়রিয়া", "ডেঙ্গু লক্ষণ (Dengue)", "উচ্চ রক্তচাপ (High BP)"]
        )

    if symptom != "বাছাই করুন...":
        st.markdown(f"### 🩺 পরামর্শ: <span class='highlight'>{symptom}</span>", unsafe_allow_html=True)
        data = {
            "জ্বর (Fever)": {
                "med": "প্যারাসিটামল (Napa/Ace) ৫০০ মিগ্রা। দিনে ৩ বার ভরা পেটে।",
                "food": "পাতলা স্যুপ, ফলের রস, জাউভাত।",
                "avoid": "ঠান্ডা পানি, আইসক্রিম, ভাজাপোড়া।",
                "warn": "জ্বর ১০৩° এর বেশি হলে বা ৩ দিনের বেশি থাকলে ডাক্তার দেখান।"
            },
            "ঠান্ডা/সর্দি (Common Cold)": {
                "med": "অ্যান্টিহিস্টামিন (Fexo 120mg) রাতে ১টি। নাক বন্ধ থাকলে Antazol ড্রপ।",
                "food": "আদা চা, মধু, গরম পানি, লেবু।",
                "avoid": "ঠান্ডা বাতাস, ধুমপান।",
                "warn": "শ্বাসকষ্ট হলে বা বুকে কফ জমে গেলে দ্রুত ডাক্তার দেখান।"
            },
            "গ্যাস্ট্রিক/বুক জ্বালা": {
                "med": "এন্টাসিড সিরাপ ২ চামচ অথবা ওমিপ্রাজল (Seclo 20mg) খাওয়ার আগে।",
                "food": "শসা, ডাবের পানি, ঠান্ডা দুধ, পেঁপে।",
                "avoid": "ঝাল, মশলাদার খাবার, খালি পেটে থাকা।",
                "warn": "বুকে তীব্র ব্যথা হলে (যা পিঠে ছড়ায়) হার্ট অ্যাটাক হতে পারে।"
            },
            "মাথা ব্যথা": {
                "med": "প্যারাসিটামল (Napa Extra) অথবা Tufnil (মাইগ্রেন হলে)।",
                "food": "বাদাম, পানি, ম্যাগনেসিয়াম সমৃদ্ধ খাবার।",
                "avoid": "মোবাইল স্ক্রিন, কড়া রোদ, অনিদ্রা।",
                "warn": "বমি বা চোখে ঝাপসা দেখলে নিউরোলোজিস্ট দেখান।"
            },
            "ডেঙ্গু লক্ষণ (Dengue)": {
                "med": "শুধুমাত্র প্যারাসিটামল। অন্য কোনো ব্যথানাশক (Painkiller) খাবেন না।",
                "food": "প্রচুর স্যালাইন, ডাব, পেঁপে পাতার রস।",
                "avoid": "লাল রঙের খাবার (যাতে রক্তক্ষরণ বোঝা যায় না)।",
                "warn": "দাঁত/নাক দিয়ে রক্ত পড়লে বা পেট ব্যথা হলে ইমার্জেন্সি।"
            },
            "ডায়রিয়া": {
                "med": "খাওয়ার স্যালাইন (Orsaline-N) প্রতিবার পায়খানার পর। জিংক ট্যাবলেট।",
                "food": "জাউভাত, কাঁচাকলা ভর্তা।",
                "avoid": "দুধ, শাক, বাইরের খাবার।",
                "warn": "প্রস্রাব ৬ ঘণ্টার বেশি বন্ধ থাকলে হাসপাতালে স্যালাইন দিতে হবে।"
            },
             "শরীরে কাটা/ক্ষত": {
                "med": "স্যাভলন বা Povidone Iodine দিয়ে পরিষ্কার করুন।",
                "food": "প্রোটিন যুক্ত খাবার (ডিম, মাছ)।",
                "avoid": "কাটা স্থানে পানি লাগানো।",
                "warn": "রক্তপাত ১০ মিনিটের বেশি হলে সেলাই লাগতে পারে।"
            },
            "পুড়ে যাওয়া (Burn)": {
                "med": "সিলভারজিন ক্রিম বা বার্নল মলম লাগান।",
                "food": "ভিটামিন সি যুক্ত ফল।",
                "avoid": "বরফ ঘষা, টুথপেস্ট লাগানো।",
                "warn": "ফোসকা গলিয়ে দেবেন না। কাপড় চামড়ায় লেগে গেলে হাসপাতালে যান।"
            },
            "উচ্চ রক্তচাপ (High BP)": {
                "med": "ডাক্তারের পরামর্শ ছাড়া ঔষধ খাবেন না। তাৎক্ষণিক বিশ্রামে যান।",
                "food": "টক দই, লেবু, রসুন।",
                "avoid": "লবণ, গরুর মাংস, টেনশন।",
                "warn": "ঘাড় ব্যথা বা বুকে চাপ অনুভব করলে হাসপাতালে যান।"
            }
        }
        info = data.get(symptom, {})
        
        t1, t2, t3, t4 = st.tabs(["💊 ঔষধ", "🍲 খাবার", "🚫 বর্জনীয়", "🚨 সতর্কতা"])
        with t1: st.markdown(f"<div class='sym-card'><h4>প্রাথমিক ঔষধ</h4><p>{info.get('med')}</p></div>", unsafe_allow_html=True)
        with t2: st.markdown(f"<div class='sym-card'><h4>কী খাবেন</h4><p>{info.get('food')}</p></div>", unsafe_allow_html=True)
        with t3: st.markdown(f"<div class='sym-card'><h4>কী খাবেন না</h4><p>{info.get('avoid')}</p></div>", unsafe_allow_html=True)
        with t4: st.markdown(f"<div class='sym-card' style='border-color:#ff6b6b;'><h4 class='warning'>সতর্কতা</h4><p>{info.get('warn')}</p></div>", unsafe_allow_html=True)

# --- HOSPITAL ---
elif menu == "🏥 হাসপাতাল ও ম্যাপ":
    st.markdown(f"## 🏥 {selected_district}-এর হাসপাতাল")
    filtered_hosp = df_h[df_h['District'] == selected_district]
    
    if not filtered_hosp.empty:
        tab1, tab2 = st.tabs(["📋 তালিকা", "🗺️ ম্যাপ"])
        with tab1:
            for _, row in filtered_hosp.iterrows():
                st.markdown(f"""
                <div class="hosp-card">
                    <div style="display:flex; justify-content:space-between;">
                        <div><h3>{row['Name']}</h3><p style="color:#ccc;">📍 {row['Location']}</p></div>
                        <a href="tel:{row['Phone']}"><button>📞 কল করুন</button></a>
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
        st.warning("তথ্য আপডেট করা হচ্ছে...")

# --- DOCTOR ---
elif menu == "👨‍⚕️ ডাক্তার খুঁজুন":
    st.markdown(f"## 👨‍⚕️ {selected_district}-এর ডাক্তার")
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
                <div class="doc-card" style="border-left: 5px solid #00d4ff;">
                    <div style="display:flex; align-items:center;">
                        <div style="font-size:2rem; margin-right:15px;">👨‍⚕️</div>
                        <div>
                            <h3 style="margin:0;">{row['Name']}</h3>
                            <span class="highlight">{row['Specialty']}</span>
                            <p style="font-size:0.9rem;">🏥 {row['Hospital']}</p>
                        </div>
                    </div>
                    <a href="tel:{row['Phone']}"><button style="margin-top:10px;">📞 অ্যাপয়েন্টমেন্ট</button></a>
                </div>
                """, unsafe_allow_html=True)

# --- AMBULANCE ---
elif menu == "🚑 অ্যাম্বুলেন্স":
    st.markdown("## 🚑 অ্যাম্বুলেন্স সার্ভিস")
    c1, c2 = st.columns([1, 1])
    with c1: st_lottie(anim_amb, height=200)
    with c2:
        st.markdown("""
        <div class="feature-card" style="border-left:5px solid #ff6b6b;">
            <h3 class="warning">⚠️ কল করার চেকলিস্ট:</h3>
            <ul>
                <li>রোগীর বর্তমান অবস্থা (অজ্ঞান/রক্তপাত/হার্ট অ্যাটাক)</li>
                <li>সঠিক লোকেশন ও ল্যান্ডমার্ক</li>
                <li>রোগীর বয়স ও জেন্ডার</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    filtered_amb = df_a[(df_a['District'] == selected_district) | (df_a['District'] == 'All BD')]
    if not filtered_amb.empty:
        for _, row in filtered_amb.iterrows():
            st.markdown(f"""
            <div class="amb-card" style="display:flex; justify-content:space-between; align-items:center;">
                <div><h3>🚑 {row['ServiceName']}</h3><h2 class="warning">{row['Contact']}</h2></div>
                <a href="tel:{row['Contact']}"><button style="background:#ff6b6b; width:auto;">📞 কল করুন</button></a>
            </div>
            """, unsafe_allow_html=True)

# --- BMI & DIET PLAN (DETAILED) ---
elif menu == "📊 BMI ও ডায়েট":
    st.markdown("## 📊 ফিটনেস চেক ও ডায়েট")
    c_anim, c_in = st.columns([1, 2])
    with c_anim: if anim_bmi: st_lottie(anim_bmi, height=200)
    with c_in:
        weight = st.number_input("ওজন (kg):", 30.0, 150.0, 60.0)
        c1, c2 = st.columns(2)
        with c1: feet = st.number_input("উচ্চতা (ফুট):", 2, 8, 5)
        with c2: inch = st.number_input("ইঞ্চি:", 0, 11, 6)
        calc = st.button("হিসাব করুন ও চার্ট দেখুন 🥗")

    if calc:
        h_m = ((feet*12)+inch)*0.0254
        bmi = weight/(h_m**2)
        
        status, color, diet = "", "", ""
        if bmi < 18.5:
            status = "ওজন কম (Underweight)"
            color = "#f0ad4e"
            diet = """
            * **সকাল:** ২টা ডিম, ২টা রুটি, ১ গ্লাস দুধ, কলা।
            * **দুপুর:** মুরগির মাংস/মাছ, ঘন ডাল, বেশি করে ভাত, সবজি।
            * **বিকাল:** বাদাম, দই, ফলের রস।
            * **রাত:** ১ গ্লাস দুধ, খেজুর, রুটি/ভাত।
            """
        elif 18.5 <= bmi < 24.9:
            status = "সুস্বাস্থ্য (Healthy)"
            color = "#5cb85c"
            diet = """
            * **সকাল:** ১টা রুটি/ওটস, সবজি, ১টা ডিম।
            * **দুপুর:** ১ কাপ ভাত, মাছ/মাংস, সালাদ, ডাল।
            * **বিকাল:** গ্রিন টি, বিস্কুট।
            * **রাত:** হালকা খাবার, সুপ বা রুটি।
            """
        else:
            status = "ওজন বেশি (Overweight)"
            color = "#d9534f"
            diet = """
            * **সকাল:** ওটস/লাল আটার রুটি (চিনি ছাড়া), গ্রিন টি।
            * **দুপুর:** ১ কাপ ভাত, প্রচুর সবজি, ছোট মাছ (তেল কম)।
            * **বিকাল:** শসা, ফল (চিনি ছাড়া)।
            * **রাত:** সালাদ, সুপ বা ১টা রুটি। (৮টার মধ্যে খাবেন)
            """

        st.markdown(f"""
        <div class="feature-card" style="border-top: 5px solid {color};">
            <h1 style="color:{color} !important;">BMI: {bmi:.1f}</h1>
            <h3>{status}</h3>
            <hr style="border-top: 1px solid rgba(255,255,255,0.2);">
            <p style="text-align:left;"><b>🥗 আপনার জন্য ডায়েট চার্ট:</b></p>
            <div style="text-align:left;">{diet}</div>
        </div>
        """, unsafe_allow_html=True)
