import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from streamlit_lottie import st_lottie
import requests

# ================= 1. PAGE CONFIGURATION (MUST BE AT TOP) =================
st.set_page_config(
    page_title="HealthConnect BD",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= 2. ASSETS & LOADER FUNCTIONS =================
@st.cache_data
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Load Premium Animations
anim_hero = load_lottie("https://assets5.lottiefiles.com/packages/lf20_5njp3vgg.json")
anim_map = load_lottie("https://assets3.lottiefiles.com/packages/lf20_s5id889b.json")
anim_amb = load_lottie("https://assets9.lottiefiles.com/packages/lf20_z4cshyhf.json")
anim_blood = load_lottie("https://assets6.lottiefiles.com/packages/lf20_9xR7SM.json")

# ================= 3. ADVANCED CSS (DESIGN SYSTEM) =================
st.markdown("""
<style>
    /* Global Font & Theme */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        background-color: #f4f6f9;
    }
    
    /* Hero Section Gradient Text */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(to right, #FF4B4B, #FF9068);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 2px 2px 20px rgba(0,0,0,0.1);
    }
    
    /* Modern Card Effects */
    .feature-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        text-align: center;
        transition: all 0.3s ease;
        border-bottom: 4px solid #FF4B4B;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(255, 75, 75, 0.2);
    }
    
    /* Info Cards */
    .hospital-box {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #FF4B4B;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    .doctor-box {
        background: white;
        padding: 15px;
        border-radius: 15px;
        border-top: 5px solid #4F8BF9;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }

    .amb-box {
        background: #fff5f5;
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #ffcccc;
        text-align: center;
        margin-bottom: 15px;
    }

    /* Custom Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #4F8BF9, #00C6FF);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 12px 25px;
        font-weight: 700;
        width: 100%;
        transition: 0.3s;
        box-shadow: 0 5px 15px rgba(0, 198, 255, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(0, 198, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ================= 4. ROBUST DATA LOADING =================
@st.cache_data
def load_data():
    # Fallback Mechanism: If CSV missing, create empty structure
    try: df_hosp = pd.read_csv("hospitals_64.csv")
    except: df_hosp = pd.DataFrame(columns=["District", "Name", "Location", "Phone", "Lat", "Lon"])
    
    try: df_doc = pd.read_csv("doctors_64.csv")
    except: df_doc = pd.DataFrame(columns=["District", "Name", "Specialty", "Hospital", "Phone"])
    
    try: df_amb = pd.read_csv("ambulances_64.csv")
    except: df_amb = pd.DataFrame(columns=["District", "ServiceName", "Contact"])
    
    return df_hosp, df_doc, df_amb

df_hosp, df_doc, df_amb = load_data()

# ================= 5. SIDEBAR NAVIGATION =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063205.png", width=100)
    st.title("HealthConnect")
    st.write("বাংলাদেশের ৬৪ জেলার ইমার্জেন্সি সেবা")
    
    # Smart District Filter
    if not df_hosp.empty:
        all_districts = sorted(df_hosp['District'].unique().tolist())
        selected_district = st.selectbox("📍 আপনার জেলা নির্বাচন করুন:", all_districts)
    else:
        st.warning("⚠️ ডাটাবেস ফাইল পাওয়া যায়নি")
        selected_district = "Dhaka"
        
    menu = st.radio("মেনু:", ["🏠 হোম", "🏥 হাসপাতাল", "👨‍⚕️ ডাক্তার", "🚑 অ্যাম্বুলেন্স", "🩸 ব্লাড ব্যাংক"])
    
    st.markdown("---")
    st.info("জরুরী কল: **999**")

# ================= 6. MAIN APPLICATION =================

# --- 🏠 HOME PAGE ---
if menu == "🏠 হোম":
    st.markdown("<div class='hero-title'>HealthConnect BD</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#666;'>আপনার জেলা: <b>{selected_district}</b> | আপনার বিশ্বস্ত স্বাস্থ্য সাথী</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if anim_hero: st_lottie(anim_hero, height=250, key="hero_anim")

    st.markdown("### 🚀 আপনি কী সেবা খুঁজছেন?")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="feature-card"><h1>🏥</h1><h4>হাসপাতাল</h4><p>লোকেশন ও ম্যাপ</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="feature-card"><h1>👨‍⚕️</h1><h4>ডাক্তার</h4><p>চেম্বার ও সিরিয়াল</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="feature-card"><h1>🚑</h1><h4>অ্যাম্বুলেন্স</h4><p>জরুরী সেবা</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="feature-card"><h1>🩸</h1><h4>ব্লাড ব্যাংক</h4><p>ডোনার খুঁজুন</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 বাম পাশের মেনু থেকে বিস্তারিত অপশনে যান।")

# --- 🏥 HOSPITAL & MAP ---
elif menu == "🏥 হাসপাতাল":
    st.markdown(f"## 🏥 {selected_district}-এর হাসপাতালসমূহ")
    
    filtered_hosp = df_hosp[df_hosp['District'] == selected_district]
    
    if not filtered_hosp.empty:
        tab1, tab2 = st.tabs(["📋 তালিকা দেখুন", "🗺️ ম্যাপে দেখুন"])
        
        with tab1:
            for _, row in filtered_hosp.iterrows():
                st.markdown(f"""
                <div class="hospital-box">
                    <h3 style="margin:0; color:#333;">{row['Name']}</h3>
                    <p style="margin:0; color:#666;">📍 {row['Location']}</p>
                    <a href="tel:{row['Phone']}" style="text-decoration:none;">
                        <h4 style="margin:5px 0 0 0; color:#FF4B4B;">📞 {row['Phone']}</h4>
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
        with tab2:
            st.write("### 🗺️ লাইভ লোকেশন")
            # Calculate Average Lat/Lon for centering map
            avg_lat = filtered_hosp['Lat'].mean()
            avg_lon = filtered_hosp['Lon'].mean()
            
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=13)
            
            for _, row in filtered_hosp.iterrows():
                folium.Marker(
                    [row['Lat'], row['Lon']],
                    popup=f"<b>{row['Name']}</b><br>{row['Phone']}",
                    icon=folium.Icon(color="red", icon="plus-sign")
                ).add_to(m)
            
            folium_static(m)
    else:
        st.warning(f"⚠️ {selected_district}-এর জন্য এখনো ডাটা আপলোড করা হয়নি।")
        if anim_map: st_lottie(anim_map, height=200)

# --- 👨‍⚕️ DOCTOR ---
elif menu == "👨‍⚕️ ডাক্তার":
    st.markdown(f"## 👨‍⚕️ {selected_district}-এর ডাক্তারগণ")
    
    filtered_docs = df_doc[df_doc['District'] == selected_district]
    
    if not filtered_docs.empty:
        # Smart Search
        specs = ["সকল"] + sorted(filtered_docs['Specialty'].unique().tolist())
        choice = st.selectbox("বিভাগ নির্বাচন করুন:", specs)
        
        if choice != "সকল":
            filtered_docs = filtered_docs[filtered_docs['Specialty'] == choice]
            
        cols = st.columns(2)
        for i, (index, row) in enumerate(filtered_docs.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="doctor-box">
                    <h4 style="margin:0;">{row['Name']}</h4>
                    <span style="background:#e3f2fd; color:#4F8BF9; padding:2px 8px; border-radius:10px; font-size:12px;">{row['Specialty']}</span>
                    <p style="margin:5px 0 0 0; font-size:13px;">🏥 {row['Hospital']}</p>
                    <a href="tel:{row['Phone']}" style="text-decoration:none;">
                        <button style="background:#28a745; color:white; border:none; padding:8px 10px; border-radius:5px; cursor:pointer; width:100%; margin-top:10px;">📞 সিরিয়াল দিন</button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("ডাক্তারের তথ্য শীঘ্রই আপডেট করা হবে।")

# --- 🚑 AMBULANCE ---
elif menu == "🚑 অ্যাম্বুলেন্স":
    st.markdown(f"## 🚑 অ্যাম্বুলেন্স সার্ভিস ({selected_district})")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        if anim_amb: st_lottie(anim_amb, height=150)
    with c2:
        st.error("🚨 জরুরী প্রয়োজনে **৯৯৯** এ কল করুন।")
        
    filtered_amb = df_amb[(df_amb['District'] == selected_district) | (df_amb['District'] == 'All BD')]
    
    if not filtered_amb.empty:
        for _, row in filtered_amb.iterrows():
            st.markdown(f"""
            <div class="amb-box">
                <h3 style="margin:0;">🚑 {row['ServiceName']}</h3>
                <h2 style="color:#FF4B4B; margin:5px 0;">{row['Contact']}</h2>
                <a href="tel:{row['Contact']}"><button style="background:#FF4B4B; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">সরাসরি কল করুন</button></a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("লোকাল অ্যাম্বুলেন্স ডাটা নেই।")

# --- 🩸 BLOOD BANK ---
elif menu == "🩸 ব্লাড ব্যাংক":
    st.markdown("## 🩸 ব্লাড ডোনার খুঁজুন")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if anim_blood: st_lottie(anim_blood, height=250)
    with col2:
        st.write("### ফিল্টার")
        bg = st.selectbox("রক্তের গ্রুপ:", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        area = st.text_input("এলাকা (যেমন: ধানমন্ডি):")
        
        if st.button("ডোনার খুঁজুন 🔍"):
            st.success(f"✅ {bg} গ্রুপের ডোনার পাওয়া গেছে:")
            st.markdown("""
            1. **রাফি আহমেদ** - 017XXXXXXXX
            2. **কামাল হোসেন** - 019XXXXXXXX
            3. **সুমন খান** - 018XXXXXXXX
            """)
            st.caption("*গোপনীয়তার স্বার্থে নাম্বার লুকানো (ডেমো)*")
