#!/usr/bin/env python3
"""
سكريبت لتوليد ملف index.json تلقائياً من ملفات النسخ الاحتياطية
يقرأ جميع ملفات .polaris.json في المجلد ويولد index.json
"""

import os
import json
import re
from datetime import datetime

def extract_info_from_filename(filename):
    """استخراج معلومات من اسم الملف"""
    # نمط: polaris_backup_2025-07-16.polaris.json
    # أو: polaris_backup_2025-Q1.polaris.json
    
    info = {
        "filename": filename,
        "label": filename.replace('.polaris.json', '').replace('polaris_backup_', ''),
        "year": None,
        "quarter": None
    }
    
    # محاولة استخراج السنة
    year_match = re.search(r'(\d{4})', filename)
    if year_match:
        info["year"] = year_match.group(1)
    
    # محاولة استخراج الربع
    quarter_match = re.search(r'[Qq](\d)', filename)
    if quarter_match:
        info["quarter"] = quarter_match.group(1)
        quarter_num = info["quarter"]
        quarter_names = {
            "1": "الربع الأول",
            "2": "الربع الثاني", 
            "3": "الربع الثالث",
            "4": "الربع الرابع"
        }
        if info["year"]:
            info["label"] = f"{quarter_names.get(quarter_num, f'الربع {quarter_num}')} {info['year']}"
    
    # محاولة استخراج التاريخ
    date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if date_match and not quarter_match:
        year, month, day = date_match.groups()
        info["year"] = year
        # تحديد الربع من الشهر
        month_num = int(month)
        if 1 <= month_num <= 3:
            info["quarter"] = "1"
        elif 4 <= month_num <= 6:
            info["quarter"] = "2"
        elif 7 <= month_num <= 9:
            info["quarter"] = "3"
        else:
            info["quarter"] = "4"
        
        info["label"] = f"{year}-{month}-{day}"
    
    return info

def generate_index_json():
    """توليد ملف index.json من الملفات الموجودة"""
    # الحصول على المجلد الحالي
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # البحث عن جميع ملفات .polaris.json
    backup_files = []
    for filename in os.listdir(current_dir):
        if filename.endswith('.polaris.json'):
            backup_files.append(filename)
    
    # ترتيب الملفات
    backup_files.sort()
    
    # استخراج المعلومات
    backups = []
    for filename in backup_files:
        info = extract_info_from_filename(filename)
        backups.append(info)
    
    # إنشاء البيانات
    data = {
        "backups": backups,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_count": len(backups)
    }
    
    # حفظ الملف
    index_path = os.path.join(current_dir, 'index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم توليد index.json بنجاح!")
    print(f"📊 عدد النسخ الاحتياطية: {len(backups)}")
    print(f"📁 الملفات:")
    for backup in backups:
        print(f"   - {backup['label']} ({backup['filename']})")

if __name__ == "__main__":
    generate_index_json()

