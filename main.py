import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from streamlit_lottie import st_lottie
import requests

# ================= 1. CONFIGURATION =================
st.set_page_config(
    page_title="HealthConnect BD | Emergency Hub",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. ANIMATION & STYLING =================
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Load Animations
anim_map = load_lottie("https://assets3.lottiefiles.com/packages/lf20_s5id889b.json")
anim_doc = load_lottie("https://assets10.lottiefiles.com/packages/lf20_5njp3vgg.json")
anim_amb = load_lottie("https://assets9.lottiefiles.com/packages/lf20_z4cshyhf.json")

# Advanced CSS (Glassmorphism & Gradients)
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Header Gradient */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #ff4b4b, #ff9068);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Stats Box */
    .stat-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        border-bottom: 5px solid #ff4b4b;
    }

    /* Hospital Card */
    .hospital-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #ff4b4b;
        box-shadow: 5px 5px 15px #d1d1d1, -5px -5px 15px #ffffff;
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .hospital-card:hover {
        transform: translateY(-5px);
    }

    /* Doctor Card */
    .doc-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border-top: 4px solid #4F8BF9;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }

    /* Ambulance Card */
    .amb-card {
        background: #fff5f5;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #ffcccc;
        text-align: center;
        color: #333;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #FF4B4B, #FF9068);
        color: white;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ================= 3. DATA LOADING =================
@st.cache_data
def load_data():
    try:
        df_hosp = pd.read_csv("hospitals_64.csv")
    except: df_hosp = pd.DataFrame(columns=["District", "Name", "Location", "Phone", "Lat", "Lon"])
    
    try:
        df_doc = pd.read_csv("doctors_64.csv")
    except: df_doc = pd.DataFrame(columns=["District", "Name", "Specialty", "Hospital", "Phone"])
    
    try:
        df_amb = pd.read_csv("ambulances_64.csv")
    except: df_amb = pd.DataFrame(columns=["District", "ServiceName", "Contact"])
    
    return df_hosp, df_doc, df_amb

df_hosp, df_doc, df_amb = load_data()

# ================= 4. SIDEBAR NAVIGATION =================
with st.sidebar:
    if anim_doc: st_lottie(anim_doc, height=150, key="anim_sidebar")
    
    st.markdown("## 🏥 HealthConnect")
    st.write("বাংলাদেশের সকল জেলার স্বাস্থ্য সেবা।")
    
    # --- SMART DISTRICT SELECTOR ---
    all_districts = sorted(df_hosp['District'].unique().tolist()) if not df_hosp.empty else ["Dhaka"]
    selected_district = st.selectbox("📍 আপনার জেলা নির্বাচন করুন:", all_districts)

    menu = st.radio("মেনু:", 
        ["🏠 ড্যাশবোর্ড", "🏥 হাসপাতাল ও ম্যাপ", "👨‍⚕️ ডাক্তার খুঁজুন", "🚑 অ্যাম্বুলেন্স", "🩸 ব্লাড ব্যাংক"]
    )
    
    st.markdown("---")
    st.info("জরুরী প্রয়োজনে: **999**")

# ================= 5. MAIN FEATURES =================

# --- 🏠 DASHBOARD ---
if menu == "🏠 ড্যাশবোর্ড":
    st.markdown("<div class='main-title'>HealthConnect Bangladesh</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center; color:#555;'>বর্তমান জেলা: <b>{selected_district}</b></h3>", unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    dist_hosp_count = len(df_hosp[df_hosp['District'] == selected_district])
    dist_doc_count = len(df_doc[df_doc['District'] == selected_district])
    
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <h1 style="color:#ff4b4b; margin:0;">{dist_hosp_count}</h1>
            <p>হাসপাতাল</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <h1 style="color:#4F8BF9; margin:0;">{dist_doc_count}</h1>
            <p>ডাক্তার</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-box">
            <h1 style="color:#28a745; margin:0;">24/7</h1>
            <p>সার্ভিস</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### 👋 আমাদের সেবাসমূহ:")
        st.write("""
        * ✅ ৬৪ জেলার হাসপাতালের এক্সাক্ট লোকেশন
        * ✅ বিশেষজ্ঞ ডাক্তারদের চেম্বার ও ফোন নাম্বার
        * ✅ লোকাল এবং সরকারি অ্যাম্বুলেন্স সার্ভিস
        * ✅ লাইভ ব্লাড ডোনার কানেকশন
        """)
    with c2:
        if anim_map: st_lottie(anim_map, height=300, key="anim_dash")

# --- 🏥 HOSPITAL & MAP ---
elif menu == "🏥 হাসপাতাল ও ম্যাপ":
    st.markdown(f"## 🏥 {selected_district}-এর হাসপাতালসমূহ")
    
    filtered_hosp = df_hosp[df_hosp['District'] == selected_district]
    
    if not filtered_hosp.empty:
        col1, col2 = st.columns([1.5, 2.5])
        
        with col1:
            st.write("### 📋 তালিকা:")
            for _, row in filtered_hosp.iterrows():
                st.markdown(f"""
                <div class="hospital-card">
                    <h4 style="margin:0; color:#333;">{row['Name']}</h4>
                    <small style="color:#666;">📍 {row['Location']}</small>
                    <h5 style="margin:5px 0 0 0; color:#FF4B4B;">📞 {row['Phone']}</h5>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.write("### 🗺️ ম্যাপ ভিউ (Live):")
            # Create Map
            avg_lat = filtered_hosp['Lat'].mean()
            avg_lon = filtered_hosp['Lon'].mean()
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=13)
            
            for _, row in filtered_hosp.iterrows():
                folium.Marker(
                    [row['Lat'], row['Lon']],
                    popup=f"<b>{row['Name']}</b><br>{row['Phone']}",
                    tooltip=row['Name'],
                    icon=folium.Icon(color="red", icon="plus-sign")
                ).add_to(m)
            
            folium_static(m)
    else:
        st.warning(f"⚠️ {selected_district}-এর জন্য ডাটা এখনো আপডেট করা হয়নি।")

# --- 👨‍⚕️ DOCTOR FINDER ---
elif menu == "👨‍⚕️ ডাক্তার খুঁজুন":
    st.markdown(f"## 👨‍⚕️ বিশেষজ্ঞ ডাক্তার ({selected_district})")
    
    filtered_docs = df_doc[df_doc['District'] == selected_district]
    
    if not filtered_docs.empty:
        # Smart Filter
        specs = ["সকল"] + sorted(filtered_docs['Specialty'].unique().tolist())
        selected_spec = st.selectbox("কোন বিশেষজ্ঞ ডাক্তার খুঁজছেন?", specs)
        
        if selected_spec != "সকল":
            filtered_docs = filtered_docs[filtered_docs['Specialty'] == selected_spec]
        
        # Display Grid Layout
        cols = st.columns(2)
        for i, (index, row) in enumerate(filtered_docs.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="doc-card">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <h4 style="margin:0;">{row['Name']}</h4>
                            <span style="background:#e3f2fd; color:#4F8BF9; padding:2px 6px; border-radius:4px; font-size:12px;">{row['Specialty']}</span>
                            <p style="margin:5px 0 0 0; font-size:13px; color:#555;">🏥 {row['Hospital']}</p>
                        </div>
                        <div style="align-self:center;">
                            <a href="tel:{row['Phone']}" style="text-decoration:none; font-size:20px;">📞</a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("এই জেলায় ডাক্তারের তথ্য শীঘ্রই আসছে...")

# --- 🚑 AMBULANCE ---
elif menu == "🚑 অ্যাম্বুলেন্স":
    st.markdown(f"## 🚑 অ্যাম্বুলেন্স সার্ভিস ({selected_district})")
    
    col_anim, col_info = st.columns([1, 2])
    with col_anim:
        if anim_amb: st_lottie(anim_amb, height=150)
    with col_info:
        st.error("🚨 জাতীয় জরুরী সেবা: **999** (টোল ফ্রি)")
        
    filtered_amb = df_amb[(df_amb['District'] == selected_district) | (df_amb['District'] == 'All BD')]
    
    if not filtered_amb.empty:
        for _, row in filtered_amb.iterrows():
            st.markdown(f"""
            <div class="amb-card">
                <h3 style="margin:0;">🚑 {row['ServiceName']}</h3>
                <h1 style="color:#FF4B4B; margin:5px 0;">{row['Contact']}</h1>
                <a href="tel:{row['Contact']}"><button>সরাসরি কল করুন</button></a>
            </div>
            <br>
            """, unsafe_allow_html=True)
    else:
        st.warning("লোকাল অ্যাম্বুলেন্স ডাটা পাওয়া যায়নি। ৯৯৯ এ কল করুন।")

# --- 🩸 BLOOD BANK ---
elif menu == "🩸 ব্লাড ব্যাংক":
    st.markdown("## 🩸 ব্লাড ডোনার খুঁজুন")
    
    c1, c2 = st.columns(2)
    with c1:
        bg = st.selectbox("রক্তের গ্রুপ:", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    with c2:
        area = st.text_input("এলাকা (ঐচ্ছিক):", placeholder="যেমন: ধানমন্ডি")
        
    if st.button("ডোনার খুঁজুন 🔍"):
        st.success(f"✅ {selected_district}-এ {bg} গ্রুপের ডোনার পাওয়া গেছে:")
        st.markdown("""
        * **আব্দুর রহমান** - 017XXXXXXXX
        * **কামাল হোসেন** - 019XXXXXXXX
        * **হাসান মাহমুদ** - 018XXXXXXXX
        """)
        st.caption("গোপনীয়তার স্বার্থে নাম্বার হাইড করা হয়েছে (ডেমো)")
