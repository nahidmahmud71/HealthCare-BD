# 🩺 Medical Health Companion (Smart Health Assistant)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-ff4b4b)
![Status](https://img.shields.io/badge/Status-Active-success)

**Medical Health Companion** is an interactive, Python-based web application designed to serve as a personal digital health assistant. Tailored specifically for users in **Bangladesh**, it provides real-time BMI analysis, personalized diet charts, home remedies for common illnesses, and quick access to national emergency contacts.

---

## 📖 Table of Contents
- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Future Scope](#-future-scope)
- [Contact](#-contact)

---

## 🌟 Features

### 1. 📊 Advanced BMI Calculator & Diet Planner
- Calculates Body Mass Index (BMI) based on weight and height.
- **Visual Indicator:** Dynamic progress bar showing the user's health status (Underweight, Normal, Overweight, Obese).
- **Automated Diet Chart:** Instantly generates a **Breakfast, Lunch, and Dinner** plan based on the calculated BMI category.
- **Tabbed Interface:** Clean organization of meal plans for easy reading.

### 2. 💊 Smart Health Guide (Remedies)
- Provides detailed advice for common ailments:
  - Fever (জ্বর)
  - Cold & Cough (সর্দি ও কাশি)
  - Acidity/Gastric
  - Headache
  - Dehydration
- **Detailed Insights:** Includes Symptoms, "Do's and Don'ts" (করণীয় ও বর্জনীয়), and Dietary advice.
- **Warning System:** Highlights critical symptoms requiring immediate doctor consultation.

### 3. 🚑 Emergency Services (Bangladesh Context)
- Quick access buttons for National Emergency Helplines:
  - **999:** National Service (Ambulance/Police)
  - **16263:** Shastho Batayon (Health Advice)
  - **109:** Women & Child Support
- **Hospital Checklist:** An interactive checklist of items to carry during a hospital emergency (NID, Cash, Reports, etc.).

### 4. 🌐 User-Friendly Interface
- **Bilingual Support:** Interface mixes English and Bangla for better accessibility.
- **Responsive Design:** Optimized for both desktop and mobile views via Streamlit's wide layout.

---

## 🛠 Tech Stack

* **Language:** Python
* **Frontend Framework:** Streamlit
* **Libraries Used:**
    * `streamlit` (UI and Logic)
    * `pandas` (Data handling - optional for future expansion)
    * `time` (System utilities)

---

## ⚙️ Installation & Setup

Follow these steps to run the application locally on your machine.

### Prerequisites
Make sure you have [Python](https://www.python.org/downloads/) installed.

### Step 1: Clone the Repository
```bash
git clone [https://github.com/your-username/medical-health-companion.git](https://github.com/your-username/medical-health-companion.git)
cd medical-health-companion
