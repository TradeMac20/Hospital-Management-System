Hospital Management System
Overview
This repository contains a Hospital Management System web application built using Flask, SQLAlchemy, and Bootstrap. The application provides functionalities for managing patients, doctors, nurses, and pharmacists within a hospital environment.

Features
User Authentication: Login and logout functionality for administrators, doctors, nurses, and pharmacists.
Role-Based Access Control: Different levels of access based on user roles.
Patient Management: CRUD operations for patients, including viewing patient details, assigning doctors, and managing medical records.
Doctor Dashboard: Features for doctors to view patient lists, write diagnosis reports, prescribe drugs, and refer patients.
Nurse Dashboard: Patient management options such as assigning doctors and updating patient details.
Pharmacy Dashboard: Drug management functionalities, including writing dosage recommendations, checking drug availability, and updating drug details.
Responsive Design: Bootstrap framework used for responsive and mobile-friendly UI.
Technologies Used
Python: Backend language for server-side logic.
Flask: Micro web framework used for routing and request handling.
SQLAlchemy: ORM for database interaction with PostgreSQL.
HTML/CSS: Frontend markup and styling.
Bootstrap: Frontend framework for responsive design and UI components.

Directory Structure
The repository is structured as follows:

app.py: Main Flask application file containing routes and logic.

templates/: Directory containing HTML templates for different pages.

static/: Directory for static assets like CSS stylesheets, images, and client-side JavaScript files.

static/css/: CSS files for styling.

static/img/: Image files used in the application.

Running the Application

Ensure you have PostgreSQL installed and running.

Run the Application:
python app.py
Access the application at http://localhost:5000 in your web browser.


Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for bug fixes, improvements, or new features.

