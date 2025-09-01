# 🏠 Household Services Management App

## Overview  
This project is a **full-stack web application** designed to manage household services by connecting **customers**, **service professionals**, and an **admin**. It supports end-to-end workflows like booking services, managing requests, professional approvals, and feedback collection.  

The app demonstrates skills in **backend development (Flask, SQLAlchemy)**, **frontend templating (Jinja2, Bootstrap)**, and **database design** with a well-structured schema.  

---

## Key Highlights  
- **Role-Based Dashboards**  
  - **Admin** – Manage services, approve professionals, block users, monitor system activity.  
  - **Customers** – Browse & book services, schedule requests, track status, provide ratings.  
  - **Professionals** – Accept/reject jobs, track service history, view ratings.  

- **Full-Stack Implementation**  
  - **Backend:** Flask + SQLAlchemy  
  - **Frontend:** Jinja2 + HTML + Bootstrap5  
  - **Visuals:** ChartJS for interactive service/request summaries  

- **Database Design**  
  - 6 core tables: `Users`, `Customers`, `ServiceProfessionals`, `Services`, `ServiceRequests`, `ServiceRejections`  
  - Clear relationships between roles, services, and transactions  
  - Optimized schema for scalability and search functionality  

---

## Architecture  
- **Templates** – Role-specific UIs (`admin-`, `customer-`, `prof-`) using Jinja2  
- **Static Assets** – CSS, Bootstrap, and branding  
- **Backend** – Flask controllers for each role, with centralized DB models  
- **Database** – SQLite (tested with DBeaver)  

* High-level flow:*  
1. Users sign up/login.  
2. Customers create service requests.  
3. Professionals accept/reject requests.  
4. Admin monitors activity and ensures quality.  

---

## Database ER Diagram  
👉 *(Upload your ER diagram image in repo and update path below)*  
![ER Diagram](./assets/er-diagram.png)  

---

## 🖼️ Screenshots  

- **Login Page**  
  ![Login Screenshot](./assets/login.png)  

- **Customer Dashboard**  
  ![Customer Dashboard](./assets/customer-dashboard.png)  

- **Admin Panel**  
  ![Admin Panel](./assets/admin-panel.png)  

---

## Tech Stack  
- **Backend:** Flask, SQLAlchemy, SQLite  
- **Frontend:** HTML, CSS, Bootstrap5, Jinja2  
- **Visualization:** ChartJS  
- **Tools:** DBeaver, FlaskSQLAlchemy  

---

## 🎥 Demo Video  
🔗 [Project Presentation Video](https://drive.google.com/file/d/12HGKhjrD0s2mfCr2qPDfIEG9AiRlrWIJ/view?usp=drive_link)  

---

## Learnings & Takeaways  
- Designed and implemented a **relational database** with role-based relationships.  
- Built a **full-stack Flask app** integrating backend models, controllers, and templating.  
- Gained experience with **role-based access control** and secure CRUD operations.  
- Learned to visualize data and insights using **ChartJS**.  

---

## Future Improvements  
- Add authentication with JWT/session management.  
- Deploy on a cloud platform (Heroku/AWS).  
- Expand to support **payment gateway integration**.  
- Build a **mobile-friendly UI** or PWA version.  

---
