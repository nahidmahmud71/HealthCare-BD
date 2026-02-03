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
# এটি অ্যাপ খোলার সাথে সাথে একবারই দেখাবে
if 'splash_shown' not in st.session_state:
    st.session_state.splash_shown = False

if not st.session_state.splash_shown:
    # Full Screen Intro Design
    st.markdown("""
    <style>
        .stApp { background-color: #000000; color: white; }
        .intro-text {
            text-align: center;
            margin-top: 15%;
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(to right, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeIn 2s ease-in-out;
        }
        .uni-text {
            text-align: center;
            font-size: 1.5rem;
            color: #ccc;
            margin-top: 10px;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
    <div class="intro-text">Developed by MD NAHID MAHMUD</div>
    <div class="uni-text">Southeast University | CSE Batch 67</div>
    """, unsafe_allow_html=True)
    
    # Wait for 3 seconds then reload to main app
    time.sleep(3) 
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

# IMPORT MAIN LIBRARIES LATE FOR SPEED
import folium
from streamlit_folium import folium_static

# Advanced CSS
st.markdown("""
<style>
    /* Reset & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #f4f7f6;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 2px solid #e0e0e0;
    }

    /* Main Header Gradient */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #0061ff, #60efff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* Hospital Cards */
    .hospital-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #FF4B4B;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .hospital-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(255, 75, 75, 0.2);
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #0061ff, #00c6ff);
        color: white;
        border-radius: 50px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# ================= 4. DATA LOADING =================
# ৬৪ জেলার নাম (সাজানো)
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
    st.caption("Developed by **MD NAHID MAHMUD**")
    
    st.divider()
    
    # District Selector
    selected_district = st.selectbox(
        "📍 জেলা নির্বাচন করুন:", 
        ALL_DISTRICTS, 
        index=ALL_DISTRICTS.index("Dhaka")
    )
    
    st.divider()
    menu = st.radio("মেনু:", 
        ["🏠 হোম (Home)", "🏥 হাসপাতাল ও ম্যাপ", "👨‍⚕️ ডাক্তার", "🚑 অ্যাম্বুলেন্স", "📊 BMI ক্যালকুলেটর"]
    )
    st.markdown("---")
    st.error("জরুরী হটলাইন: **999**")

# ================= 6. MAIN CONTENT =================

if menu == "🏠 হোম (Home)":
    # Hero Title
    st.markdown("<div class='hero-title'>HealthPlus Bangladesh</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>আপনার জেলা: <b>{selected_district}</b></p>", unsafe_allow_html=True)
    
    # Welcome Animation
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(f"""
        ### 👋 স্বাগতম!
        **MD NAHID MAHMUD** এর ডেভেলপ করা এই অ্যাপে আপনাকে স্বাগতম।
        আমরা ৬৪ জেলার মানুষের স্বাস্থ্যসেবা নিশ্চিত করতে এটি তৈরি করেছি।
        
        **একনজরে {selected_district}:**
        * 🏥 হাসপাতাল: **{len(df_h[df_h['District']==selected_district])}** টি
        * 👨‍⚕️ ডাক্তার: **{len(df_d[df_d['District']==selected_district])}** জন
        """)
        
        st.info("👈 বাম পাশের মেনু থেকে সেবা নির্বাচন করুন।")
        
    with c2:
        if anim_welcome: st_lottie(anim_welcome, height=300)

elif menu == "🏥 হাসপাতাল ও ম্যাপ":
    st.markdown(f"## 🏥 {selected_district}-এর হাসপাতাল")
    
    filtered_hosp = df_h[df_h['District'] == selected_district]
    
    if not filtered_hosp.empty:
        tab1, tab2 = st.tabs(["📋 তালিকা (List)", "🗺️ লাইভ ম্যাপ (Map)"])
        
        with tab1:
            for _, row in filtered_hosp.iterrows():
                st.markdown(f"""
                <div class="hospital-card">
                    <h3 style="margin:0; color:#333;">{row['Name']}</h3>
                    <p style="margin:0; color:#666;">📍 {row['Location']}</p>
                    <a href="tel:{row['Phone']}" style="text-decoration:none;">
                        <h4 style="margin:10px 0 0 0; color:#FF4B4B;">📞 {row['Phone']}</h4>
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
        with tab2:
            st.write("### 🗺️ লোকেশন দেখুন")
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
        st.warning(f"⚠️ {selected_district}-এর ডাটা শীঘ্রই আপডেট করা হবে।")
        if anim_map: st_lottie(anim_map, height=200)

elif menu == "👨‍⚕️ ডাক্তার":
    st.markdown(f"## 👨‍⚕️ {selected_district}-এর ডাক্তার")
    filtered_docs = df_d[df_d['District'] == selected_district]
    
    if not filtered_docs.empty:
        for _, row in filtered_docs.iterrows():
            st.markdown(f"""
            <div style="background:white; padding:15px; border-radius:10px; border-left:5px solid #0061ff; margin-bottom:10px;">
                <h4 style="margin:0;">{row['Name']}</h4>
                <p style="margin:0;">{row['Specialty']}</p>
                <p style="color:#666; font-size:12px;">🏥 {row['Hospital']}</p>
                <h5 style="color:#0061ff;">📞 {row['Phone']}</h5>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ডাক্তারের তালিকা আপডেট করা হচ্ছে...")

elif menu == "🚑 অ্যাম্বুলেন্স":
    st.markdown(f"## 🚑 অ্যাম্বুলেন্স সার্ভিস")
    filtered_amb = df_a[(df_a['District'] == selected_district) | (df_a['District'] == 'All BD')]
    
    if not filtered_amb.empty:
        for _, row in filtered_amb.iterrows():
            st.error(f"🚑 {row['ServiceName']}: {row['Contact']}")
    else:
        st.error("জাতীয় জরুরী সেবা: **999**")

elif menu == "📊 BMI ক্যালকুলেটর":
    st.markdown("## 📊 BMI চেক করুন")
    w = st.number_input("ওজন (kg):", 30, 150, 60)
    h_ft = st.number_input("উচ্চতা (ft):", 2, 8, 5)
    h_in = st.number_input("উচ্চতা (inch):", 0, 11, 6)
    
    if st.button("হিসাব করুন"):
        h_m = ((h_ft*12)+h_in)*0.0254
        bmi = w/(h_m**2)
        st.success(f"আপনার BMI: {bmi:.2f}")
