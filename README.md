# 🧒 Child Adoption & Sponsorship Web Application  
*A Full-Stack Django-Based Platform for Adoption, Sponsorship & Child Welfare Management*

## 📌 Overview  
This project is a full-stack **Child Adoption and Sponsorship Management System** built using **Django**.  
It helps organizations manage child profiles, adoption requests, sponsorship activities, and communication with users in a secure and structured way.

---

## 🚀 Features

### 👶 Child Management  
- CRUD operations for child profiles  
- Store details like age, background, education, health status, etc.

### 📝 Adoption & Sponsorship Requests  
- Users can submit adoption or sponsorship requests  
- Admin can review, approve, or reject requests  

### 🔐 User Authentication  
- Secure login and registration system  
- Profile editing  
- Role-based access control (User vs Admin)

### 🛠 Admin Dashboard  
- Manage children, users, and requests  
- Approve/reject adoption and sponsorship applications  

### 📧 Email Notifications  
- Sends automated emails to users for approvals, rejections, and visit scheduling  

### 💰 Child Sponsorship  
Users can donate for specific needs, such as:  
- Medical treatment  
- Education  
- General welfare  

Tracks sponsorship history for transparency.

### 🔒 Security & Validation  
- Strong input validation  
- Secure handling of user and payment information  
- Proper access separation between users and admins

---

## 🏗 Tech Stack  
- **Backend:** Django  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** SQLite / PostgreSQL  
- **Authentication:** Django Auth System  
- **Email:** SMTP-based notifications  

---

## 📂 Project Modules  
- **User Module:** Registration, Login, Profile Management  
- **Child Module:** Add, View, Update, Delete Children  
- **Adoption Module:** Request submission + admin approval  
- **Sponsorship Module:** Donate & track sponsorship  
- **Admin Module:** Dashboard for managing all operations  

---

## 🧪 Setup Instructions

```bash
# Clone the repository
git clone https://github.com/your-username/your-repo-name.git

# Navigate into project directory
cd your-repo-name

just activate the environment:

env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver


After that just run the project:

python manage.py runserver

then click on the localhost link which takes to the webapplication


