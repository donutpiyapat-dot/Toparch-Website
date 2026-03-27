import os
from PIL import Image

def convert_to_webp(directory):
    # วนลูปหาไฟล์ในโฟลเดอร์
    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            # สร้างชื่อไฟล์ใหม่โดยเปลี่ยนนามสกุลเป็น .webp
            name = os.path.splitext(filename)[0]
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(directory, f"{name}.webp")

            # เริ่มการแปลงไฟล์
            with Image.open(input_path) as img:
                # แก้ไขปัญหาเรื่องการหมุนรูปภาพ (ถ้ามี)
                img = img.convert("RGB") 
                # บันทึกเป็น WebP โดยตั้งค่า Quality (75-80 คือค่าแนะนำ)
                img.save(output_path, "WEBP", quality=80)
                print(f"Converted: {filename} -> {name}.webp")

# ใส่ Path ของโฟลเดอร์รูปภาพที่นี่ (ถ้าไฟล์นี้อยู่ในโฟลเดอร์เดียวกับรูป ให้ใส่ ".")
folder_path = "." 
convert_to_webp(folder_path)
print("--- เสร็จเรียบร้อย! ---")