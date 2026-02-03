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
            margin-bottom: 15px;
            text-transform: uppercase;
            text-align: center;
        }
        .uni-name {
            font-size: 2rem;
            color: #ffffff;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .college-name {
            font-size: 1.4rem;
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

# ================= 3. ASSETS & ANIMATIONS =================
@st.cache_data
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Loaded Animations
anim_home = load_lottie("https://assets10.lottiefiles.com/packages/lf20_pnycZg.json")
anim_doc = load_lottie("https://assets10.lottiefiles.com/packages/lf20_5njp3vgg.json")
anim_amb = load_lottie("https://assets9.lottiefiles.com/packages/lf20_z4cshyhf.json")
anim_symptom = load_lottie("https://lottie.host/58819173-0740-4a80-9646-7a8311145491/6S5u5Q0D32.json")
# BMI Specific Animations
anim_bmi_fit = load_lottie("https://assets2.lottiefiles.com/packages/lf20_wopcsux6.json") # Fit
anim_bmi_fat = load_lottie("https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json") # Obese

# ================= 4. ADVANCED CSS (DESIGN ENGINE) =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #f4f7f6;
    }

    /* --- ADVANCED SIDEBAR --- */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #ddd;
    }
    /* Styling the Radio Buttons to look like Cards */
    .stRadio > div {
        background-color: transparent;
    }
    .stRadio > div > label {
        background-color: #f8f9fa;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 5px;
        border: 1px solid #eee;
        transition: 0.3s;
        cursor: pointer;
        font-weight: 600;
        color: #333 !important;
        display: block;
    }
    .stRadio > div > label:hover {
        background-color: #e3f2fd;
        transform: translateX(5px);
    }
    /* Active Selection */
    div[role="radiogroup"] > label > div:first-of-type {
        background-color: #0061ff !important;
        border-radius: 50%;
    }

    /* --- GLOBAL CARD STYLES --- */
    .feature-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border-bottom: 4px solid #0061ff;
    }
    .feature-card:hover { transform: translateY(-10px); box-shadow: 0 15px 35px rgba(0,0,0,0.1); }

    /* Doctor Card */
    .doc-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #0061ff;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .doc-card:hover { transform: scale(1.02); }
    
    /* Symptom Card */
    .sym-card {
        background: #fff;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #eee;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    }

    /* BMI Result Box */
    .bmi-box {
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    /* Button */
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
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 5px 15px rgba(0,97,255,0.3); }

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

# ================= 6. ADVANCED SIDEBAR =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063205.png", width=80)
    st.markdown("## HealthPlus BD")
    
    st.divider()
    
    selected_district = st.selectbox(
        "📍 জেলা নির্বাচন করুন:", 
        ALL_DISTRICTS, 
        index=ALL_DISTRICTS.index("Dhaka")
    )
    
    st.write("") # Spacer
    
    # Updated Menu Options
    menu = st.radio("মেনু নেভিগেশন:", 
        ["🏠 হোম পেজ", "🤒 প্রাথমিক চিকিৎসা", "🏥 হাসপাতাল ও ম্যাপ", "👨‍⚕️ ডাক্তার খুঁজুন", "🚑 অ্যাম্বুলেন্স", "📊 BMI ক্যালকুলেটর"]
    )
    st.divider()
    st.info("জরুরী: **999**")

# ================= 7. MAIN INTERFACE =================

# --- HOME ---
if menu == "🏠 হোম পেজ":
    st.markdown("<h1 style='text-align:center; background:linear-gradient(90deg, #0061ff, #00c6ff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:3.5rem;'>HealthPlus Bangladesh</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>জেলা: <b>{selected_district}</b> | স্মার্ট স্বাস্থ্য সেবা</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        st.write("### 👋 স্বাগতম!")
        st.write("এক অ্যাপেই আপনার জেলার সব স্বাস্থ্যসেবা। হাসপাতাল, ডাক্তার, অ্যাম্বুলেন্স এবং প্রাথমিক চিকিৎসা গাইডলাইন।")
        
        # Stats
        h_cnt = len(df_h[df_h['District'] == selected_district])
        d_cnt = len(df_d[df_d['District'] == selected_district])
        
        s1, s2 = st.columns(2)
        with s1: st.markdown(f"<div style='background:#e3f2fd; padding:15px; border-radius:10px; text-align:center;'><h2>{h_cnt}</h2><p>হাসপাতাল</p></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div style='background:#e3f2fd; padding:15px; border-radius:10px; text-align:center;'><h2>{d_cnt}</h2><p>ডাক্তার</p></div>", unsafe_allow_html=True)

    with c2:
        if anim_home: st_lottie(anim_home, height=280)

    st.markdown("---")
    st.subheader("🚀 কুইক এক্সেস")
    co1, co2, co3, co4 = st.columns(4)
    with co1: st.markdown("<div class='feature-card'><h1>🤒</h1><h4>Symptom</h4></div>", unsafe_allow_html=True)
    with co2: st.markdown("<div class='feature-card'><h1>👨‍⚕️</h1><h4>Doctor</h4></div>", unsafe_allow_html=True)
    with co3: st.markdown("<div class='feature-card'><h1>🚑</h1><h4>Ambulance</h4></div>", unsafe_allow_html=True)
    with co4: st.markdown("<div class='feature-card'><h1>📊</h1><h4>BMI Check</h4></div>", unsafe_allow_html=True)

# --- SYMPTOM CHECKER (RESTORED & ANIMATED) ---
elif menu == "🤒 প্রাথমিক চিকিৎসা":
    st.markdown("## 🤒 প্রাথমিক চিকিৎসা ও পরামর্শ")
    
    c1, c2 = st.columns([1, 1.5])
    with c1:
        if anim_symptom: st_lottie(anim_symptom, height=250)
    with c2:
        st.write("### আপনার সমস্যাটি সিলেক্ট করুন:")
        symptom = st.selectbox("লক্ষণসমূহ:", 
            ["বাছাই করুন...", "জ্বর (Fever)", "গ্যাস্ট্রিক/বুক জ্বালা", "মাথা ব্যথা", "শরীরে কাটা/ক্ষত", "পুড়ে যাওয়া (Burn)", "ডায়রিয়া"]
        )
        
        if symptom != "বাছাই করুন...":
            st.divider()
            
            # Logic Dictionary
            advice = {
                "জ্বর (Fever)": {"med": "Napa / Ace (Paracetamol)", "tips": "মাথায় জলপট্টি দিন। প্রচুর পানি ও ফলের রস পান করুন। ১০২° এর বেশি হলে ডাক্তার দেখান।"},
                "গ্যাস্ট্রিক/বুক জ্বালা": {"med": "Seclo 20mg / Pantonix 20mg", "tips": "ভাজাপোড়া ও ঝাল খাবার বর্জন করুন। খাওয়ার পর সাথে সাথে শুয়ে পড়বেন না।"},
                "মাথা ব্যথা": {"med": "Napa Extra / Tufnil", "tips": "অন্ধকার ঘরে বিশ্রাম নিন। মোবাইল/ল্যাপটপ থেকে দূরে থাকুন।"},
                "শরীরে কাটা/ক্ষত": {"med": "Savlon / Povidone Iodine", "tips": "ক্ষতস্থান পরিষ্কার পানি দিয়ে ধুয়ে ফেলুন। রক্তপাত বন্ধ করতে চেপে ধরুন।"},
                "পুড়ে যাওয়া (Burn)": {"med": "Silverzine Cream / Burnol", "tips": "পোড়া স্থানে ১০-১৫ মিনিট ঠান্ডা পানি ঢালুন। বরফ লাগাবেন না।"},
                "ডায়রিয়া": {"med": "Orsaline-N / Zinc", "tips": "প্রতিবার পায়খানার পর স্যালাইন খান। ডাবের পানি ও জাউভাত খেতে পারেন।"}
            }
            
            res = advice.get(symptom)
            
            st.markdown(f"""
            <div class="sym-card">
                <h3 style="color:#0061ff;">✅ পরামর্শ: {symptom}</h3>
                <p><b>💊 প্রাথমিক ঔষধ:</b> <span style="color:#e91e63; font-weight:bold;">{res['med']}</span></p>
                <p><b>💡 করণীয়:</b> {res['tips']}</p>
                <br>
                <small style="color:red;">*সতর্কতা: এটি শুধুমাত্র প্রাথমিক পরামর্শ। সমস্যা গুরুতর হলে দ্রুত হাসপাতালে যান।*</small>
            </div>
            """, unsafe_allow_html=True)

# --- HOSPITAL ---
elif menu == "🏥 হাসপাতাল ও ম্যাপ":
    st.markdown(f"## 🏥 {selected_district}-এর হাসপাতাল")
    filtered_hosp = df_h[df_h['District'] == selected_district]
    
    if not filtered_hosp.empty:
        tab1, tab2 = st.tabs(["📋 তালিকা", "🗺️ ম্যাপ"])
        with tab1:
            for _, row in filtered_hosp.iterrows():
                st.markdown(f"""
                <div class="doc-card" style="border-left: 5px solid #FF4B4B;">
                    <h4 style="margin:0;">{row['Name']}</h4>
                    <p style="color:#666;">📍 {row['Location']}</p>
                    <a href="tel:{row['Phone']}" style="text-decoration:none;"><h5 style="color:#FF4B4B;">📞 {row['Phone']}</h5></a>
                </div>
                """, unsafe_allow_html=True)
        with tab2:
            avg_lat, avg_lon = filtered_hosp['Lat'].mean(), filtered_hosp['Lon'].mean()
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)
            for _, row in filtered_hosp.iterrows():
                folium.Marker([row['Lat'], row['Lon']], popup=row['Name'], icon=folium.Icon(color="red", icon="plus-sign")).add_to(m)
            folium_static(m)
    else:
        st.warning("তথ্য আপডেট করা হচ্ছে...")

# --- DOCTOR (SPECIALIST BADGE ADDED) ---
elif menu == "👨‍⚕️ ডাক্তার খুঁজুন":
    st.markdown(f"## 👨‍⚕️ {selected_district}-এর বিশেষজ্ঞ ডাক্তার")
    
    c1, c2 = st.columns([2, 1])
    with c2: 
        if anim_doc: st_lottie(anim_doc, height=150)
        
    filtered_docs = df_d[df_d['District'] == selected_district]
    
    if not filtered_docs.empty:
        specs = ["সকল বিভাগ"] + sorted(filtered_docs['Specialty'].unique().tolist())
        choice = st.selectbox("বিভাগ ফিল্টার করুন:", specs)
        if choice != "সকল বিভাগ": filtered_docs = filtered_docs[filtered_docs['Specialty'] == choice]
        
        st.write("")
        cols = st.columns(2)
        for i, (index, row) in enumerate(filtered_docs.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="doc-card">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <h4 style="color:#000; font-weight:800;">{row['Name']}</h4>
                            <span style="background:#e3f2fd; color:#0061ff; padding:3px 10px; border-radius:15px; font-size:0.85rem; font-weight:bold; display:inline-block; margin-top:5px;">
                                {row['Specialty']}
                            </span>
                            <p style="font-size:0.9rem; margin-top:5px;">🏥 {row['Hospital']}</p>
                        </div>
                        <div style="align-self:center;">
                             <a href="tel:{row['Phone']}"><button style="background:#28a745; color:white; border:none; padding:8px 15px; border-radius:50px; cursor:pointer;">📞</button></a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("তালিকা শীঘ্রই আসছে...")

# --- AMBULANCE ---
elif menu == "🚑 অ্যাম্বুলেন্স":
    st.markdown("## 🚑 অ্যাম্বুলেন্স সার্ভিস")
    c1, c2 = st.columns([1, 2])
    with c1: 
        if anim_amb: st_lottie(anim_amb, height=150)
    with c2:
        st.error("🚨 জরুরী সেবা: **999**")

    filtered_amb = df_a[(df_a['District'] == selected_district) | (df_a['District'] == 'All BD')]
    if not filtered_amb.empty:
        for _, row in filtered_amb.iterrows():
            st.markdown(f"""
            <div style="background:#fff5f5; padding:15px; border-radius:10px; border:1px solid #ffcccc; margin-bottom:10px; display:flex; justify-content:space-between;">
                <div>
                    <h4 style="margin:0;">🚑 {row['ServiceName']}</h4>
                    <h2 style="margin:5px 0; color:#d32f2f;">{row['Contact']}</h2>
                </div>
                <a href="tel:{row['Contact']}"><button style="background:#d32f2f; color:white; border:none; padding:10px 20px; border-radius:50px; cursor:pointer;">কল করুন</button></a>
            </div>
            """, unsafe_allow_html=True)

# --- BMI CALCULATOR (SUPER ANIMATED) ---
elif menu == "📊 BMI ক্যালকুলেটর":
    st.markdown("## 📊 ফিটনেস চেক (BMI)")
    st.write("আপনার উচ্চতা এবং ওজন দিয়ে জেনে নিন আপনি কতটা ফিট।")
    
    col_in, col_res = st.columns([1, 1])
    
    with col_in:
        weight = st.number_input("ওজন (kg):", 30.0, 150.0, 60.0)
        c1, c2 = st.columns(2)
        with c1: feet = st.number_input("উচ্চতা (ফুট):", 2, 8, 5)
        with c2: inch = st.number_input("ইঞ্চি:", 0, 11, 6)
        
        calc = st.button("ফলাফল দেখুন 🔄")
        
    if calc:
        h_m = ((feet*12)+inch)*0.0254
        bmi = weight/(h_m**2)
        
        status = ""
        color_grad = ""
        anim_to_show = None
        
        if bmi < 18.5:
            status = "⚠️ আপনার ওজন কম (Underweight)"
            color_grad = "linear-gradient(135deg, #f093fb, #f5576c)"
            anim_to_show = anim_bmi_fat # Using warning anim
        elif 18.5 <= bmi < 24.9:
            status = "✅ আপনি সম্পূর্ণ সুস্থ (Healthy)"
            color_grad = "linear-gradient(135deg, #84fab0, #8fd3f4)"
            anim_to_show = anim_bmi_fit
        elif 25 <= bmi < 29.9:
            status = "⚠️ আপনার ওজন বেশি (Overweight)"
            color_grad = "linear-gradient(135deg, #f6d365, #fda085)"
            anim_to_show = anim_bmi_fat
        else:
            status = "🚨 স্থূলতা (Obese) - সতর্ক হন"
            color_grad = "linear-gradient(135deg, #ff9a9e, #fecfef)"
            anim_to_show = anim_bmi_fat

        with col_res:
            if anim_to_show: st_lottie(anim_to_show, height=200)
            st.markdown(f"""
            <div class="bmi-box" style="background: {color_grad};">
                <h3>আপনার BMI স্কোর</h3>
                <h1 style="font-size:3.5rem; margin:0;">{bmi:.1f}</h1>
                <h4 style="margin-top:10px;">{status}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if 18.5 <= bmi < 24.9:
                st.balloons()
