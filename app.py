from flask import Flask, render_template, request, session, redirect, url_for
from functools import wraps

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'feedback-system-secret-key'

STUDENTS = {
    'S001': {'name': 'Rahul Kumar', 'password': 'pass123'},
    'S002': {'name': 'Priya Sharma', 'password': 'pass123'},
    'S003': {'name': 'Amit Singh', 'password': 'pass123'},
    'S004': {'name': 'Sneha Patel', 'password': 'pass123'},
    'S005': {'name': 'Vikram Rathore', 'password': 'pass123'},
}

FACULTY = {
    'F001': {'name': 'Dr. Anil Sharma', 'password': 'faculty123'},
    'F002': {'name': 'Prof. Sunita Verma', 'password': 'faculty123'},
    'F003': {'name': 'Mr. Rajesh Gupta', 'password': 'faculty123'},
    'F004': {'name': 'Mrs. Anita Desai', 'password': 'faculty123'},
    'F005': {'name': 'Dr. Prakash Rao', 'password': 'faculty123'},
}

REVIEWS = []

def require_student(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'student_id' not in session:
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated_function

def require_faculty(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'faculty_id' not in session:
            return redirect(url_for('faculty_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'student_id' in session:
        return redirect(url_for('review_form'))
    if 'faculty_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('student_login'))

@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_id = request.form.get('student_id', '')
        password = request.form.get('password', '')
        
        if student_id in STUDENTS and STUDENTS[student_id]['password'] == password:
            session['student_id'] = student_id
            session['student_name'] = STUDENTS[student_id]['name']
            return redirect(url_for('review_form'))
        return render_template('student_login.html', error='Invalid credentials')
    
    return render_template('student_login.html')

@app.route('/faculty-login', methods=['GET', 'POST'])
def faculty_login():
    if request.method == 'POST':
        faculty_id = request.form.get('faculty_id', '')
        password = request.form.get('password', '')
        
        if faculty_id in FACULTY and FACULTY[faculty_id]['password'] == password:
            session['faculty_id'] = faculty_id
            session['faculty_name'] = FACULTY[faculty_id]['name']
            return redirect(url_for('dashboard'))
        return render_template('faculty_login.html', error='Invalid credentials')
    
    return render_template('faculty_login.html')

@app.route('/review', methods=['GET', 'POST'])
@require_student
def review_form():
    if request.method == 'POST':
        faculty_id = request.form.get('faculty_id', '')
        behavior = request.form.get('behavior', '')
        punctuality = request.form.get('punctuality', '')
        teaching_method = request.form.get('teaching_method', '')
        comments = request.form.get('comments', '')
        
        review_id = len(REVIEWS) + 1
        REVIEWS.append({
            'id': review_id,
            'faculty_id': faculty_id,
            'behavior': behavior,
            'punctuality': punctuality,
            'teaching_method': teaching_method,
            'comments': comments
        })
        
        return redirect(url_for('thank_you'))
    
    return render_template('review_form.html', faculty=FACULTY)

@app.route('/dashboard')
@require_faculty
def dashboard():
    faculty_id = session['faculty_id']
    faculty_reviews = [r for r in REVIEWS if r['faculty_id'] == faculty_id]
    return render_template('dashboard.html', faculty_name=session['faculty_name'], reviews=faculty_reviews)

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('student_login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)