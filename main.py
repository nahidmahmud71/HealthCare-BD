import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# ================= 1. PAGE SETUP =================
st.set_page_config(
    page_title="HealthConnect BD",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. ADVANCED CSS =================
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        font-weight: 800;
        text-shadow: 2px 2px 4px #cccccc;
    }
    .sub-title {
        text-align: center;
        color: gray;
        margin-bottom: 20px;
    }
    .card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        border-left: 5px solid #FF4B4B;
    }
    .amb-card {
        background-color: #ffeaea;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #ffaaaa;
    }
</style>
""", unsafe_allow_html=True)

# ================= 3. DATA LOADING FUNCTION =================
@st.cache_data
def load_data():
    try:
        df_hosp = pd.read_csv("hospitals_64.csv")
        df_doc = pd.read_csv("doctors_64.csv")
        df_amb = pd.read_csv("ambulances_64.csv")
        return df_hosp, df_doc, df_amb
    except FileNotFoundError:
        st.error("❌ ডাটাবেস ফাইল মিসিং! দয়া করে CSV ফাইলগুলো ঠিকমতো তৈরি করুন।")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_hosp, df_doc, df_amb = load_data()

# ================= 4. SIDEBAR & NAVIGATION =================
with st.sidebar:
    st.title("🏥 HealthConnect BD")
    st.write("৬৪ জেলার স্বাস্থ্য সেবা, এক ক্লিকে।")
    
    # Global District Filter (Smart Feature)
    # Get all unique districts from database
    if not df_hosp.empty:
        all_districts = sorted(df_hosp['District'].unique().tolist())
        selected_district = st.selectbox("📍 আপনার জেলা নির্বাচন করুন:", all_districts)
    else:
        selected_district = "Dhaka"

    menu = st.radio("সেবা নির্বাচন করুন:", 
        ["🏥 হাসপাতাল ও ম্যাপ", "👨‍⚕️ ডাক্তার খুঁজুন", "🚑 অ্যাম্বুলেন্স", "🩸 ব্লাড ব্যাংক"],
    )
    st.divider()
    st.info("জরুরী প্রয়োজনে: **999**")

# ================= 5. MAIN FEATURES =================

# HEADER
st.markdown(f"<div class='main-title'>HealthConnect Bangladesh</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>বর্তমানে নির্বাচিত জেলা: <b>{selected_district}</b></div>", unsafe_allow_html=True)

# --- 🏥 HOSPITAL & MAP ---
if menu == "🏥 হাসপাতাল ও ম্যাপ":
    col1, col2 = st.columns([1.5, 2.5])
    
    # Filter Data based on District
    filtered_hosp = df_hosp[df_hosp['District'] == selected_district]
    
    with col1:
        st.subheader(f"🏥 {selected_district}-এর হাসপাতালসমূহ")
        if not filtered_hosp.empty:
            for _, row in filtered_hosp.iterrows():
                st.markdown(f"""
                <div class="card">
                    <h4 style="margin:0;">{row['Name']}</h4>
                    <small>📍 {row['Location']}</small><br>
                    <b style="color:blue;">📞 {row['Phone']}</b>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("এই জেলার হাসপাতালের তথ্য শীঘ্রই আসছে...")

    with col2:
        st.subheader("🗺️ ম্যাপে অবস্থান")
        
        if not filtered_hosp.empty:
            # Center map to the average location of hospitals in that district
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
            st.info("ম্যাপ লোড করার জন্য পর্যাপ্ত ডাটা নেই।")

# --- 👨‍⚕️ DOCTOR FINDER ---
elif menu == "👨‍⚕️ ডাক্তার খুঁজুন":
    st.subheader(f"👨‍⚕️ {selected_district}-এর বিশেষজ্ঞ ডাক্তারগণ")
    
    filtered_docs = df_doc[df_doc['District'] == selected_district]
    
    # Filter by Specialty
    if not filtered_docs.empty:
        specialties = ["All"] + sorted(filtered_docs['Specialty'].unique().tolist())
        selected_spec = st.selectbox("বিশেষজ্ঞতা বাছুন:", specialties)
        
        if selected_spec != "All":
            filtered_docs = filtered_docs[filtered_docs['Specialty'] == selected_spec]
        
        for _, row in filtered_docs.iterrows():
            st.markdown(f"""
            <div class="card" style="border-left: 5px solid #4F8BF9;">
                <h3 style="margin:0;">{row['Name']}</h3>
                <span style="background:#eee; padding:2px 8px; border-radius:5px;">{row['Specialty']}</span>
                <p style="margin:5px 0;">🏥 {row['Hospital']}</p>
                <a href="tel:{row['Phone']}" style="text-decoration:none;">
                    <button style="background-color:#28a745; color:white; border:none; padding:5px 15px; border-radius:5px; cursor:pointer;">📞 সিরিয়াল দিন</button>
                </a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning(f"{selected_district}-এ কোনো ডাক্তারের তথ্য পাওয়া যায়নি।")

# --- 🚑 AMBULANCE ---
elif menu == "🚑 অ্যাম্বুলেন্স":
    st.subheader(f"🚑 {selected_district}-এর অ্যাম্বুলেন্স সার্ভিস")
    
    filtered_amb = df_amb[(df_amb['District'] == selected_district) | (df_amb['District'] == 'All BD')]
    
    if not filtered_amb.empty:
        cols = st.columns(2)
        for i, (index, row) in enumerate(filtered_amb.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="amb-card">
                    <h4>🚑 {row['ServiceName']}</h4>
                    <h2 style="color:red;">📞 {row['Contact']}</h2>
                    <a href="tel:{row['Contact']}">Click to Call</a>
                </div>
                <br>
                """, unsafe_allow_html=True)
    else:
        st.warning("তথ্য পাওয়া যায়নি। ৯৯৯ এ কল করুন।")

# --- 🩸 BLOOD BANK ---
elif menu == "🩸 ব্লাড ব্যাংক":
    st.subheader("🩸 লাইভ ব্লাড ডোনার খুঁজুন")
    
    c1, c2 = st.columns(2)
    with c1:
        bg = st.selectbox("রক্তের গ্রুপ:", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    with c2:
        area = st.text_input(f"এলাকা ({selected_district}-এর ভেতর):")
        
    if st.button("ডোনার খুঁজুন 🔍"):
        st.success(f"{selected_district}-এ {bg} গ্রুপের ৩ জন ডোনার পাওয়া গেছে (Demo Data):")
        st.markdown("""
        1. **রাফি আহমেদ** - 017XXXXXXXX
        2. **সাকিব আল হাসান** - 019XXXXXXXX
        3. **শফিক করিম** - 018XXXXXXXX
        """)