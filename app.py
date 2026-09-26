import streamlit as st
import pandas as pd

# --- 1. REGIONAL LANGUAGE DICTIONARY (Localization Packs) ---
LANG_DB = {
    "English": {
        "title": "🧱 Our Agri Portal 🧑‍🌾",
        "subtitle": "Verify identity to unlock the village grid",
        "name_lbl": "Farmer Name (e.g. raksh):",
        "aadhaar_lbl": "12-Digit Aadhaar Number:",
        "btn_login": "Assemble & Enter 🧩",
        "err_len": "⚠️ Aadhaar must be exactly 12 digits long!",
        "err_match": "🚨 Authentication Failed! Details do not match rural records.",
        "status_title": "🏗️ Warehouse Grid Status",
        "logout": "🚪 Leave Grid",
        "help": "📞 Help Desk: 1800-425-XXXX (24/7 Rural Support)"
    },
     "தமிழ்": {
        "title": "🧱 நமது அக்ரி போர்டல் 🧑‍🌾",
        "subtitle": "கிராமப்புற கணினியை அணுக உங்கள் அடையாளத்தை சரிபார்க்கவும்",
        "name_lbl": "விவசாயி பெயர்:",
        "aadhaar_lbl": "12-இலக்க ஆதார் எண்:",
        "btn_login": "இணைந்து உள்ளே நுழைக 🧩",
        "err_len": "⚠️ ஆதார் எண் சரியாக 12 இலக்கங்களாக இருக்க வேண்டும்!",
        "err_match": "🚨 அங்கீகாரம் தோல்வி! விவரங்கள் பதிவுகளுடன் பொருந்தவில்லை.",
        "status_title": "🏗️ கிடங்கு இட விபரம்",
        "logout": "🚪 வெளியேறு",
        "help": "📞 உதவி மையம்: 1800-425-XXXX (24/7 கிராமப்புற உதவி)"
    },
    "हिन्दी": {
        "title": "🧱 हमारा एग्री पोर्टल 🧑‍🌾",
        "subtitle": "ग्रिड में प्रवेश करने के लिए अपनी पहचान सत्यापित करें",
        "name_lbl": "किसान का नाम:",
        "aadhaar_lbl": "12-अंकीय आधार संख्या:",
        "btn_login": "जुड़ें और प्रवेश करें 🧩",
        "err_len": "⚠️ आधार संख्या बिल्कुल 12 अंकों की होनी चाहिए!",
        "err_match": "🚨 सत्यापन विफल! विवरण रिकॉर्ड से मेल नहीं खाता।",
        "status_title": "🏗️ गोदाम ग्रिड स्थिति",
        "logout": "🚪 ग्रिड से बाहर निकलें",
        "help": "📞 सहायता डेस्क: 1800-425-XXXX (24/7 ग्रामीण सहायता)"
    }
}

# --- 2. CORE SYSTEM STATE BANK ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "block_a_used" not in st.session_state:
    st.session_state.block_a_used = 42  
if "block_b_used" not in st.session_state:
    st.session_state.block_b_used = 10  
if "has_booked" not in st.session_state:
    st.session_state.has_booked = False  
if "tracker_stage" not in st.session_state:
    st.session_state.tracker_stage = 0

GOVT_DATABASE = {
    "raksh": "123456789012",
    "ramesh": "987654321098"
}

BLOCK_A_MAX = 50
BLOCK_B_MAX = 30

# --- 3. INJECT NATIVE LEGO CUSTOM STYLING (The Green Farmland Theme) ---
st.markdown("""
    <style>
    /* Style the main viewport container to mimic a bright green Lego Baseplate */
    .stApp {
        background-color: #2e8b57 !important;
        background-image: radial-gradient(#3cb371 20%, transparent 20%) !important;
        background-size: 30px 30px !important;
    }
    /* Format the data content input boxes to look like stacked plastic bricks */
    div.stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 4px solid #000000 !important;
        border-radius: 0px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. TOP CORNER CONTENT SECTION MATRIX ---
header_col, settings_col = st.columns([3, 1])

with settings_col:
    # Isolated Settings Container Box pinned exactly to the top right corner
    with st.expander("⚙️ Settings", expanded=False):
        chosen_lang = st.selectbox("🌐 Lang", ["English", "தமிழ்", "हिन्दी"], index=["English", "தமிழ்", "हिन्दी"].index(st.session_state.lang))
        st.session_state.lang = chosen_lang
        
        # Display the support line inside settings block layout
        st.caption(LANG_DB[st.session_state.lang]["help"])

TXT = LANG_DB[st.session_state.lang]

# --- 5. SECURE IDENTITY ACCESS GATE ---
if not st.session_state.logged_in:
    with header_col:
        st.markdown(f"<h1 style='color: white; text-shadow: 2px 2px #000;'>{TXT['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #fff; font-weight: bold;'>[ 🟢 {TXT['subtitle']} ]</p>", unsafe_allow_html=True)

    # Center placement login block card structure
    st.markdown("<br>", unsafe_allow_html=True)
    login_card = st.container()
    with login_card:
        farmer_name = st.text_input(TXT["name_lbl"]).strip().lower()
        farmer_aadhaar = st.text_input(TXT["aadhaar_lbl"], max_chars=12)
        
        if st.button(TXT["btn_login"]):
            if len(farmer_aadhaar) != 12 or not farmer_aadhaar.isdigit():
                st.error(TXT["err_len"])
            elif farmer_name in GOVT_DATABASE and GOVT_DATABASE[farmer_name] == farmer_aadhaar:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error(TXT["err_match"])

# --- 6. SECURE LOGGED IN DASHBOARD CONTEXT ---
else:
    with header_col:
        st.markdown(f"<h1 style='color: white; text-shadow: 2px 2px #000;'>{TXT['title']}</h1>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.write(f"🧑‍🌾 User Grid Master: **{farmer_name.upper()}**")
        if st.button(TXT["logout"]):
            st.session_state.logged_in = False
            st.session_state.tracker_stage = 0
            st.rerun()

    st.write(f"### {TXT['status_title']}")
    left_box, right_box = st.columns(2)
    with left_box:
        st.metric(label="📍 Block A Space Used", value=f"{st.session_state.block_a_used} / {BLOCK_A_MAX} Tons")
    with right_box:
        st.metric(label="📍 Block B Space Used", value=f"{st.session_state.block_b_used} / {BLOCK_B_MAX} Tons")
        
    st.divider()
    
    # --- AUTOMATED ROUTE TRACKING HUB ---
    st.write("### 🚚 Automated Transit Tracking Engine")

    route_database = {
        0: {"status": "📦 Dispatched from Farm Hub", "place": "Gummidipoondi Village Hub", "lat": 13.4079, "lon": 80.1235, "percentage": 33},
        1: {"status": "🚛 Passing Highway Checkpoint Alpha", "place": "Red Hills Toll Plaza", "lat": 13.1972, "lon": 80.1685, "percentage": 66},
        2: {"status": "🏭 Arrived at Procurement Center Gate", "place": "Chennai Industrial Zone Depot", "lat": 13.0827, "lon": 80.2707, "percentage": 100}
    }

    if st.session_state.has_booked:
        st.info("Your booking is registered! Click the tracking update button below to poll the vehicle's satellite sensor.")
        
        if st.button("🛰️ Refresh Live Location Data"):
            st.session_state.tracker_stage = (st.session_state.tracker_stage + 1) % 3
            st.rerun()
        
        current_data = route_database[st.session_state.tracker_stage]
        st.progress(current_data["percentage"])
        st.success(f"**Item Status:** {current_data['status']}")
        st.info(f"📍 **Current Location Place Name:** {current_data['place']}")
        
        tracking_map_data = pd.DataFrame({'lat': [current_data['lat']], 'lon': [current_data['lon']]})
        st.map(tracking_map_data, zoom=11)
    else:
        st.warning("⚪ **Current Stage:** No active delivery tracking found. Please input storage quantity and click an available slot booking option below to activate the delivery routing tracker.")

    st.divider()

    # --- LOCK & CANCELLATION LOGIC CONTROLLER ---
    if st.session_state.has_booked:
        st.warning(f"🔒 You have already secured a slot for **{st.session_state.booked_slot}** ({st.session_state.booked_amount} Tons in {st.session_state.allocated_block}).")
        
        if st.button("❌ Cancel Current Registration"):
            if st.session_state.allocated_block == "Block A":
                st.session_state.block_a_used -= st.session_state.booked_amount
            elif st.session_state.allocated_block == "Block B":
                st.session_state.block_b_used -= st.session_state.booked_amount
                
            st.session_state.has_booked = False
            st.session_state.booked_slot = ""
            st.session_state.booked_amount = 0
            st.session_state.allocated_block = ""
            st.session_state.tracker_stage = 0 
            st.rerun()

    else:
        goods_amount = st.number_input("Enter the amount of goods you want to bring (in Tons):", min_value=0)

    st.write("### ⏰ Select an Available Booking Slot:")
    col1, col2, col3 = st.columns(3)

    def process_booking(slot_time, amount):
        if amount <= 0:
            st.warning("Please enter a valid amount of goods greater than 0.")
            return

        space_left_in_a = BLOCK_A_MAX - st.session_state.block_a_used
        space_left_in_b = BLOCK_B_MAX - st.session_state.block_b_used

        if amount <= space_left_in_a:
            st.session_state.block_a_used += amount
            st.session_state.has_booked = True
            st.session_state.booked_slot = slot_time
            st.session_state.booked_amount = amount
            st.session_state.allocated_block = "Block A"
            st.rerun()
        
        elif amount <= space_left_in_b:
            st.session_state.block_b_used += amount
            st.session_state.has_booked = True
            st.session_state.booked_slot = slot_time
            st.session_state.booked_amount = amount
            st.session_state.allocated_block = "Block B"
            st.rerun()
        
        else:
            st.error("🚨 Booking Failed! Both blocks lack capacity for this load.")

    with col1:
        if st.button("09:00 AM - 12:00 PM"):
            process_booking("09:00 AM - 12:00 PM", goods_amount)

    with col2:
        if st.button("12:00 PM - 03:00 PM"):
            process_booking("12:00 PM - 03:00 PM", goods_amount)

    with col3:
        if st.button("03:00 PM - 06:00 PM"):
            process_booking("03:00 PM - 06:00 PM", goods_amount)
