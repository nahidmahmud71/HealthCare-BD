import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from streamlit_lottie import st_lottie
import requests
import time

# ================= 1. APP CONFIGURATION =================
st.set_page_config(
    page_title="HealthPlus BD | Ultimate Health Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. ASSET LOADING (ANIMATIONS) =================
@st.cache_data
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Premium Lottie Animations
anim_welcome = load_lottie("https://assets10.lottiefiles.com/packages/lf20_pnycZg.json") # Doctor wave
anim_map = load_lottie("https://assets9.lottiefiles.com/packages/lf20_s5id889b.json") # Map location
anim_amb = load_lottie("https://assets2.lottiefiles.com/packages/lf20_z4cshyhf.json") # Ambulance
anim_blood = load_lottie("https://assets5.lottiefiles.com/packages/lf20_gjpogvz8.json") # Blood donation
anim_bmi_healthy = load_lottie("https://assets2.lottiefiles.com/packages/lf20_wopcsux6.json") # Healthy person
anim_bmi_warning = load_lottie("https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json") # Overweight person
anim_symptom = load_lottie("https://lottie.host/58819173-0740-4a80-9646-7a8311145491/6S5u5Q0D32.json") # Checking symptom

# ================= 3. ADVANCED COLORFUL CSS =================
st.markdown("""
<style>
    /* Global Themes & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        background-color: #F0F4F8; /* Soft light blue bg */
    }
    
    /* Modern Gradient Titles */
    .main-header {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00C6FF, #0072FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0px 5px 15px rgba(0, 114, 255, 0.2);
    }
    
    .section-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #333;
        border-left: 8px solid #00C6FF;
        padding-left: 15px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* Dashboard Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #e6e6e6);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 5px 5px 15px #d1d1d1, -5px -5px 15px #ffffff;
        transition: transform 0.3s;
    }
    .metric-card:hover { transform: translateY(-10px); }
    .metric-card h1 { margin: 0; font-size: 3rem; color: #0072FF; }
    .metric-card p { color: #666; font-weight: 600; }

    /* Feature Link Cards */
    .feature-link-card {
        background: white;
        padding: 25px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border-bottom: 5px solid #FF4B4B;
        cursor: pointer;
        height: 100%;
    }
    .feature-link-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 35px rgba(255, 75, 75, 0.25);
    }
    .feature-link-card h2 { font-size: 3rem; margin-bottom: 10px; }

    /* Hospital Info Card */
    .hosp-card {
        background: #fff;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #FF4B4B;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .hosp-card:hover { box-shadow: 0 8px 25px rgba(255, 75, 75, 0.2); }

    /* Doctor Info Card */
    .doc-card {
        background: #fff;
        padding: 20px;
        border-radius: 15px;
        border-top: 5px solid #00C6FF;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }

    /* BMI Calculator Result Styling */
    .bmi-result-box {
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-top: 20px;
    }
    .bmi-healthy { background: linear-gradient(135deg, #28a745, #a8e063); }
    .bmi-warning { background: linear-gradient(135deg, #ffc107, #f76b1c); }
    .bmi-danger { background: linear-gradient(135deg, #dc3545, #ff4b2b); }

    /* Buttons */
    .stButton>button {
        border-radius: 50px;
        background: linear-gradient(90deg, #00C6FF, #0072FF);
        color: white;
        border: none;
        padding: 12px 25px;
        font-weight: 600;
        width: 100%;
        transition: 0.3s;
        box-shadow: 0 5px 15px rgba(0, 114, 255, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0, 114, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ================= 4. DATA LOADING (ROBUST) =================
@st.cache_data
def load_data():
    try: df_h = pd.read_csv("hospitals_64.csv")
    except: df_h = pd.DataFrame(columns=["District", "Name", "Location", "Phone", "Lat", "Lon"])
    
    try: df_d = pd.read_csv("doctors_64.csv")
    except: df_d = pd.DataFrame(columns=["District", "Name", "Specialty", "Hospital", "Phone"])
    
    try: df_a = pd.read_csv("ambulances_64.csv")
    except: df_a = pd.DataFrame(columns=["District", "ServiceName", "Contact"])
    
    return df_h, df_d, df_a

df_hosp, df_doc, df_amb = load_data()

# ================= 5. SIDEBAR NAVIGATION =================
with st.sidebar:
    if anim_welcome: st_lottie(anim_welcome, height=150, key="side_anim")
    st.markdown("### 🩺 HealthPlus BD")
    st.write("আপনার ডিজিটাল স্বাস্থ্য সঙ্গী")
    
    # --- Global District Filter ---
    all_districts = sorted(df_hosp['District'].unique().tolist()) if not df_hosp.empty else ["Dhaka"]
    selected_district = st.selectbox("📍 আপনার জেলা নির্বাচন করুন:", all_districts)
    
    st.markdown("---")
    
    menu = st.radio("মেনু নির্বাচন করুন:", 
        ["🏠 ড্যাশবোর্ড", "📊 স্বাস্থ্য ক্যালকুলেটর (BMI)", "🤒 প্রাথমিক চিকিৎসা (Symptom)", "🏥 হাসপাতাল ও ম্যাপ", "👨‍⚕️ ডাক্তার খুঁজুন", "🚑 অ্যাম্বুলেন্স ও ব্লাড"]
    )
    st.divider()
    st.info("জরুরী হটলাইন: **16263** (স্বাস্থ্য বাতায়ন) বা **999**")

# ================= 6. MAIN CONTENT MODULES =================

# --- 🏠 DASHBOARD HOME ---
if menu == "🏠 ড্যাশবোর্ড":
    st.markdown("<div class='main-header'>HealthPlus Bangladesh</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#666; font-size:1.2rem;'>জেলা: <b>{selected_district}</b> | এক ছাতার নিচে সব স্বাস্থ্যসেবা</p>", unsafe_allow_html=True)

    # Hero Section with Animation
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown("## 👋 স্বাগতম!")
        st.write("""
        HealthPlus BD-তে আপনাকে স্বাগতম। এটি বাংলাদেশের সবচেয়ে আধুনিক এবং অ্যানিমেটেড হেলথ পোর্টাল। 
        আমরা আপনার জেলার স্বাস্থ্যসেবাকে আপনার হাতের মুঠোয় নিয়ে এসেছি।
        """)
        
        # Quick Stats
        dh_count = len(df_hosp[df_hosp['District'] == selected_district])
        dd_count = len(df_doc[df_doc['District'] == selected_district])
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1: st.markdown(f"<div class='metric-card'><h1>{dh_count}</h1><p>হাসপাতাল</p></div>", unsafe_allow_html=True)
        with sc2: st.markdown(f"<div class='metric-card'><h1>{dd_count}</h1><p>ডাক্তার</p></div>", unsafe_allow_html=True)
        with sc3: st.markdown(f"<div class='metric-card'><h1>24/7</h1><p>সার্ভিস</p></div>", unsafe_allow_html=True)

    with c2:
        if anim_welcome: st_lottie(anim_welcome, height=300, key="dash_hero_anim")

    st.markdown("---")
    st.subheader("🚀 আমাদের সেবাসমূহ একনজরে:")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="feature-link-card"><h2>🏥</h2><h4>হাসপাতাল</h4><p>লোকেশন ও ম্যাপ</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="feature-link-card"><h2>👨‍⚕️</h2><h4>ডাক্তার</h4><p>বিশেষজ্ঞ পরামর্শ</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="feature-link-card"><h2>📊</h2><h4>BMI চেক</h4><p>ফিটনেস ট্র্যাকার</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="feature-link-card"><h2>🚑</h2><h4>ইমার্জেন্সি</h4><p>অ্যাম্বুলেন্স ও রক্ত</p></div>""", unsafe_allow_html=True)

# --- 📊 BMI CALCULATOR (NEW FEATURE) ---
elif menu == "📊 স্বাস্থ্য ক্যালকুলেটর (BMI)":
    st.markdown("<div class='main-header'>📊 BMI ফিটনেস ক্যালকুলেটর</div>", unsafe_allow_html=True)
    st.write("আপনার উচ্চতা এবং ওজন দিয়ে জেনে নিন আপনি কতটা ফিট।")
    
    col_input, col_anim = st.columns([1, 1])
    
    with col_input:
        st.markdown("### আপনার তথ্য দিন:")
        weight = st.number_input("ওজন (Weight) - কেজিতে:", min_value=10.0, max_value=200.0, value=60.0, step=0.5)
        
        st.write("উচ্চতা (Height):")
        c_ft, c_in = st.columns(2)
        with c_ft: feet = st.number_input("ফুট (Feet):", 2, 8, 5)
        with c_in: inches = st.number_input("ইঞ্চি (Inches):", 0, 11, 6)
        
        calculate_btn = st.button("ফলাফল দেখুন 🔄")

    with col_anim:
        if anim_bmi_healthy: st_lottie(anim_bmi_healthy, height=250, key="bmi_input_anim")

    if calculate_btn:
        st.divider()
        # BMI Calculation Logic
        height_meters = ((feet * 12) + inches) * 0.0254
        bmi_score = weight / (height_meters ** 2)
        
        status = ""
        bg_class = ""
        result_anim = None
        advice = ""

        if bmi_score < 18.5:
            status = "আপনার ওজন কম (Underweight)"
            bg_class = "bmi-warning"
            result_anim = anim_bmi_warning
            advice = "পরামর্শ: পুষ্টিকর খাবার বেশি করে খান এবং ডাক্তারের পরামর্শ নিন।"
        elif 18.5 <= bmi_score < 24.9:
            status = "আপনার ওজন ঠিক আছে (Healthy) 🎉"
            bg_class = "bmi-healthy"
            result_anim = anim_bmi_healthy
            advice = "পরামর্শ: চমৎকার! সুষম খাবার এবং নিয়মিত ব্যায়াম চালিয়ে যান।"
        elif 25 <= bmi_score < 29.9:
            status = "আপনার ওজন বেশি (Overweight)"
            bg_class = "bmi-warning"
            result_anim = anim_bmi_warning
            advice = "পরামর্শ: চর্বিযুক্ত খাবার কমান এবং প্রতিদিন অন্তত ৩০ মিনিট হাঁটুন।"
        else:
            status = "আপনি স্থূলতায় ভুগছেন (Obese) 🚨"
            bg_class = "bmi-danger"
            result_anim = anim_bmi_warning
            advice = "পরামর্শ: দ্রুত একজন পুষ্টিবিদ বা ডাক্তারের সাথে পরামর্শ করুন।"

        # Display Result
        r1, r2 = st.columns([2, 1])
        with r1:
             st.markdown(f"""
            <div class='bmi-result-box {bg_class}'>
                <h3>আপনার BMI স্কোর</h3>
                <h1 style='font-size:4rem; margin:0;'>{bmi_score:.2f}</h1>
                <h4 style='margin-top:10px;'>{status}</h4>
            </div>
            """, unsafe_allow_html=True)
             st.info(advice)
        with r2:
            if result_anim: st_lottie(result_anim, height=200, key="bmi_result_anim")

# --- 🤒 SYMPTOM CHECKER (NEW FEATURE) ---
elif menu == "🤒 প্রাথমিক চিকিৎসা (Symptom)":
    st.markdown("<div class='main-header'>🤒 প্রাথমিক স্বাস্থ্য পরামর্শ</div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1.5])
    with c1:
        if anim_symptom: st_lottie(anim_symptom, height=250)
    with c2:
        st.write("### আপনার সমস্যা নির্বাচন করুন:")
        symptom = st.selectbox("লক্ষণ:", 
            ["নির্বাচন করুন...", "জ্বর (Fever)", "মাথা ব্যথা (Headache)", "গ্যাস্ট্রিক/বুক জ্বালা (Acidity)", "কাশি (Cough)", "শরীরে ব্যথা (Body Pain)"]
        )
        check_btn = st.button("পরামর্শ দেখুন 🩺")

    if check_btn and symptom != "নির্বাচন করুন...":
        st.divider()
        st.subheader(f"পরামর্শ: {symptom}-এর জন্য")
        
        advice_text = ""
        if symptom == "জ্বর (Fever)":
            advice_text = """
            * পর্যাপ্ত বিশ্রাম নিন এবং প্রচুর পানি পান করুন।
            * জ্বর ১০০°F এর বেশি হলে প্যারাসিটামল (যেমন: Napa/Ace) খেতে পারেন (প্রাপ্তবয়স্কদের জন্য ৫০০ মিগ্রা)।
            * মাথায় জলপট্টি দিন।
            * ⚠️ **সতর্কতা:** ৩ দিনের বেশি জ্বর থাকলে অবশ্যই ডাক্তার দেখান।
            """
        elif symptom == "মাথা ব্যথা (Headache)":
             advice_text = """
            * অন্ধকার ও শান্ত ঘরে কিছুক্ষণ বিশ্রাম নিন।
            * পর্যাপ্ত ঘুম নিশ্চিত করুন।
            * তীব্র ব্যথায় প্যারাসিটামল খেতে পারেন।
            * ⚠️ **সতর্কতা:** সাথে বমি বা চোখে ঝাপসা দেখলে দ্রুত ডাক্তার দেখান।
            """
        elif symptom == "গ্যাস্ট্রিক/বুক জ্বালা (Acidity)":
             advice_text = """
            * ভাজাপোড়া ও ঝাল খাবার এড়িয়ে চলুন।
            * এন্টাসিড সিরাপ বা ওমিপ্রাজল (যেমন: Seclo 20mg) খেতে পারেন।
            * একবারে পেট ভরে না খেয়ে অল্প অল্প করে বারবার খান।
            """
        elif symptom == "কাশি (Cough)":
             advice_text = """
            * হালকা গরম পানিতে লবণ দিয়ে গার্গল করুন।
            * আদা চা বা মধু-তুলসী পাতার রস খেতে পারেন।
            * ⚠️ **সতর্কতা:** কাশির সাথে শ্বাসকষ্ট বা জ্বর থাকলে ডাক্তার দেখান।
            """
        elif symptom == "শরীরে ব্যথা (Body Pain)":
             advice_text = """
            * ব্যথার স্থানে হালকা গরম সেঁক দিতে পারেন।
            * বিশ্রাম নিন।
            * অতিরিক্ত ব্যথায় প্যারাসিটামল কাজ করতে পারে।
            """
            
        st.info(advice_text)
        st.warning("🔴 **দাবিত্যাগ:** এই পরামর্শ শুধুমাত্র প্রাথমিক ধারণার জন্য। এটি ডাক্তারের বিকল্প নয়। সমস্যা গুরুতর হলে অবশ্যই হাসপাতালে যান।")

# --- 🏥 HOSPITAL & MAP (ENHANCED) ---
elif menu == "🏥 হাসপাতাল ও ম্যাপ":
    st.markdown(f"<div class='section-header'>🏥 {selected_district}-এর হাসপাতালসমূহ</div>", unsafe_allow_html=True)
    
    filtered_hosp = df_hosp[df_hosp['District'] == selected_district]
    
    if not filtered_hosp.empty:
        tab1, tab2 = st.tabs(["📋 তালিকা ও নাম্বার", "🗺️ ম্যাপ ভিউ (Live)"])
        
        with tab1:
            for _, row in filtered_hosp.iterrows():
                st.markdown(f"""
                <div class="hosp-card">
                    <h3 style="margin:0; color:#333;">{row['Name']}</h3>
                    <p style="margin:0; color:#666;">📍 {row['Location']}</p>
                    <h4 style="margin:10px 0 0 0; color:#FF4B4B;">📞 {row['Phone']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
        with tab2:
            if anim_map: st_lottie(anim_map, height=150, key="map_anim_tab")
            # Center map
            avg_lat = filtered_hosp['Lat'].mean()
            avg_lon = filtered_hosp['Lon'].mean()
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)
            
            for _, row in filtered_hosp.iterrows():
                folium.Marker(
                    [row['Lat'], row['Lon']],
                    popup=f"<b>{row['Name']}</b><br>{row['Phone']}",
                    icon=folium.Icon(color="red", icon="plus-sign")
                ).add_to(m)
            folium_static(m)
    else:
        st.warning(f"⚠️ {selected_district}-এর জন্য ডাটা এখনো আপডেট করা হয়নি।")

# --- 👨‍⚕️ DOCTOR FINDER (ENHANCED) ---
elif menu == "👨‍⚕️ ডাক্তার খুঁজুন":
    st.markdown(f"<div class='section-header'>👨‍⚕️ {selected_district}-এর বিশেষজ্ঞ ডাক্তার</div>", unsafe_allow_html=True)
    
    filtered_docs = df_doc[df_doc['District'] == selected_district]
    
    if not filtered_docs.empty:
        specs = ["সকল বিভাগ"] + sorted(filtered_docs['Specialty'].unique().tolist())
        spec_choice = st.selectbox("🔍 বিভাগ অনুযায়ী ফিল্টার করুন:", specs)
        
        if spec_choice != "সকল বিভাগ":
            filtered_docs = filtered_docs[filtered_docs['Specialty'] == spec_choice]
            
        st.divider()
        cols = st.columns(2)
        for i, (index, row) in enumerate(filtered_docs.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="doc-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <h3 style="margin:0; color:#333;">{row['Name']}</h3>
                            <span style="background:#e3f2fd; color:#00C6FF; padding:4px 10px; border-radius:15px; font-size:12px; font-weight:bold;">{row['Specialty']}</span>
                            <p style="margin:10px 0 0 0; color:#666;">🏥 {row['Hospital']}</p>
                        </div>
                        <div style="text-align:right;">
                            <a href="tel:{row['Phone']}" style="text-decoration:none;">
                                <button style="background:linear-gradient(90deg, #28a745, #85e085); color:white; border:none; padding:10px 15px; border-radius:50px; cursor:pointer; font-weight:bold;">📞 কল করুন</button>
                            </a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("এই জেলায় ডাক্তারের তথ্য শীঘ্রই আসছে...")

# --- 🚑 AMBULANCE & BLOOD ---
elif menu == "🚑 অ্যাম্বুলেন্স ও ব্লাড":
    st.markdown("<div class='main-header'>🚨 ইমার্জেন্সি সার্ভিস</div>", unsafe_allow_html=True)
    
    tab_amb, tab_blood = st.tabs(["🚑 অ্যাম্বুলেন্স হটলাইন", "🩸 ব্লাড ব্যাংক (ডোনার)"])
    
    with tab_amb:
        st.markdown(f"### {selected_district}-এর অ্যাম্বুলেন্স")
        c1, c2 = st.columns([1, 2])
        with c1:
            if anim_amb: st_lottie(anim_amb, height=150)
        with c2:
            st.error("🚨 জাতীয় জরুরী সেবা: **999** (ফ্রি)")
            st.info("📞 স্বাস্থ্য বাতায়ন: **16263**")

        filtered_amb = df_amb[(df_amb['District'] == selected_district) | (df_amb['District'] == 'All BD')]
        if not filtered_amb.empty:
            for _, row in filtered_amb.iterrows():
                 st.markdown(f"""
                <div style="background:#fff5f5; padding:15px; border-radius:15px; border:2px solid #ffcccc; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h4 style="margin:0;">🚑 {row['ServiceName']}</h4>
                        <h2 style="margin:5px 0; color:#FF4B4B;">{row['Contact']}</h2>
                    </div>
                     <a href="tel:{row['Contact']}"><button style="background:#FF4B4B; color:white; border:none; padding:10px 20px; border-radius:50px; cursor:pointer;">কল</button></a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("লোকাল ডাটা নেই।")
            
    with tab_blood:
        st.markdown("### 🩸 লাইভ ব্লাড ডোনার খুঁজুন")
        cb1, cb2 = st.columns([1, 1.5])
        with cb1:
             if anim_blood: st_lottie(anim_blood, height=200)
        with cb2:
            bg = st.selectbox("রক্তের গ্রুপ দরকার:", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            area = st.text_input("এলাকা (অপশনাল):")
            if st.button("ডোনার সার্চ করুন 🔍"):
                with st.spinner("খোঁজা হচ্ছে..."):
                    time.sleep(1.5) # Fake loading for effect
                    st.success(f"✅ {bg} গ্রুপের ৩ জন ডোনার পাওয়া গেছে:")
                    st.markdown("""
                    * **ডোনার ১** - 017XXXXXXXX (ভেরিফায়েড)
                    * **ডোনার ২** - 019XXXXXXXX
                    * **ডোনার ৩** - 018XXXXXXXX
                    """)
                    st.caption("*গোপনীয়তার স্বার্থে নাম্বার লুকানো (ডেমো)*")
