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
        "User Profile": "User Profile",
        "User Name": "User Name",
        "User Email": "User Email",
        "Register": "Register",
        "Login": "Login",
        "Logout": "Logout",
        "Save User": "Save User",
        "User Login": "User Login",
        "User Registration": "User Registration",
        "Cansel": "Cansel",
        "Logged in as {user_name}": "Logged in as {user_name}",
        "Login successful. Access granted to the app.": "Login successful. Access granted to the app.",
        "You have logged out and returned to guest access.": "You have logged out and returned to guest access.",
        "Please enter your user name.": "Please enter your user name.",
        "Please enter your email address.": "Please enter your email address.",
        "User profile saved successfully.": "User profile saved successfully.",
        "User profile confirmed successfully.": "User profile confirmed successfully.",
        "User registered successfully. Please log in with your saved credentials.": "User registered successfully. Please log in with your saved credentials.",
        "User registered successfully.": "User registered successfully.",
        "User not found. Access granted as guest. Transactions, contract details, and email sending stay restricted.": "User not found. Access granted as guest. Transactions, contract details, and email sending stay restricted.",
        "User not found in the saved user list. Please register first or continue as guest.": "User not found in the saved user list. Please register first or continue as guest.",
        "Report issued by: {user_name}": "Report issued by: {user_name}",
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
        "User Profile": "ملف المستخدم",
        "User Name": "اسم المستخدم",
        "User Email": "بريد المستخدم",
        "Register": "تسجيل",
        "Login": "تسجيل الدخول",
        "Logout": "تسجيل الخروج",
        "Save User": "حفظ المستخدم",
        "User Login": "تسجيل الدخول",
        "User Registration": "تسجيل المستخدم",
        "Cansel": "إلغاء",
        "Logged in as {user_name}": "تم تسجيل الدخول كـ {user_name}",
        "Login successful. Access granted to the app.": "تم تسجيل الدخول بنجاح. تم منح الوصول للتطبيق.",
        "You have logged out and returned to guest access.": "تم تسجيل الخروج والعودة إلى الوصول كضيف.",
        "Please enter your user name.": "يرجى إدخال اسم المستخدم.",
        "Please enter your email address.": "يرجى إدخال البريد الإلكتروني.",
        "User profile saved successfully.": "تم حفظ ملف المستخدم بنجاح.",
        "User profile confirmed successfully.": "تم تأكيد ملف المستخدم بنجاح.",
        "User registered successfully. Please log in with your saved credentials.": "تم تسجيل المستخدم بنجاح. يرجى تسجيل الدخول باستخدام بياناتك المحفوظة.",
        "User registered successfully.": "تم تسجيل المستخدم بنجاح.",
        "User not found. Access granted as guest. Transactions, contract details, and email sending stay restricted.": "لم يتم العثور على المستخدم. تم منح الوصول كضيف. المعاملات وتفاصيل العقد وإرسال البريد الإلكتروني تبقى مقيدة.",
        "User not found in the saved user list. Please register first or continue as guest.": "لم يتم العثور على المستخدم في القائمة المحفوظة. يرجى التسجيل أولاً أو المتابعة كضيف.",
        "Report issued by: {user_name}": "تم إصدار التقرير من قبل: {user_name}",
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
    if re.search(r"[A-Za-z]", text):
        return text

    normalized = text.strip()
    if not normalized:
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
