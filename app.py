from flask import Flask, render_template, request, redirect, url_for,  session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:#lydia4578@localhost/ProvidenceHospital'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Define the Doctor model
class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    years_of_experience = db.Column(db.Integer, nullable=False)

class Nurse(db.Model):
    __tablename__ = 'nurses'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    years_of_experience = db.Column(db.Integer, nullable=False)

class Pharmacist(db.Model):
    __tablename__ = 'pharmacists'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    license_number = db.Column(db.String(100), nullable=False)
    years_of_experience = db.Column(db.Integer, nullable=False)
    
class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    body_temperature = db.Column(db.Float)
    pulse_rate = db.Column(db.Integer)
    respiration_rate = db.Column(db.Integer)
    blood_pressure = db.Column(db.String(20))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    doctor = db.relationship('Doctor', backref=db.backref('patients', lazy=True))
    
class PatientReport(db.Model):
    __tablename__ = 'patient_reports'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    report = db.Column(db.Text, nullable=True)
    drugs = db.Column(db.Text, nullable=True)
    referrals = db.Column(db.Text, nullable=True)
    patient = db.relationship('Patient', backref=db.backref('reports', lazy=True))
    doctor = db.relationship('Doctor', backref=db.backref('reports', lazy=True))


class Dosage(db.Model):
    __tablename__ = 'dosages'
    id = db.Column(db.Integer, primary_key=True)
    patient_report_id = db.Column(db.Integer, db.ForeignKey('patient_reports.id'), nullable=False)
    dosage = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    patient_report = db.relationship('PatientReport', backref=db.backref('dosage', uselist=False))



with app.app_context():
    db.create_all()


@app.route('/add_new_account', methods=['GET', 'POST'])
def add_new_account():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        years_of_experience = request.form.get('years_of_experience')
        new_user = None
        if user_type == 'doctor':
            specialization = request.form.get('specialization')
            new_user = Doctor(first_name=first_name, last_name=last_name, specialization=specialization, years_of_experience=years_of_experience)
            db.session.add(new_user)
        elif user_type == 'nurse':
            department = request.form.get('department')
            new_user = Nurse(first_name=first_name, last_name=last_name, department=department, years_of_experience=years_of_experience)
            db.session.add(new_user)
        elif user_type == 'pharmacist':
            license_number = request.form.get('license_number')
            new_user = Pharmacist(first_name=first_name, last_name=last_name, license_number=license_number, years_of_experience=years_of_experience)
            db.session.add(new_user)
        db.session.commit()
        flash(f'Account added successfully, and this is your ID: {new_user.id}', 'success')
        return redirect(url_for('add_new_account'))
    return render_template('add_new_account.html')

@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/patients', methods=['GET', 'POST'])
def patients_page():
    return render_template('patients.html')

@app.route('/patients_login', methods=['POST'])
def patients_login():
    nurse_id = request.form.get('nurseId')
    last_name = request.form.get('lastName')
    
    # Check nurse credentials
    nurse = Nurse.query.filter_by(id=nurse_id, last_name=last_name).first()
    if nurse:
        session['nurse_id'] = nurse.id
        session['nurse_name'] = nurse.first_name  # Assuming first_name is stored
        
        # Flash success message and redirect to patients options
        flash(f'Welcome, {nurse.first_name}!', 'success')
        return redirect(url_for('patients_options'))
    else:
        flash('Invalid credentials. Please try again.', 'danger')
        return redirect(url_for('patients_page'))

@app.route('/patients_options')
def patients_options():
    nurse_name = session.get('nurse_name')
    if nurse_name:
        return render_template('patients_options.html', nurse_name=nurse_name)
    else:
        flash('Please log in first.', 'danger')
        return redirect(url_for('patients_page'))


@app.route('/manage_patients')
def manage_patients():
    return render_template('manage_patients.html')

@app.route('/existing_patient')
def existing_patient():
    nurse_name = session.get('nurse_name')
    if nurse_name:
        return render_template('existing_patient_options.html', nurse_name=nurse_name)
    else:
        flash('Please log in first.', 'danger')
        return redirect(url_for('patients_page'))

@app.route('/new_patient')
def new_patient():
    return render_template('new_patient.html')

@app.route('/view_patient', methods=['POST'])
def view_patient():
    patient_id = request.form.get('patientId')

    # Query the Patient table for patient details
    patient = Patient.query.filter_by(id=patient_id).first()

    if patient:
        return render_template('patient_details.html', patient=patient)
    else:
        flash("Patient not found.", 'danger')
        return redirect(url_for('existing_patient'))

@app.route('/add_patient', methods=['POST'])
def add_patient():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        sex = request.form.get('sex')
        age = request.form.get('age')
        height = request.form.get('height')
        weight = request.form.get('weight')
        temperature = request.form.get('temperature')
        pulse_rate = request.form.get('pulseRate')
        respiration_rate = request.form.get('respirationRate')
        blood_pressure = request.form.get('bloodPressure')

        # Create new Patient object
        new_patient = Patient(
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            age=age,
            height=height,
            weight=weight,
            body_temperature=temperature,
            pulse_rate=pulse_rate,
            respiration_rate=respiration_rate,
            blood_pressure=blood_pressure
        )

        # Add new patient to the database
        db.session.add(new_patient)
        db.session.commit()

        flash('Patient added successfully.', 'success')
        return redirect(url_for('patients_options'))
    else:
        abort(405)  # Method Not Allowed
        
@app.route('/assign_doctor', methods=['GET', 'POST'])
def assign_doctor():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        specialization = request.form.get('specialization')
        
        # Check if patient exists
        patient = Patient.query.get(patient_id)
        if patient:
            # Fetch doctors based on specialization
            doctors = Doctor.query.filter_by(specialization=specialization).all()
            return render_template('choose_doctor.html', doctors=doctors, patient_id=patient_id)
        else:
            flash('Patient not found.', 'danger')
            return redirect(url_for('assign_doctor'))
    return render_template('assign_doctor.html')

@app.route('/assign_patient_to_doctor', methods=['POST', 'GET'])
def assign_patient_to_doctor():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        doctor_id = request.form.get('doctor_id')
        
        # Check if patient exists
        patient = Patient.query.get(patient_id)
        if patient:
            patient.doctor_id = doctor_id
            try:
                db.session.commit()
                flash('Doctor assigned successfully.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error assigning doctor to patient: {e}', 'danger')
        else:
            flash('Patient not found.', 'danger')
    
    # After assigning, redirect back to the assign_doctor page
    return redirect(url_for('assign_doctor'))

@app.route('/view_all_patients')
def view_all_patients():
    patients = Patient.query.all()
    return render_template('view_all_patients.html', patients=patients)

@app.route('/view_patient_by_id', methods=['GET', 'POST'])
def view_patient_by_id():
    if request.method == 'POST':
        patient_id = request.form.get('patientId')
        patient = Patient.query.filter_by(id=patient_id).first()
        if patient:
            return render_template('view_patient.html', patient=patient)
        else:
            flash('Patient not found.', 'danger')
            return redirect(url_for('view_patient_by_id'))
    return render_template('view_patient_by_id.html')

@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        last_name = request.form.get('last_name')
        doctor = Doctor.query.filter_by(id=doctor_id, last_name=last_name).first()
        if doctor:
            session['doctor_id'] = doctor_id
            flash(f'Welcome Dr. {doctor.last_name}', 'success')
            return redirect(url_for('doctor_dashboard'))
        else:
            flash('Invalid doctor ID or last name.', 'danger')
    return render_template('doctor_login.html')

@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'doctor_id' not in session:
        flash('Please log in to access the doctor dashboard.', 'danger')
        return redirect(url_for('doctor_login'))
    return render_template('doctor_dashboard.html')

@app.route('/assigned_patients')
def assigned_patients():
    if 'doctor_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('doctor_login'))

    doctor_id = session['doctor_id']
    patients = Patient.query.filter_by(doctor_id=doctor_id).all()
    return render_template('assigned_patients.html', patients=patients)

@app.route('/write_doctor_review', methods=['GET', 'POST'])
def write_doctor_review():
    if 'doctor_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('doctor_login'))

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        doctor_id = session['doctor_id']
        report = request.form.get('report')
        drugs = request.form.get('drugs')
        referrals = request.form.get('referrals')

        patient = Patient.query.get(patient_id)
        if patient and (patient.doctor_id is None or patient.doctor_id == int(doctor_id)):
            patient_report = PatientReport(
                patient_id=patient_id,
                doctor_id=doctor_id,
                report=report,
                drugs=drugs,
                referrals=referrals
            )
            if patient.doctor_id is None:
                patient.doctor_id = doctor_id  # Assign doctor to patient if not already assigned
            db.session.add(patient_report)
            try:
                db.session.commit()
                flash('Review submitted successfully.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error submitting review: {e}', 'danger')
        else:
            flash('Patient not found or you are not assigned to this patient.', 'danger')
    return render_template('write_doctor_review.html')

@app.route('/update_doctor_review', methods=['GET', 'POST'])
def update_doctor_review():
    if 'doctor_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('doctor_login'))

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        patient_report = PatientReport.query.filter_by(patient_id=patient_id).first()

        if patient_report:
            patient = Patient.query.get(patient_id)
            doctor = Doctor.query.get(patient_report.doctor_id)

            if 'update_review' in request.form:
                # Update the patient report with new data from the form
                patient_report.report = request.form.get('report', patient_report.report)
                patient_report.drugs = request.form.get('drugs', patient_report.drugs)
                patient_report.referrals = request.form.get('referrals', patient_report.referrals)
                try:
                    db.session.commit()
                    flash('Patient review updated successfully.', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash('Error updating patient review.', 'danger')
            return render_template('update_doctor_review.html', patient_report=patient_report, patient=patient, doctor=doctor)
        else:
            flash('No review found for the given patient ID.', 'danger')

    return render_template('update_patient_review_form.html')

@app.route('/view_patient_review', methods=['GET', 'POST'])
def view_patient_review():
    if 'doctor_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('doctor_login'))

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        patient_report = PatientReport.query.filter_by(patient_id=patient_id).first()
        patient = Patient.query.get(patient_id)  # Assuming you have a Patient model

        if patient_report:
            doctor = Doctor.query.get(patient_report.doctor_id)
            return render_template('view_patient_review.html', patient=patient, patient_report=patient_report, doctor=doctor)
        else:
            flash('No review found for the given patient ID.', 'danger')

    return render_template('view_patient_review_form.html')





@app.route('/view_patients')
def view_patients():
    return render_template('view_patients.html')

@app.route('/new_report', methods=['GET', 'POST'])
def new_report():
    if request.method == 'POST':
        # Handle form submission logic here
        patient_id = request.form.get('patientId')
        report = request.form.get('report')
        recommendation = request.form.get('recommendation')
        # Save the report and recommendation to the database
        return redirect(url_for('doctor_dashboard'))
    return render_template('new_report.html')

@app.route('/edit_report', methods=['GET', 'POST'])
def edit_report():
    if request.method == 'POST':
        # Handle form submission logic here
        patient_id = request.form.get('patientId')
        report = request.form.get('report')
        recommendation = request.form.get('recommendation')
        # Update the existing report and recommendation in the database
        return redirect(url_for('doctor_dashboard'))
    return render_template('edit_report.html')

@app.route('/pharmacist_login', methods=['GET', 'POST'])
def pharmacist_login():
    if request.method == 'POST':
        pharmacist_id = request.form.get('pharmacist_id')
        last_name = request.form.get('last_name')

        pharmacist = Pharmacist.query.filter_by(id=pharmacist_id, last_name=last_name).first()
        if pharmacist:
            session['pharmacist_id'] = pharmacist.id
            flash('Login successful!', 'success')
            return redirect(url_for('pharmacist_dashboard'))
        else:
            flash('Invalid ID or last name. Please try again.', 'danger')

    return render_template('pharmacist_login.html')

@app.route('/pharmacist_dashboard')
def pharmacist_dashboard():
    if 'pharmacist_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('pharmacist_login'))
    return render_template('pharmacist_dashboard.html')

@app.route('/pharmacist_view_all_reports')
def pharmacist_view_all_reports():
    if 'pharmacist_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('pharmacist_login'))

    patient_reports = PatientReport.query.all()
    return render_template('pharmacist_view_all_reports.html', patient_reports=patient_reports)

    
    # Render template with form to input patient ID
    return render_template('pharmacist_view_patient_form.html')

@app.route('/pharmacist_view_report', methods=['GET', 'POST'])
def pharmacist_view_report():
    if 'pharmacist_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('pharmacist_login'))

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        patient_report = PatientReport.query.filter_by(patient_id=patient_id).first()

        if patient_report:
            return render_template('pharmacist_view_report.html', patient_report=patient_report)
        else:
            flash('No report found for the given patient ID.', 'danger')

    return render_template('pharmacist_view_report_form.html')

@app.route('/pharmacist_write_dosage', methods=['GET', 'POST'])
def pharmacist_write_dosage():
    if 'pharmacist_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('pharmacist_login'))

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        dosage = request.form.get('dosage')
        price = request.form.get('price')
        availability = request.form.get('availability') == 'True'

        patient_report = PatientReport.query.filter_by(patient_id=patient_id).first()
        if patient_report:
            new_dosage = Dosage(
                patient_report_id=patient_report.id,
                dosage=dosage,
                price=price,
                availability=availability
            )
            db.session.add(new_dosage)
            db.session.commit()
            flash('Dosage and price added successfully.', 'success')
            return render_template('pharmacist_view_report.html', patient_report=patient_report)
        else:
            flash('No report found for the given patient ID.', 'danger')

    return render_template('pharmacist_write_dosage_form.html')

@app.route('/pharmacist_view_dosage', methods=['GET', 'POST'])
def pharmacist_view_dosage():
    if 'pharmacist_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('pharmacist_login'))

    if request.method == 'POST':
        patient_report_id = request.form.get('patient_report_id')
        dosage = Dosage.query.filter_by(patient_report_id=patient_report_id).first()
        
        if dosage:
            return render_template('pharmacist_view_dosage.html', dosage=dosage)
        else:
            flash('No dosage information found for the given patient report ID.', 'danger')

    return render_template('pharmacist_view_dosage_form.html')

@app.route('/pharmacist_update_dosage', methods=['GET', 'POST'])
def pharmacist_update_dosage():
    if 'pharmacist_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('pharmacist_login'))

    if request.method == 'POST':
        patient_report_id = request.form.get('patient_report_id')
        dosage = Dosage.query.filter_by(patient_report_id=patient_report_id).first()
        
        if dosage:
            if 'update_dosage' in request.form:
                dosage.dosage = request.form.get('dosage')
                dosage.price = request.form.get('price')
                dosage.availability = request.form.get('availability') == 'True'
                db.session.commit()
                flash('Dosage information updated successfully.', 'success')
            return render_template('pharmacist_update_dosage.html', dosage=dosage)
        else:
            flash('No dosage information found for the given patient report ID.', 'danger')

    return render_template('pharmacist_update_dosage_form.html')





@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == '123':
            session['user_type'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('admin_login.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/view_records', methods=['GET', 'POST'])
def view_records():
    if request.method == 'POST':
        record_type = request.form.get('record_type')
        if record_type == 'doctor':
            records = Doctor.query.all()
        elif record_type == 'nurse':
            records = Nurse.query.all()
        elif record_type == 'pharmacist':
            records = Pharmacist.query.all()
        return render_template('view_records_table.html', records=records, record_type=record_type)
    return render_template('view_records.html')


@app.route('/update_account', methods=['GET', 'POST'])
def update_account():
    if request.method == 'POST':
        role = request.form.get('role')
        id = request.form.get('id')
        if role == 'doctor':
            record = Doctor.query.get(id)
        elif role == 'nurse':
            record = Nurse.query.get(id)
        elif role == 'pharmacist':
            record = Pharmacist.query.get(id)
        else:
            record = None

        if record:
            return render_template('update_account_form.html', role=role, record=record)
        else:
            flash(f"No record found for {role.capitalize()} with ID {id}", 'danger')
            return redirect(url_for('update_account'))
    
    return render_template('update_account.html')

@app.route('/update_account_record/<role>/<int:id>', methods=['POST'])
def update_account_record(role, id):
    if role == 'doctor':
        doctor = Doctor.query.get_or_404(id)
        doctor.first_name = request.form['first_name']
        doctor.last_name = request.form['last_name']
        doctor.specialization = request.form['specialization']
        doctor.years_of_experience = request.form['years_of_experience']
        db.session.commit()
        flash(f"Dr. {doctor.last_name}'s info has been updated", 'success')
        return redirect(url_for('admin_dashboard'))
    elif role == 'nurse':
        nurse = Nurse.query.get_or_404(id)
        nurse.first_name = request.form['first_name']
        nurse.last_name = request.form['last_name']
        nurse.department = request.form['department']
        nurse.years_of_experience = request.form['years_of_experience']
        db.session.commit()
        flash(f"Nurse {nurse.last_name}'s info has been updated", 'success')
        return redirect(url_for('admin_dashboard'))
    elif role == 'pharmacist':
        pharmacist = Pharmacist.query.get_or_404(id)
        pharmacist.first_name = request.form['first_name']
        pharmacist.last_name = request.form['last_name']
        pharmacist.license_number = request.form['license_number']
        pharmacist.years_of_experience = request.form['years_of_experience']
        db.session.commit()
        flash(f"Pharmacist {pharmacist.last_name}'s info has been updated", 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        abort(404)

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        role = request.form.get('role')
        id = request.form.get('id')

        if role == 'doctor':
            doctor = Doctor.query.get(id)
            if doctor:
                return render_template('view_delete_doctor.html', doctor=doctor)
            else:
                flash(f"Doctor with ID {id} does not exist.", 'danger')

        elif role == 'nurse':
            nurse = Nurse.query.get(id)
            if nurse:
                return render_template('view_delete_nurse.html', nurse=nurse)
            else:
                flash(f"Nurse with ID {id} does not exist.", 'danger')

        elif role == 'pharmacist':
            pharmacist = Pharmacist.query.get(id)
            if pharmacist:
                return render_template('view_delete_pharmacist.html', pharmacist=pharmacist)
            else:
                flash(f"Pharmacist with ID {id} does not exist.", 'danger')

        else:
            flash("Invalid role selected.", 'danger')

    return render_template('delete_account.html')

@app.route('/confirm_delete/<role>/<int:id>', methods=['POST'])
def confirm_delete(role, id):
    if role == 'doctor':
        doctor = Doctor.query.get(id)
        if doctor:
            db.session.delete(doctor)
            db.session.commit()
            flash(f"Doctor {doctor.last_name} with ID {doctor.id} has been removed from records.", 'success')
        else:
            flash(f"Doctor with ID {id} does not exist.", 'danger')
    
    elif role == 'nurse':
        nurse = Nurse.query.get(id)
        if nurse:
            db.session.delete(nurse)
            db.session.commit()
            flash(f"Nurse {nurse.last_name} with ID {nurse.id} has been removed from records.", 'success')
        else:
            flash(f"Nurse with ID {id} does not exist.", 'danger')
    
    elif role == 'pharmacist':
        pharmacist = Pharmacist.query.get(id)
        if pharmacist:
            db.session.delete(pharmacist)
            db.session.commit()
            flash(f"Pharmacist {pharmacist.last_name} with ID {pharmacist.id} has been removed from records.", 'success')
        else:
            flash(f"Pharmacist with ID {id} does not exist.", 'danger')
    
    else:
        flash("Invalid role selected.", 'danger')
    
    return redirect(url_for('admin_dashboard'))


@app.route('/logout')
def logout():
    # Clear the session or any other logout logic
    session.clear()
    # Redirect to the appropriate login page based on user type or previous page
    if 'user_type' in session:
        if session['user_type'] == 'doctor':
            return redirect(url_for('doctors_page'))
        elif session['user_type'] == 'nurse':
            return redirect(url_for('patients_page'))
        elif session['user_type'] == 'admin':
            return redirect(url_for('administrators_page'))
        elif session['user_type'] == 'pharmacist':
            return redirect(url_for('pharmacy_page'))
    return redirect(url_for('home_page'))



@app.route('/about')
def about_page():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
