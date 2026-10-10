# Defines 38 career profiles with skill requirements, descriptions, and roadmap data in both English and Persian.

import json
from data.skills import SKILL_LIST

# Career profiles with skill scores in order: analytical_thinking, logical_thinking, creativity, communication,
# leadership, problem_solving, curiosity, learning_speed, attention_to_detail, stress_tolerance, teamwork, mathematics.
CAREERS = [
    {"title_en": "Software Engineer", "title_fa": "مهندس نرم‌افزار", "category": "tech",
     "skills": [9, 9, 6, 5, 4, 9, 8, 8, 7, 6, 6, 7], "demand": 92, "salary": "high",
     "desc_en": "Designs, builds, and maintains software applications and systems.",
     "desc_fa": "طراحی، ساخت و نگهداری نرم‌افزارها و سامانه‌های کامپیوتری."},

    {"title_en": "AI / Machine Learning Engineer", "title_fa": "مهندس هوش مصنوعی و یادگیری ماشین", "category": "tech",
     "skills": [9, 9, 7, 5, 4, 9, 9, 9, 7, 6, 6, 9], "demand": 97, "salary": "very_high",
     "desc_en": "Builds and deploys machine learning models to solve real-world problems.",
     "desc_fa": "طراحی و پیاده‌سازی مدل‌های هوش مصنوعی برای حل مسائل واقعی."},

    {"title_en": "Data Scientist", "title_fa": "دانشمند داده", "category": "tech",
     "skills": [9, 8, 6, 6, 4, 8, 9, 8, 8, 6, 6, 9], "demand": 93, "salary": "very_high",
     "desc_en": "Extracts insights and predictions from large, complex datasets.",
     "desc_fa": "استخراج بینش و پیش‌بینی از داده‌های حجیم و پیچیده."},

    {"title_en": "Cybersecurity Analyst", "title_fa": "کارشناس امنیت سایبری", "category": "tech",
     "skills": [8, 9, 5, 5, 4, 9, 8, 8, 9, 8, 5, 6], "demand": 94, "salary": "high",
     "desc_en": "Protects computer systems and networks from digital threats.",
     "desc_fa": "محافظت از سامانه‌ها و شبکه‌های کامپیوتری در برابر تهدیدات سایبری."},

    {"title_en": "Backend Developer", "title_fa": "توسعه‌دهنده بک‌اند", "category": "tech",
     "skills": [8, 9, 5, 4, 3, 8, 7, 7, 7, 6, 6, 6], "demand": 88, "salary": "high",
     "desc_en": "Builds the server-side logic, databases, and APIs behind applications.",
     "desc_fa": "توسعه منطق سمت سرور، پایگاه‌داده و رابط‌های برنامه‌نویسی برنامه‌ها."},

    {"title_en": "Frontend Developer", "title_fa": "توسعه‌دهنده فرانت‌اند", "category": "tech",
     "skills": [6, 7, 8, 5, 3, 7, 7, 7, 7, 5, 6, 4], "demand": 85, "salary": "medium",
     "desc_en": "Builds the visual, interactive parts of websites and applications.",
     "desc_fa": "توسعه بخش‌های بصری و تعاملی وب‌سایت‌ها و برنامه‌ها."},

    {"title_en": "DevOps Engineer", "title_fa": "مهندس دواپس", "category": "tech",
     "skills": [7, 8, 5, 5, 4, 8, 7, 7, 8, 7, 6, 5], "demand": 89, "salary": "high",
     "desc_en": "Automates and manages infrastructure, deployment, and system reliability.",
     "desc_fa": "خودکارسازی و مدیریت زیرساخت، استقرار و پایداری سامانه‌ها."},

    {"title_en": "Cloud Engineer", "title_fa": "مهندس زیرساخت ابری", "category": "tech",
     "skills": [8, 8, 5, 5, 4, 8, 7, 8, 7, 6, 6, 6], "demand": 90, "salary": "high",
     "desc_en": "Designs and manages scalable cloud infrastructure and services.",
     "desc_fa": "طراحی و مدیریت زیرساخت‌های ابری مقیاس‌پذیر."},

    {"title_en": "Game Developer", "title_fa": "توسعه‌دهنده بازی", "category": "tech",
     "skills": [7, 7, 9, 5, 4, 8, 8, 7, 7, 5, 7, 6], "demand": 75, "salary": "medium",
     "desc_en": "Designs and programs interactive video games.",
     "desc_fa": "طراحی و برنامه‌نویسی بازی‌های ویدیویی تعاملی."},

    {"title_en": "Database Administrator", "title_fa": "مدیر پایگاه داده", "category": "tech",
     "skills": [8, 8, 3, 4, 3, 7, 5, 6, 9, 6, 5, 6], "demand": 72, "salary": "medium",
     "desc_en": "Manages, secures, and optimizes an organization's databases.",
     "desc_fa": "مدیریت، ایمن‌سازی و بهینه‌سازی پایگاه‌های داده سازمان."},

    {"title_en": "Mechanical Engineer", "title_fa": "مهندس مکانیک", "category": "engineering",
     "skills": [8, 8, 6, 5, 4, 8, 6, 6, 8, 6, 6, 8], "demand": 78, "salary": "high",
     "desc_en": "Designs and analyzes mechanical systems and machinery.",
     "desc_fa": "طراحی و تحلیل سیستم‌ها و ماشین‌آلات مکانیکی."},

    {"title_en": "Electrical Engineer", "title_fa": "مهندس برق", "category": "engineering",
     "skills": [8, 8, 5, 5, 4, 8, 6, 6, 8, 6, 5, 8], "demand": 80, "salary": "high",
     "desc_en": "Designs and develops electrical systems and equipment.",
     "desc_fa": "طراحی و توسعه سیستم‌ها و تجهیزات الکتریکی."},

    {"title_en": "Civil Engineer", "title_fa": "مهندس عمران", "category": "engineering",
     "skills": [7, 7, 5, 6, 5, 7, 5, 5, 8, 6, 6, 7], "demand": 76, "salary": "high",
     "desc_en": "Designs and oversees construction of infrastructure like roads and buildings.",
     "desc_fa": "طراحی و نظارت بر ساخت زیرساخت‌هایی مانند جاده و ساختمان."},

    {"title_en": "Industrial Engineer", "title_fa": "مهندس صنایع", "category": "engineering",
     "skills": [7, 7, 5, 6, 6, 7, 5, 5, 7, 6, 7, 7], "demand": 74, "salary": "medium",
     "desc_en": "Optimizes complex processes, systems, and organizations.",
     "desc_fa": "بهینه‌سازی فرایندها، سیستم‌ها و سازمان‌های پیچیده."},

    {"title_en": "Embedded Systems Engineer", "title_fa": "مهندس سیستم‌های نهفته", "category": "engineering",
     "skills": [8, 9, 5, 4, 3, 8, 7, 7, 8, 6, 5, 7], "demand": 82, "salary": "high",
     "desc_en": "Designs software and hardware for specialized embedded devices.",
     "desc_fa": "طراحی نرم‌افزار و سخت‌افزار برای دستگاه‌های تعبیه‌شده تخصصی."},

    {"title_en": "Chemical Engineer", "title_fa": "مهندس شیمی", "category": "engineering",
     "skills": [8, 7, 5, 5, 4, 7, 6, 6, 8, 6, 6, 7], "demand": 71, "salary": "high",
     "desc_en": "Designs processes for large-scale chemical, fuel, and material production.",
     "desc_fa": "طراحی فرایندهای تولید مواد شیمیایی و سوخت در مقیاس صنعتی."},

    {"title_en": "Product Manager", "title_fa": "مدیر محصول", "category": "business",
     "skills": [6, 6, 6, 8, 8, 7, 7, 6, 5, 7, 8, 4], "demand": 87, "salary": "high",
     "desc_en": "Defines product vision and coordinates teams to build it.",
     "desc_fa": "تعیین چشم‌انداز محصول و هماهنگی تیم‌ها برای ساخت آن."},

    {"title_en": "Project Manager", "title_fa": "مدیر پروژه", "category": "business",
     "skills": [5, 6, 4, 8, 8, 6, 5, 5, 6, 8, 8, 4], "demand": 80, "salary": "medium",
     "desc_en": "Plans, coordinates, and delivers projects on time and on budget.",
     "desc_fa": "برنامه‌ریزی، هماهنگی و تحویل پروژه‌ها در زمان و بودجه مشخص."},

    {"title_en": "Business Analyst", "title_fa": "تحلیلگر کسب‌وکار", "category": "business",
     "skills": [8, 7, 4, 7, 5, 7, 6, 6, 7, 5, 6, 6], "demand": 83, "salary": "medium",
     "desc_en": "Analyzes business processes and translates needs into solutions.",
     "desc_fa": "تحلیل فرایندهای کسب‌وکار و تبدیل نیازها به راه‌حل."},

    {"title_en": "Financial Analyst", "title_fa": "تحلیلگر مالی", "category": "business",
     "skills": [8, 7, 3, 5, 4, 6, 5, 5, 8, 6, 5, 8], "demand": 79, "salary": "high",
     "desc_en": "Analyzes financial data to guide investment and business decisions.",
     "desc_fa": "تحلیل داده‌های مالی برای هدایت تصمیمات سرمایه‌گذاری و کسب‌وکار."},

    {"title_en": "Accountant", "title_fa": "حسابدار", "category": "business",
     "skills": [6, 6, 2, 4, 3, 5, 3, 4, 9, 5, 4, 8], "demand": 68, "salary": "medium",
     "desc_en": "Manages financial records, reporting, and tax compliance.",
     "desc_fa": "مدیریت اسناد مالی، گزارش‌دهی و امور مالیاتی."},

    {"title_en": "Entrepreneur", "title_fa": "کارآفرین", "category": "business",
     "skills": [6, 5, 8, 8, 9, 8, 8, 7, 4, 9, 6, 5], "demand": 70, "salary": "very_high",
     "desc_en": "Builds and runs a new business from the ground up.",
     "desc_fa": "ساخت و اداره یک کسب‌وکار جدید از ابتدا."},

    {"title_en": "Marketing Manager", "title_fa": "مدیر بازاریابی", "category": "business",
     "skills": [5, 5, 8, 9, 6, 6, 6, 5, 5, 6, 7, 3], "demand": 81, "salary": "medium",
     "desc_en": "Plans and leads campaigns to promote products and brands.",
     "desc_fa": "برنامه‌ریزی و هدایت کمپین‌های تبلیغاتی برای معرفی محصولات و برند."},

    {"title_en": "UI Designer", "title_fa": "طراح رابط کاربری", "category": "creative",
     "skills": [5, 5, 9, 6, 3, 6, 6, 6, 8, 4, 6, 3], "demand": 80, "salary": "medium",
     "desc_en": "Designs the visual look and feel of digital interfaces.",
     "desc_fa": "طراحی نمای بصری و ظاهر رابط‌های دیجیتال."},

    {"title_en": "UX Designer", "title_fa": "طراح تجربه کاربری", "category": "creative",
     "skills": [6, 6, 8, 7, 4, 7, 7, 6, 7, 4, 6, 3], "demand": 82, "salary": "medium",
     "desc_en": "Researches and designs how users experience and interact with products.",
     "desc_fa": "پژوهش و طراحی تجربه تعامل کاربران با محصولات."},

    {"title_en": "Graphic Designer", "title_fa": "طراح گرافیک", "category": "creative",
     "skills": [4, 4, 9, 5, 2, 5, 6, 5, 7, 4, 5, 2], "demand": 65, "salary": "low",
     "desc_en": "Creates visual content for branding, print, and digital media.",
     "desc_fa": "خلق محتوای بصری برای برندسازی، چاپ و رسانه دیجیتال."},

    {"title_en": "Content Writer", "title_fa": "نویسنده محتوا", "category": "creative",
     "skills": [5, 5, 8, 8, 3, 5, 7, 5, 6, 4, 4, 2], "demand": 70, "salary": "low",
     "desc_en": "Writes articles, copy, and content for brands and publications.",
     "desc_fa": "نگارش مقاله، متن تبلیغاتی و محتوا برای برندها و رسانه‌ها."},

    {"title_en": "Architect", "title_fa": "معمار", "category": "creative",
     "skills": [6, 6, 8, 6, 5, 7, 6, 5, 8, 5, 6, 6], "demand": 68, "salary": "high",
     "desc_en": "Designs buildings and physical spaces, balancing form and function.",
     "desc_fa": "طراحی ساختمان‌ها و فضاهای فیزیکی با تعادل بین زیبایی و کارکرد."},

    {"title_en": "Research Scientist", "title_fa": "پژوهشگر علمی", "category": "science",
     "skills": [9, 8, 7, 5, 4, 8, 9, 8, 8, 6, 5, 7], "demand": 75, "salary": "medium",
     "desc_en": "Conducts original research to expand scientific knowledge.",
     "desc_fa": "انجام پژوهش‌های علمی برای گسترش دانش بشری."},

    {"title_en": "Biotechnologist", "title_fa": "متخصص زیست‌فناوری", "category": "science",
     "skills": [8, 7, 6, 5, 4, 7, 8, 7, 8, 6, 5, 6], "demand": 73, "salary": "medium",
     "desc_en": "Applies biology and technology to develop products and processes.",
     "desc_fa": "استفاده از زیست‌شناسی و فناوری برای توسعه محصولات و فرایندها."},

    {"title_en": "Environmental Scientist", "title_fa": "کارشناس محیط زیست", "category": "science",
     "skills": [7, 6, 5, 6, 4, 6, 8, 6, 7, 5, 6, 5], "demand": 71, "salary": "medium",
     "desc_en": "Studies environmental problems and develops solutions to protect ecosystems.",
     "desc_fa": "بررسی مسائل زیست‌محیطی و توسعه راه‌حل برای حفاظت از اکوسیستم."},

    {"title_en": "Physician", "title_fa": "پزشک", "category": "healthcare",
     "skills": [8, 7, 4, 7, 6, 8, 6, 6, 9, 9, 7, 5], "demand": 90, "salary": "very_high",
     "desc_en": "Diagnoses and treats illness and injury in patients.",
     "desc_fa": "تشخیص و درمان بیماری و آسیب در بیماران."},

    {"title_en": "Nurse", "title_fa": "پرستار", "category": "healthcare",
     "skills": [5, 5, 3, 8, 5, 6, 5, 5, 8, 8, 8, 3], "demand": 88, "salary": "medium",
     "desc_en": "Provides direct patient care and support in medical settings.",
     "desc_fa": "ارائه مراقبت مستقیم و پشتیبانی از بیماران در محیط‌های درمانی."},

    {"title_en": "Pharmacist", "title_fa": "داروساز", "category": "healthcare",
     "skills": [7, 6, 2, 6, 4, 5, 5, 5, 9, 6, 5, 5], "demand": 76, "salary": "high",
     "desc_en": "Dispenses medication and advises on safe, effective drug use.",
     "desc_fa": "تجویز دارو و مشاوره درباره مصرف ایمن و مؤثر آن."},

    {"title_en": "Teacher", "title_fa": "معلم", "category": "education",
     "skills": [5, 5, 6, 9, 6, 5, 6, 5, 5, 7, 7, 4], "demand": 72, "salary": "low",
     "desc_en": "Educates and mentors students in a subject or skill area.",
     "desc_fa": "آموزش و راهنمایی دانش‌آموزان در یک حوزه یا مهارت خاص."},

    {"title_en": "Lawyer", "title_fa": "وکیل", "category": "legal",
     "skills": [7, 8, 4, 9, 6, 7, 6, 6, 8, 8, 5, 3], "demand": 77, "salary": "high",
     "desc_en": "Advises clients and represents them in legal matters.",
     "desc_fa": "مشاوره به موکلان و نمایندگی آن‌ها در مسائل حقوقی."},

    {"title_en": "Psychologist", "title_fa": "روان‌شناس", "category": "social",
     "skills": [6, 5, 5, 9, 4, 6, 7, 5, 6, 7, 5, 2], "demand": 79, "salary": "medium",
     "desc_en": "Studies human behavior and helps people manage mental health.",
     "desc_fa": "بررسی رفتار انسان و کمک به مدیریت سلامت روان."},

    {"title_en": "HR Manager", "title_fa": "مدیر منابع انسانی", "category": "business",
     "skills": [4, 4, 4, 9, 7, 5, 5, 4, 6, 7, 8, 2], "demand": 74, "salary": "medium",
     "desc_en": "Manages hiring, culture, and employee relations within an organization.",
     "desc_fa": "مدیریت استخدام، فرهنگ سازمانی و روابط کارکنان."},
]

# Roadmap progression steps for each career category in both languages.
ROADMAPS = {
    "tech": {
        "en": ["Junior {t}", "{t}", "Senior {t}", "Lead {t}", "Principal {t} / CTO"],
        "fa": ["{t} جونیور", "{t}", "{t} ارشد", "سرپرست تیم {t}", "مدیر ارشد فنی (CTO)"],
    },
    "engineering": {
        "en": ["Junior {t}", "{t}", "Senior {t}", "Engineering Manager", "Director of Engineering"],
        "fa": ["{t} جونیور", "{t}", "{t} ارشد", "مدیر مهندسی", "مدیر ارشد مهندسی"],
    },
    "business": {
        "en": ["{t} (Entry-Level)", "{t}", "Senior {t}", "{t} Manager", "Head of Department"],
        "fa": ["{t} (سطح ورود)", "{t}", "{t} ارشد", "مدیر {t}", "مدیر بخش"],
    },
    "creative": {
        "en": ["Junior {t}", "{t}", "Senior {t}", "Lead {t}", "Creative Director"],
        "fa": ["{t} جونیور", "{t}", "{t} ارشد", "سرپرست {t}", "مدیر خلاقیت"],
    },
    "science": {
        "en": ["Research Assistant", "{t}", "Senior {t}", "Principal Investigator", "Head of Research"],
        "fa": ["دستیار پژوهشی", "{t}", "{t} ارشد", "محقق اصلی", "رئیس پژوهش"],
    },
    "healthcare": {
        "en": ["Resident / Trainee", "{t}", "Senior {t}", "Specialist {t}", "Department Head"],
        "fa": ["دستیار / کارآموز", "{t}", "{t} ارشد", "متخصص {t}", "رئیس بخش"],
    },
    "education": {
        "en": ["Trainee {t}", "{t}", "Senior {t}", "Head of Department", "School Principal"],
        "fa": ["{t} کارآموز", "{t}", "{t} ارشد", "مدیر گروه آموزشی", "مدیر مدرسه"],
    },
    "legal": {
        "en": ["Junior {t}", "{t}", "Senior {t}", "Partner", "Managing Partner"],
        "fa": ["{t} جونیور", "{t}", "{t} ارشد", "شریک", "شریک ارشد"],
    },
    "social": {
        "en": ["Trainee {t}", "{t}", "Senior {t}", "Clinical Supervisor", "Practice Director"],
        "fa": ["{t} کارآموز", "{t}", "{t} ارشد", "سرپرست بالینی", "مدیر مرکز درمانی"],
    },
}


def make_job_id(title_en):
    # Generate a URL-friendly job ID from the English title.
    job_id = title_en.lower()
    job_id = job_id.replace(" / ", "_")
    job_id = job_id.replace(" ", "_")
    job_id = job_id.replace("(", "")
    job_id = job_id.replace(")", "")
    return job_id


def top_skills(skills_dict, count):
    # Return the top N skills with the highest scores from a skills dictionary.
    items = list(skills_dict.items())
    items.sort(key=lambda pair: pair[1], reverse=True)
    result = []
    for i in range(count):
        result.append(items[i][0])
    return result


def build_all_jobs():
    # Build the complete list of job objects from the CAREERS data.
    jobs = []

    for career in CAREERS:
        # Create skill mean dictionary from the skills list.
        skills_dict = {}
        for i in range(len(SKILL_LIST)):
            skills_dict[SKILL_LIST[i]] = career["skills"][i]

        # Generate job ID and required skills list.
        job_id = make_job_id(career["title_en"])
        required = top_skills(skills_dict, 4)

        # Generate roadmap steps for both languages.
        template = ROADMAPS[career["category"]]
        roadmap_en = []
        for step in template["en"]:
            roadmap_en.append(step.format(t=career["title_en"]))
        roadmap_fa = []
        for step in template["fa"]:
            roadmap_fa.append(step.format(t=career["title_fa"]))

        # Build the complete job dictionary.
        job = {
            "id": job_id,
            "title": {"en": career["title_en"], "fa": career["title_fa"]},
            "category": career["category"],
            "description": {"en": career["desc_en"], "fa": career["desc_fa"]},
            "skills_mean": skills_dict,
            "skills_std": 0.8,
            "required_skills": required,
            "market_demand": career["demand"],
            "salary_level": career["salary"],
            "roadmap": {"en": roadmap_en, "fa": roadmap_fa},
        }
        jobs.append(job)

    return jobs


if __name__ == "__main__":
    # Generate and save the jobs data to a JSON file.
    jobs = build_all_jobs()

    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

    print("Wrote " + str(len(jobs)) + " careers to data/jobs.json")