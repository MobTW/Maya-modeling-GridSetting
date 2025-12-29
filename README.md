# Maya-modeling-GridSetting

สรุประบบ Logic การทำงานของ Script

1. ส่วนแสดงผล (UI Display & Validation)
Header Label: แสดงข้อความสถานะปัจจุบัน เช่น "Working Units: meter" หรือ "Working Units: centimeter" โดยดึงค่าจริงมาจาก PreferencesSafety Check:เมื่อกดปุ่มทำงาน สคริปต์จะเช็คก่อนว่า Working Units เป็น "meter" หรือไม่กรณีไม่ใช่ meter: จะเด้ง Warning แจ้งเตือนให้ user ไปเปลี่ยนหน่วยก่อน และจะไม่ทำการปรับ Grid ใดๆกรณีเป็น meter: ระบบจะทำงานต่อในส่วนคำนวณ

2. ส่วนเลือกขนาด (Radio Buttons)
จะมีตัวเลือกให้เลือกเพียง 1 อย่าง (Radio Collection) ดังนี้:
1 cm (0.01 m)
10 cm (0.10 m)
50 cm (0.50 m)
1 meter (1.00 m)
10 meter (10.00 m)

3. สูตรการคำนวณ (Calculation Logic)
โจทย์คือต้องการให้ ช่องว่างเล็กที่สุดใน Grid (Cell Size) มีขนาดเท่ากับค่าที่เลือกตัวแปรคงที่ (อ่านค่าจาก Maya): Subdivisions (เช่น ค่าปัจจุบันคือ 5)ตัวแปรเป้าหมาย (จากที่เลือก): Target Cell Size (เช่น 10cm หรือ 0.1m)ตัวแปรที่ต้องปรับ (Output): Grid Lines Everyสูตร:
{Grid Lines Every} = {Target Cell Size} x {Subdivisions}
ตัวอย่างการคำนวณ :
User เลือก: 10 cm (0.1 เมตร)Maya Subdivisions ปัจจุบัน: 5คำนวณ: $0.1 \times 5 = 0.5$ผลลัพธ์: สคริปต์จะปรับค่า Grid Lines Every เป็น 0.5
