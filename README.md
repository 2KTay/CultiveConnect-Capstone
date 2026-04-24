# CultiveConnect MVP  
### Senior Capstone Project · Purdue University  
**Taemoor Hasan**

![Living Stones Foundation](sandbox:/mnt/data/ab05edc2-32ce-47a7-9a77-f3b36e17deb3.png)

---

## Overview
**CultiveConnect MVP** is my senior capstone project for **Purdue University**. It was developed in connection with the **Living Stones Foundation** and supports the broader CultiveConnect initiative, which aims to help Latin American producers better understand export readiness for the **United States** and **Canada**.

This project turns complex trade and compliance requirements into a working technical prototype that helps producers track documents, understand tariff rules, and identify missing export requirements.

---

## My Role
I contributed to this project through a mix of **software engineering**, **data engineering**, and **data analyst** work.

- **Software Engineering:** built the compliance engine, dashboard logic, bilingual translation workflow, and export readiness interface  
- **Data Engineering:** structured the regulatory source-of-truth database in JSON and organized product, tariff, and compliance data into a usable system  
- **Data Analyst Work:** researched HTS / HS codes, duties, document requirements, and seasonal trade rules, then translated that research into actionable logic and validation outputs  

---

## What the System Does
- stores regulatory rules by **country** and **product**
- translates Spanish document filenames into English compliance terms
- compares uploaded files against required documents
- checks **seasonal tariff windows** for products like grapes and asparagus
- generates a clear **gap analysis** and export readiness result

---

## Tech Stack
- **Python**
- **JSON**
- **React + Vite**
- **Frontend dashboard UI**
- **Rule-based compliance engine**
- **Mock PDF testing suite**

---

## Project Structure
```text
backend/
  compliance_engine.py
  translation_map.py
  data/regulations.json
  mock_uploads/
  validation_report.txt

frontend/
  src/App.jsx
```

---

## How to Run

### Backend
```bash
cd backend
python compliance_engine.py
```


This runs the compliance engine, scans the mock uploads, and generates the validation report.

### Generate PDF Report
```bash
cd backend
python generate_pdf.py

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Then open the local development link shown in the terminal.

---

## Capstone Purpose
This capstone demonstrates how computer science can be applied to a real-world international trade problem. The project combines **structured data**, **business rules**, **bilingual validation**, and **user-facing software design** into one working MVP.

---

## Organization Context
**Living Stones Foundation** supported this project through the CultiveConnect initiative. The larger mission is to reduce barriers for agricultural producers by making export compliance and documentation workflows more understandable and accessible.

---

## Author
**Taemoor Hasan**  
Purdue University  
Senior Capstone Project
