<h1 align="center">AppRent Manager</h1>

<p align="center">
  <img src="./static/img/logo.png" alt="AppRent Logo" width="60"/>
</p>
<p align="center">
   <u>Tool for Landlords Managing Rental Apartments</u>
</p>

## 📌 Summary

**AppRent Manager** is a **financial management system** that offers landlords a **real-time overview of all rental payments and property-related financial activities**. It is designed for both **individual landlords** and **professionals** managing rental properties on behalf of clients. The application allows users to **update financial records**, add necessary details, and make notes explaining discrepancies in bills for different months.

This application is a **valuable tool** for efficiently managing **rental properties** and keeping **financial records** under control.

---

## 📑 Table of Contents

- [Project Goal](#-project-goal)
- [Technologies Used](#️-technologies-used)
- [Application Overview](#️-application-overview)
- [Database Diagram](#-database-diagram)
- [Installation & Usage](#-installation--usage)
- [Author](#-author)

---

## 🎯 Project Goal

The goal of this project is to simplify **financial management** for rental properties by providing an intuitive platform where users can track **payments**, update records, and manage essential rental data.

### 💼 Business Applications

- Helps **landlords** and **property managers** maintain an overview of **rental payments**.
- Enables efficient **financial tracking** and management of **rental income** and **expenses**.
- Provides an easy way to **document** and justify **financial changes**.

---

## 🛠️ Technologies Used

**AppRent Manager** is built using modern web technologies to ensure reliability and scalability.

- **Backend**: [Python](https://www.python.org/), [Flask](https://flask.palletsprojects.com/)
- **Database**: [SQLAlchemy ORM](https://www.sqlalchemy.org/) with support for SQLite, PostgreSQL, and other databases
- **Frontend**: [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML), [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS), [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), [Jinja templates](https://jinja.palletsprojects.com/)
- **Styling**: [Bootstrap](https://getbootstrap.com/) for responsive design

<p align="center">
  <img src="https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/flask-%23000000.svg?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQL-%23F7DF1E.svg?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/sqlalchemy-%23D71F00.svg?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/jinja-%23B41717.svg?style=for-the-badge&logo=jinja&logoColor=white"/>
  <img src="https://img.shields.io/badge/javascript-%23F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black"/>
  <img src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white"/>
  <img src="https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white"/>
</p>

---

## 🖥️ Application Overview

### 📸 Screenshots

Below are some screenshots showcasing different parts of the application:

1. **Entry page**

   - the welcome page of the application;

   ![Main Dashboard](./static/img/index.png)

2. **User Dashboard**

   - provides an overview of all rental properties assigned to the user;
   - allows the user to add, update, and delete apartment records;

   ![Payment Management](./static/img/dashboard.png)

3. **Apartment Manage - Rental Agreement Section**

   - section for managing financial aspects of a specific apartment;
   - in the **Rental Agreement** tab, the user can add a rental agreement via a dedicated form;

   ![Financial Overview](./static/img/apartment-manager_Rental-Agreement.png)

   3.1 **Add New Rental Agreement**

   - a form where the user enters details to create a new rental agreement, including rent amount, tenant, and dates;

   Part I:
   ![Settings](./static/img/apartment-manager_New-Rental-Agreement.png)

   Part II:
   ![Settings](./static/img/apartment-manager_New-Rental-Agreement-PartII.png)

4. **Apartment Manage - Monthly Rent Payments Section**

   - enables users to manage monthly rent payments;
   - payments can be marked as **paid** or **unpaid**;

   ![Rental Agreements](./static/img/apartment-manager_Monthly-Rent-Payments.png)

5. **Apartment Manage - Bills Section**

   - In this section users can add different types of bills:
     - Bills included in settlements (e.g. administrative fees, utilities);
     - Bills not included in settlements (e.g. property tax, insurance);

   ![Settings](./static/img/apartment-manager_Bills.png)

6. **Apartment Manage - Bills Settlement Section**

   - displays a summary of all utility bills and their payment status;
   - helps the landlord and tenant settle monthly costs - **summarizes the status of utility bill payments between the landlord and the tenant**;

   ![Settings](./static/img/apartment-manager_Bills-Settlement.png)

7. **Admin panel - Admin-Only Section**

   - this section is available only to admin users;
   - admins can manage user roles, set permissions, and add new admin accounts;

![Settings](./static/img/admin-panel.png)

### 🎥 Demo Video

Watch the application in action in the demo below:

**🎥 Watch the demo:** [![Watch the demo](./static/img/demo.png)](https://www.loom.com/share/bc85437ca28449b39311bdd05aaad202)

---

## 🧩 Database Diagram

The **AppRent Manager** database follows a relational model to ensure efficiency and data integrity. The database design is in **third normal form (3NF)**, which ensures that the system is both efficient and flexible, allowing for easy future expansions and minimizing the risk of data inconsistencies.

### 📌 ER Diagram

Below is the ER diagram showcasing the database structure used in AppRent Manager.

![Diagram baz danych](./static/img/AppRent_Manager-ER_Diagram.svg)

---

## 📦 Installation & Usage

To install and run the project locally, follow these steps:

```bash
# Clone the repository
git clone https://github.com/Wasiak-Remigiusz/AppRent-Manager.git
cd AppRent-Manager

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Edit the .env file to set DATABASE_URL (default is SQLite)
# DATABASE_URL=sqlite:///data.db  # For local SQLite
# DATABASE_URL=postgresql://user:password@host/dbname  # Example for PostgreSQL

# Run the application
python app.py

# Create required tables
curl -X GET http://127.0.0.1:5000/init-app
curl -X GET http://127.0.0.1:5000/create-country-table
curl -X GET http://127.0.0.1:5000/create-currency-table
curl -X GET http://127.0.0.1:5000/create-bill-type-table

```

---

## 👤 Author

**Remigiusz Wasiak**  
[GitHub Profile](https://github.com/Wasiak-Remigiusz)
