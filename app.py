"""
Streamlit Araç Kontrol Formu Uygulaması
FastAPI uygulamasının Streamlit versiyonu
"""
import streamlit as st
from excel_handler import (
    load_vehicles, load_fuel_levels, load_check_fields,
    load_items, load_users, save_form_submission
)

# Sayfa yapılandırması
st.set_page_config(
    page_title="Araç Kontrol Formu",
    page_icon="🚗",
    layout="wide"
)

# Session state başlatma
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'full_name' not in st.session_state:
    st.session_state.full_name = None

def login_page():
    """Login sayfası"""
    st.title("🔐 Giriş Yap")
    
    # Excel'den kullanıcıları yükle
    users = load_users()
    
    with st.form("login_form"):
        username = st.text_input("Kullanıcı Adı", key="login_username")
        password = st.text_input("Şifre", type="password", key="login_password")
        submit_button = st.form_submit_button("Giriş Yap")
        
        if submit_button:
            user = users.get(username)
            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.full_name = user["full_name"]
                st.success("Giriş başarılı!")
                st.rerun()
            else:
                st.error("Kullanıcı adı veya şifre hatalı!")

def form_page():
    """Araç kontrol formu sayfası"""
    st.title("🚗 Araç Kontrol Formu")
    st.write(f"Hoş geldiniz, **{st.session_state.full_name}**")
    
    # Excel'den verileri yükle
    vehicles = load_vehicles()
    fuel_levels = load_fuel_levels()
    items = load_items()
    
    # Kontrol kategorileri
    exterior_fields = load_check_fields("ExteriorChecks")
    engine_fields = load_check_fields("EngineChecks")
    safety_fields = load_check_fields("SafetyEquipment")
    interior_fields = load_check_fields("InteriorChecks")
    
    # Form oluştur
    with st.form("vehicle_inspection_form"):
        st.subheader("Temel Bilgiler")
        
        # Driver Name (readonly)
        driver_name = st.text_input(
            "Driver Name",
            value=st.session_state.full_name,
            disabled=True
        )
        
        # Vehicle seçimi
        vehicle_options = [""] + vehicles + ["Other"]
        selected_vehicle = st.selectbox(
            "Vehicle",
            options=vehicle_options,
            key="vehicle_select"
        )
        
        # Other Vehicle (koşullu)
        other_vehicle = None
        if selected_vehicle == "Other":
            other_vehicle = st.text_input(
                "Manuel Araç Girişi",
                placeholder="Aracı manuel girin",
                key="other_vehicle_input"
            )
        
        # Odometer Reading
        odometer_start = st.number_input(
            "Odometer Reading (Başlangıç KM)",
            min_value=0,
            step=1,
            key="odometer_input"
        )
        
        # Fuel Level
        fuel_options = [""] + fuel_levels
        fuel_level = st.selectbox(
            "Fuel Level",
            options=fuel_options,
            key="fuel_level_select"
        )
        
        # Other Fuel (koşullu)
        other_fuel = None
        if fuel_level == "Other":
            other_fuel = st.text_input(
                "Manuel Yakıt Seviyesi",
                placeholder="Yakıt seviyesini manuel girin",
                key="other_fuel_input"
            )
        
        # Oil Level
        oil_level = st.text_input(
            "Oil Level",
            placeholder="Oil Level",
            key="oil_level_input"
        )
        
        st.divider()
        
        # Exterior Checks
        st.subheader("Exterior Checks")
        with st.expander("Exterior Checks Detayları", expanded=False):
            # Exterior Checks için emoji mapping
            exterior_icons = {
                "headlights": "💡",
                "break_lights": "🛑",
                "indicators": "➡️",
                "mirrors": "🪞",
                "windows": "🪟",
                "windshield": "🚗",
                "wiper_fluid": "💧",
                "wipers": "🧹",
                "tires": "⚙️",
                "body_paint": "🎨"
            }
            
            exterior_checks = {}
            for field in exterior_fields:
                field_display = field.replace("_", " / ").title()
                icon = exterior_icons.get(field, "✅")
                exterior_checks[field] = st.radio(
                    f"{icon} {field_display}",
                    options=["OK", "Needs Attention"],
                    horizontal=True,
                    key=f"exterior_{field}"
                )
        
        # Engine & Mechanical Checks
        st.subheader("Engine & Mechanical Checks")
        with st.expander("Engine & Mechanical Checks Detayları", expanded=False):
            engine_checks = {}
            for field in engine_fields:
                field_display = field.replace("_", " / ").title()
                engine_checks[field] = st.radio(
                    field_display,
                    options=["OK", "Needs Attention"],
                    horizontal=True,
                    key=f"engine_{field}"
                )
        
        # Safety Equipment
        st.subheader("Safety Equipment")
        with st.expander("Safety Equipment Detayları", expanded=False):
            safety_checks = {}
            for field in safety_fields:
                field_display = field.replace("_", " / ").title()
                safety_checks[field] = st.radio(
                    field_display,
                    options=["OK", "Needs Attention"],
                    horizontal=True,
                    key=f"safety_{field}"
                )
        
        # Interior Checks
        st.subheader("Interior Checks")
        with st.expander("Interior Checks Detayları", expanded=False):
            interior_checks = {}
            for field in interior_fields:
                field_display = field.replace("_", " / ").title()
                interior_checks[field] = st.radio(
                    field_display,
                    options=["OK", "Needs Attention"],
                    horizontal=True,
                    key=f"interior_{field}"
                )
        
        st.divider()
        
        # Items in Vehicle
        st.subheader("Items in Vehicle")
        
        # Fuel Card
        fuel_card = st.radio(
            "Fuel Card",
            options=["Yes", "No"],
            horizontal=True,
            key="fuel_card_radio"
        )
        
        # Measuring Tape
        measuring_tape = st.radio(
            "Measuring Tape",
            options=["Yes", "No"],
            horizontal=True,
            key="measuring_tape_radio"
        )
        
        # Safety Vest
        safety_vest = st.radio(
            "Safety Vest",
            options=["Yes", "No"],
            horizontal=True,
            key="safety_vest_radio"
        )
        
        # Fuel Amount
        fuel_amount = st.text_input(
            "Fuel Amount ($)",
            placeholder="Fuel Amount",
            key="fuel_amount_input"
        )
        
        st.divider()
        
        # Submit button
        submit_button = st.form_submit_button("📝 Formu Kaydet", use_container_width=True)
        
        if submit_button:
            # Form verilerini topla
            form_data = {
                "driver_name": driver_name,
                "vehicle": other_vehicle if selected_vehicle == "Other" else selected_vehicle,
                "odometer_start": odometer_start,
                "fuel_level": other_fuel if fuel_level == "Other" else fuel_level,
                "oil_level": oil_level,
                "exterior_checks": exterior_checks,
                "engine_checks": engine_checks,
                "safety_checks": safety_checks,
                "interior_checks": interior_checks,
                "fuel_card": fuel_card,
                "measuring_tape": measuring_tape,
                "safety_vest": safety_vest,
                "fuel_amount": fuel_amount
            }
            
            # Excel'e kaydet
            try:
                from datetime import datetime
                save_form_submission(form_data)
                
                # Başarı mesajı
                st.success("✅ Form başarıyla kaydedildi!")
                st.balloons()
                
                # Detaylı geri bildirim
                with st.container():
                    st.info("📋 **Kaydedilen Bilgiler:**")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Sürücü:** {form_data.get('driver_name', 'N/A')}")
                        st.write(f"**Araç:** {form_data.get('vehicle', 'N/A')}")
                        st.write(f"**KM:** {form_data.get('odometer_start', 'N/A')}")
                        st.write(f"**Yakıt Seviyesi:** {form_data.get('fuel_level', 'N/A')}")
                    
                    with col2:
                        st.write(f"**Yağ Seviyesi:** {form_data.get('oil_level', 'N/A')}")
                        st.write(f"**Yakıt Kartı:** {form_data.get('fuel_card', 'N/A')}")
                        st.write(f"**Ölçü Bandı:** {form_data.get('measuring_tape', 'N/A')}")
                        st.write(f"**Güvenlik Yeleği:** {form_data.get('safety_vest', 'N/A')}")
                    
                    st.write(f"**Kayıt Zamanı:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write(f"**Kayıt Yeri:** `form_submissions.xlsx`")
                
            except Exception as e:
                st.error(f"❌ Form kaydedilirken hata oluştu: {str(e)}")
                with st.expander("🔍 Hata Detayları"):
                    st.exception(e)
            
            # Formu temizle (rerun)
            st.rerun()

def main():
    """Ana uygulama akışı"""
    # Logout butonu (sidebar)
    if st.session_state.logged_in:
        with st.sidebar:
            st.write(f"Kullanıcı: **{st.session_state.full_name}**")
            if st.button("🚪 Çıkış Yap"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.full_name = None
                st.rerun()
    
    # Sayfa yönlendirme
    if not st.session_state.logged_in:
        login_page()
    else:
        form_page()

if __name__ == "__main__":
    main()

