"""Translation resources and i18n helpers for the client manager UI."""

import re

import arabic_reshaper
from bidi.algorithm import get_display

# Shared language state.
CURRENT_LANGUAGE = "eng"


TRANSLATIONS = {
    "eng": {
        "Client": "Client",
        "Client Details": "Client Details",
        "Client Name": "Client Name",
        "Country": "Country",
        "Contact": "Contact Number",
        "Business": "Business",
        "Shop Number": "Shop Number",
        "Address": "Address",
        "Electrical Meter": "Electrical Meter",
        "Email": "Email",
        "Review": "Review",
        "Add Review": "Add Review",
        "Add Client": "Add Client",
        "Save Client": "Save Client",
        "Delete Selected Client": "Delete Selected Client",
        "Progress Overview": "Progress Overview",
        "Progress": "Progress",
        "Tasks": "Tasks",
        "All Tasks": "All Tasks",
        "Pending Tasks": "Pending Tasks",
        "Task Details": "Task Details",
        "New task": "New task",
        "Add Task": "Add Task",
        "Save": "Save",
        "Close": "Close",
        "Home": "Home",
        "Transactions": "Transactions",
        "Payment Report": "Payment Report",
        "Print": "Print",
        "Save Log": "Save Log",
        "Language": "Language",
        "English": "English",
        "العربية": "العربية",
        "Project Manager To-Do": "Project Manager To-Do",
        "Open client payment records": "Open client payment records",
        "No reviews yet": "No reviews yet",
    },
    "ar": {
        "Client": "العميل",
        "Client Details": "تفاصيل العميل",
        "Client Name": "اسم العميل",
        "Country": "الدولة",
        "Contact": "رقم التواصل",
        "Business": "نوع النشاط",
        "Shop Number": "رقم المحل",
        "Address": "العنوان",
        "Electrical Meter": "عداد الكهرباء",
        "Email": "البريد الإلكتروني",
        "Review": "المراجعة",
        "Add Review": "إضافة مراجعة",
        "Add Client": "إضافة عميل",
        "Save Client": "حفظ العميل",
        "Delete Selected Client": "حذف العميل المحدد",
        "Progress Overview": "نظرة عامة على التقدم",
        "Progress": "التقدم",
        "Tasks": "المهام",
        "All Tasks": "جميع المهام",
        "Pending Tasks": "المهام المعلقة",
        "Task Details": "تفاصيل المهمة",
        "New task": "مهمة جديدة",
        "Add Task": "إضافة مهمة",
        "Save": "حفظ",
        "Close": "إغلاق",
        "Home": "الرئيسية",
        "Transactions": "المعاملات",
        "Payment Report": "تقرير الدفع",
        "Print": "طباعة",
        "Save Log": "حفظ السجل",
        "Language": "اللغة",
        "English": "English",
        "العربية": "العربية",
        "Project Manager To-Do": "مدير المشاريع - المهام",
        "Open client payment records": "فتح سجلات الدفع للعميل",
        "No reviews yet": "لا توجد مراجعات بعد",
    },
}


def is_arabic_text(value):
    text = str(value or "")
    return any(
        0x0600 <= ord(ch) <= 0x06FF
        or 0x0750 <= ord(ch) <= 0x077F
        or 0x08A0 <= ord(ch) <= 0x08FF
        or 0xFB50 <= ord(ch) <= 0xFDFF
        or 0xFE70 <= ord(ch) <= 0xFEFF
        for ch in text
    )


def apply_bidi_text(value):
    text = str(value or "")
    if not text:
        return ""
    if not is_arabic_text(text):
        return text
    normalized = text.strip()
    if not normalized:
        return text
    if any(ch in text for ch in "{}()[]<>/\\|=+*#@%$£€¥0123456789"):
        return text
    allowed = set(" \t\n\r" + "0123456789")
    for ch in text:
        if not (
            0x0600 <= ord(ch) <= 0x06FF
            or 0x0750 <= ord(ch) <= 0x077F
            or 0x08A0 <= ord(ch) <= 0x08FF
            or 0xFB50 <= ord(ch) <= 0xFDFF
            or 0xFE70 <= ord(ch) <= 0xFEFF
            or ch in allowed
        ):
            return text
    return get_display(arabic_reshaper.reshape(text))


def set_language(lang):
    global CURRENT_LANGUAGE
    code = str(lang or "eng").strip().lower()
    CURRENT_LANGUAGE = "ar" if code in {"ar", "arabic"} else "eng"
    return CURRENT_LANGUAGE


def T(text, **kwargs):
    language_map = TRANSLATIONS.get(CURRENT_LANGUAGE, TRANSLATIONS["eng"])
    translated = language_map.get(text, text)
    if kwargs:
        translated = translated.format(**kwargs)
    if CURRENT_LANGUAGE == "ar":
        translated = apply_bidi_text(translated)
    return translated


def validate_translation_coverage():
    english_keys = set(TRANSLATIONS.get("eng", {}).keys())
    arabic_keys = set(TRANSLATIONS.get("ar", {}).keys())
    missing = sorted(key for key in english_keys if key not in arabic_keys)
    if missing:
        raise ValueError(
            "Missing Arabic translations for UI labels:\n" + "\n".join(f" - {key}" for key in missing[:50])
        )
    return None
