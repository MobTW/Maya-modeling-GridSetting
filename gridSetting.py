import maya.cmds as cmds

def apply_grid_size(*args):
    """
    ฟังก์ชันหลัก: คำนวณและปรับ Grid ทันทีเมื่อมีการเลือก Radio Button
    """
    # 1. Safety Check: ตรวจสอบ Working Units
    current_unit = cmds.currentUnit(query=True, linear=True)
    
    # ถ้าไม่ใช่ meter ให้เด้งเตือน
    if current_unit != 'm':
        # แปลงชื่อหน่วยสำหรับข้อความแจ้งเตือน
        unit_full_names = {'cm': 'centimeter', 'mm': 'millimeter', 'in': 'inch', 'ft': 'foot', 'yd': 'yard'}
        shown_unit = unit_full_names.get(current_unit, current_unit)
        
        cmds.confirmDialog(
            title='Unit Mismatch', 
            message=f'Error: Current unit is "{shown_unit}".\nPlease change Preference to "meter" first.', 
            button=['OK'], 
            icon='critical'
        )
        # รีเซ็ต Radio Button กลับไปที่ Default (1m)
        cmds.radioCollection("gridSizeCollection", edit=True, select="rb_1m")
        return

    # 2. ตรวจสอบว่า User เลือก Radio Button อันไหน
    selected_id = cmds.radioCollection("gridSizeCollection", query=True, select=True)
    
    # Map ชื่อปุ่ม กับ ขนาดเป้าหมาย (หน่วยเมตร)
    size_map = {
        "rb_1cm": 0.01,
        "rb_10cm": 0.1,
        "rb_50cm": 0.5,
        "rb_1m": 1.0,
        "rb_10m": 10.0  # <--- เพิ่ม 10 meter ตรงนี้
    }
    
    if selected_id not in size_map:
        return

    target_cell_size = size_map[selected_id]

    # 3. อ่านค่า Subdivisions ปัจจุบันจาก Maya
    current_subdiv = cmds.grid(query=True, divisions=True)
    
    # 4. คำนวณ (Formula: GridLinesEvery = TargetCellSize * Subdivisions)
    new_spacing = target_cell_size * current_subdiv
    
    # 5. สั่งปรับค่า Grid (Grid Lines Every = spacing)
    cmds.grid(spacing=new_spacing)
    
    # Feedback
    print(f"Update: Cell Size {target_cell_size}m | Grid Lines Every set to {new_spacing}")


def update_unit_label():
    """
    ฟังก์ชันสำหรับ Refresh ข้อความบอกหน่วย และแปลงเป็นคำเต็ม
    """
    current_unit = cmds.currentUnit(query=True, linear=True)
    
    unit_map = {
        'm': 'meter',
        'cm': 'centimeter',
        'mm': 'millimeter',
        'in': 'inch',
        'ft': 'foot',
        'yd': 'yard'
    }
    
    full_unit_name = unit_map.get(current_unit, current_unit)
    label_text = f"Working Units : {full_unit_name}"
    
    bg_color = (0.3, 0.7, 0.3) if current_unit == 'm' else (0.8, 0.3, 0.3)
    
    if cmds.text("unitStatusText", exists=True):
        cmds.text("unitStatusText", edit=True, label=label_text, backgroundColor=bg_color)

def create_smart_grid_ui():
    """
    สร้างหน้าต่าง UI
    """
    window_id = "SmartGridScalerWindow"
    
    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id)
    
    # ปรับความสูงเป็น 300 เพื่อให้ปุ่ม 10m แสดงผลครบถ้วน
    cmds.window(window_id, title="Smart Grid Scaler", widthHeight=(300, 300), sizeable=False)
    
    # Layout หลัก
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=['both', 10])
    
    # --- Section 1: Unit Display ---
    cmds.separator(style='none', height=5)
    cmds.text("unitStatusText", label="Checking...", align='center', height=25, font="boldLabelFont")
    update_unit_label() 
    
    cmds.separator(style='in')

    # --- Section 2: Radio Buttons ---
    cmds.text(label="Select Grid Cell Size:", align='left')
    
    cmds.radioCollection("gridSizeCollection")
    
    # รายการตัวเลือกทั้งหมด
    cmds.radioButton("rb_1cm", label="1 cm  (0.01 m)", onCommand=apply_grid_size)
    cmds.radioButton("rb_10cm", label="10 cm (0.10 m)", onCommand=apply_grid_size)
    cmds.radioButton("rb_50cm", label="50 cm (0.50 m)", onCommand=apply_grid_size)
    cmds.radioButton("rb_1m", label="1 meter (1.00 m)", select=True, onCommand=apply_grid_size) 
    
    # ปุ่ม 10 meter ที่ต้องการ
    cmds.radioButton("rb_10m", label="10 meter (10.00 m)", onCommand=apply_grid_size)
    
    cmds.separator(style='none', height=10)
    
    # --- Section 3: Manual Refresh ---
    cmds.button(label="Force Update / Re-Check Unit", command=lambda x: [update_unit_label(), apply_grid_size()])

    cmds.showWindow(window_id)

# Run Script
create_smart_grid_ui()
