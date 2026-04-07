<div align="center">
  <img src="core/static/core/images/TOPARCH-LOGO-ol-2.png" alt="Logo" width="100" height="25">
  <h1 align="center">TOPARCH Website Project</h1>
  
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
    <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  </p>

  <p align="center">
    ระบบเว็บไซต์บริษัท TOPARCH CO., LTD. เน้นความเรียบง่าย ทันสมัย และจัดการข้อมูลง่าย
    <br />
    <a href="#-features">ดูฟีเจอร์</a> •
    <a href="#-installation">วิธีติดตั้ง</a> •
    <a href="#-contact">ติดต่อเรา</a>
  </p>
</div>

---

## ✨ ฟีเจอร์หลัก (Features)
- [x] **Responsive Design:** 📱 รองรับทุกหน้าจอตั้งแต่จอมือถือไปจนถึงจอ 4K
- [x] **Admin Dashboard:** 🔐 ระบบจัดการข้อมูลหลังบ้านที่ปลอดภัย
- [x] **Portfolio:** 🖼️ จัดแสดงผลงานแยกตามหมวดหมู่

## 📸 Screenshots
<img src="toparch_web/core/static/core/images/main-img.png" alt="website 1" width="100%">

## 📦 วิธีการติดตั้ง (Installation)

1. **Clone & Enter Folder**
```bash
git clone <link-to-repo>
cd toparch_web
```
2. **Setup Environment**
```bash
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```
3. **Install & Migrate**
```bash
# Windows:
pip install -r requirements.txt
python manage.py makemigrations      
python manage.py migrate
```
4.**Activate**
```bash
. venv\Scripts\activate      
```
5.**ตรวจสอบสถานะการ Migration**
```bash
python manage.py showmigrations
```
6.**Create Admin**
```bash
python manage.py createsuperuser        
```

📂 โครงสร้างโฟลเดอร์ (Project Structure)
```bash
Plaintext
├── core/               # Settings & Configuration
├── apps/               # Business Logic Apps
├── static/             # CSS, JS, Images
└── templates/          # HTML Templates
```
👤 ติดต่อผู้พัฒนา
[PIYAPAT JUNGKAPAE]

📧 Email: donutpiyapat@gmail.com

LinkIn: https://www.linkedin.com/in/piyapat-jungkapae-435125381/