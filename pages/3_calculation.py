import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta


st.title("คำนวณเวลาเดินทาง: จากบ้านไปที่ทำงาน")
st.caption("กรอกข้อมูลระยะทาง โหมดการเดินทาง สภาพอากาศ และระยะเวลารถติด เพื่อคำนวณเวลาเดินทางโดยประมาณ")


def format_duration(minutes: float) -> str:
    if minutes is None or pd.isna(minutes):
        return "N/A"
    minutes = max(0, float(minutes))
    h = int(minutes // 60)
    m = int(round(minutes % 60))
    if h > 0:
        return f"{h} ชั่วโมง {m} นาที"
    return f"{m} นาที"


distance_km = st.number_input("ระยะทาง (กม.)", min_value=0.0, value=10.0, step=0.5)
mode = st.selectbox(
        "วิธีการเดินทาง",
        options=["รถยนต์", "มอเตอร์ไซค์", "ขนส่งสาธารณะ", "จักรยาน", "เดินเท้า"],
        index=0,
    )
weather = st.selectbox(
    "สภาพอากาศ",
    options=["แดดออก", "เมฆมาก", "ฝนตก", "หมอก", "พายุฝน"],
    index=0,
)

traffic = st.select_slider(
    "สภาพการจราจร",
    options=["น้อย", "ปานกลาง", "หนาแน่น", "ติดมาก"],
    value="ปานกลาง",
)

depart_time = st.time_input("เวลาออกเดินทาง", value=time(8, 0))

st.sidebar.markdown("---")
st.sidebar.caption("เคล็ดลับ: ชั่วโมงเร่งด่วน (07:00-09:00, 16:30-19:30) จะทำให้ช้าลง")

BASE_SPEED = {
    "รถยนต์": 40.0,
    "มอเตอร์ไซค์": 45.0,
    "ขนส่งสาธารณะ": 25.0,
    "จักรยาน": 15.0,
    "เดินเท้า": 5.0,
}

WEATHER_FACTOR = {
    "แดดออก": 1.00,
    "เมฆมาก": 0.95,
    "ฝนตก": 0.80,
    "หมอก": 0.85,
    "พายุฝน": 0.60,
}

TRAFFIC_FACTOR = {
    "น้อย": 1.10,      
    "ปานกลาง": 0.90,
    "หนาแน่น": 0.70,
    "ติดมาก": 0.50,
}

BUFFER_MIN = {
    "รถยนต์": 5.0,       
    "มอเตอร์ไซค์": 2.0,
    "ขนส่งสาธารณะ": 8.0, 
    "จักรยาน": 1.0,
    "เดินเท้า": 0.0,
}


def peak_factor(mode_name: str, t: time) -> float:
    affected = {"รถยนต์", "มอเตอร์ไซค์", "ขนส่งสาธารณะ"}
    if mode_name not in affected:
        return 1.0
    in_morning_peak = time(7, 0) <= t <= time(9, 0)
    in_evening_peak = time(16, 30) <= t <= time(19, 30)
    return 0.85 if (in_morning_peak or in_evening_peak) else 1.0


if distance_km <= 0:
    st.warning("โปรดกรอกระยะทางที่มากกว่า 0 กม.")
else:
    base = BASE_SPEED[mode]
    w_fac = WEATHER_FACTOR[weather]
    t_fac = TRAFFIC_FACTOR[traffic]
    p_fac = peak_factor(mode, depart_time)

    effective_speed = max(0.1, base * w_fac * t_fac * p_fac) 
    travel_hours = distance_km / effective_speed
    buffer_min = BUFFER_MIN[mode]
    est_minutes = travel_hours * 60 + buffer_min

    st.header("ผลการคำนวณ")
    st.metric("เวลาโดยประมาณ", format_duration(est_minutes))

    depart_dt = datetime.combine(date.today(), depart_time)
    arrive_dt = depart_dt + timedelta(minutes=est_minutes)
    st.markdown(
        f"เวลาออกเดินทาง: {depart_dt.strftime('%H:%M')}  ",
    )
    st.markdown(
        f"เวลาไปถึงโดยประมาณ: {arrive_dt.strftime('%H:%M')}"
    )

    st.markdown("---")
    st.subheader("รายละเอียดสมมติฐาน")
    d1, d2, d3, d4 = st.columns(4)
    d1.write(f"ความเร็วฐาน: {base:.0f} กม./ชม.")
    d2.write(f"ปัจจัยอากาศ: × {w_fac:.2f}")
    d3.write(f"ปัจจัยการจราจร: × {t_fac:.2f}")
    d4.write(f"ปัจจัยชั่วโมงเร่งด่วน: × {p_fac:.2f}")
    st.write(f"ความเร็วที่คำนวณได้: {effective_speed:.1f} กม./ชม.")
    st.write(f"เวลาเผื่อ: {buffer_min:.0f} นาที")

    st.info(
        "หมายเหตุ: ผลลัพธ์เป็นการประมาณจากสมมติฐานทั่วไป อาจแตกต่างจากเวลาจริงขึ้นกับสภาพถนน อุบัติเหตุ เส้นทางที่เลือก และเหตุการณ์ไม่คาดคิด"
    )
