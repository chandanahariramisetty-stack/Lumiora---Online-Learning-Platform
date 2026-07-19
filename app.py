from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'lumiora-secret-key-2026'

# ==================== DATA STORAGE (JSON-based) ====================
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}

def save_data(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# Initialize data files
if not os.path.exists(os.path.join(DATA_DIR, 'users.json')):
    save_data('users.json', {})
if not os.path.exists(os.path.join(DATA_DIR, 'courses.json')):
    save_data('courses.json', {
        "1": {
            "id": "1",
            "title": "Python Basics",
            "instructor": "Dr. Sarah Mitchell",
            "category": "Development",
            "level": "Beginner",
            "language": "English",
            "rating": 4.8,
            "reviews": 12500,
            "price": 0,
            "price_type": "Free",
            "image": "python",
            "description": "Master Python programming from scratch. Learn variables, data types, operators, control flow, and functions with hands-on projects.",
            "lessons": [
                {"id": 1, "title": "Introduction to Python", "duration": "15 min", "completed": False},
                {"id": 2, "title": "Variables and Data Types", "duration": "20 min", "completed": False},
                {"id": 3, "title": "Operators in Python", "duration": "18 min", "completed": False},
                {"id": 4, "title": "Control Flow - If/Else", "duration": "25 min", "completed": False},
                {"id": 5, "title": "Loops - For and While", "duration": "22 min", "completed": False}
            ],
            "quizzes": [
                {"id": 1, "title": "Python Fundamentals Quiz", "questions": [
                    {"q": "What is Python?", "options": ["A Snake", "A Programming Language", "A Database", "An OS"], "correct": 1},
                    {"q": "Which of these is a valid variable name?", "options": ["2name", "_name", "name-2", "name 2"], "correct": 1},
                    {"q": "What is the output of print(2**3)?", "options": ["6", "8", "9", "16"], "correct": 1}
                ]},
                {"id": 2, "title": "Data Types Quiz", "questions": [
                    {"q": "What is the type of [1, 2, 3]?", "options": ["Tuple", "List", "Dictionary", "Set"], "correct": 1},
                    {"q": "Which function converts a string to integer?", "options": ["str()", "int()", "float()", "bool()"], "correct": 1}
                ]}
            ]
        },
        "2": {
            "id": "2",
            "title": "Web Development",
            "instructor": "James Cooper",
            "category": "Development",
            "level": "Intermediate",
            "language": "English",
            "rating": 4.7,
            "reviews": 8300,
            "price": 49.99,
            "price_type": "Paid",
            "image": "web",
            "description": "Build modern websites with HTML5, CSS3, JavaScript, and responsive design principles. Create real-world projects.",
            "lessons": [
                {"id": 1, "title": "HTML5 Fundamentals", "duration": "20 min", "completed": False},
                {"id": 2, "title": "CSS3 Styling", "duration": "25 min", "completed": False},
                {"id": 3, "title": "JavaScript Basics", "duration": "30 min", "completed": False},
                {"id": 4, "title": "Responsive Design", "duration": "22 min", "completed": False}
            ],
            "quizzes": [
                {"id": 1, "title": "Web Dev Basics", "questions": [
                    {"q": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Mark Language", "Home Tool Markup Language"], "correct": 0}
                ]}
            ]
        },
        "3": {
            "id": "3",
            "title": "Data Science",
            "instructor": "Dr. Emily Chen",
            "category": "Data Science",
            "level": "Advanced",
            "language": "English",
            "rating": 4.9,
            "reviews": 15300,
            "price": 59.99,
            "price_type": "Paid",
            "image": "data",
            "description": "Dive into data analysis, visualization, machine learning algorithms, and statistical modeling with Python.",
            "lessons": [
                {"id": 1, "title": "Data Analysis with Pandas", "duration": "30 min", "completed": False},
                {"id": 2, "title": "Data Visualization", "duration": "25 min", "completed": False},
                {"id": 3, "title": "Machine Learning Basics", "duration": "35 min", "completed": False}
            ],
            "quizzes": [
                {"id": 1, "title": "Data Science Quiz", "questions": [
                    {"q": "Which library is used for data visualization?", "options": ["NumPy", "Pandas", "Matplotlib", "Scikit-learn"], "correct": 2}
                ]}
            ]
        },
        "4": {
            "id": "4",
            "title": "UI/UX Design",
            "instructor": "Lisa Anderson",
            "category": "Design",
            "level": "Intermediate",
            "language": "English",
            "rating": 4.6,
            "reviews": 7200,
            "price": 39.99,
            "price_type": "Paid",
            "image": "design",
            "description": "Learn user interface and user experience design principles, wireframing, prototyping, and design tools.",
            "lessons": [
                {"id": 1, "title": "Design Principles", "duration": "20 min", "completed": False},
                {"id": 2, "title": "Wireframing", "duration": "25 min", "completed": False},
                {"id": 3, "title": "Prototyping Tools", "duration": "30 min", "completed": False}
            ],
            "quizzes": [
                {"id": 1, "title": "UI/UX Quiz", "questions": [
                    {"q": "What does UX stand for?", "options": ["User Experience", "User Extension", "Universal Experience", "User Expert"], "correct": 0}
                ]}
            ]
        },
        "5": {
            "id": "5",
            "title": "Business Analytics",
            "instructor": "Robert Taylor",
            "category": "Business",
            "level": "Beginner",
            "language": "English",
            "rating": 4.5,
            "reviews": 5400,
            "price": 29.99,
            "price_type": "Paid",
            "image": "business",
            "description": "Learn business analysis, market research, financial modeling, and strategic decision making.",
            "lessons": [
                {"id": 1, "title": "Business Analysis Fundamentals", "duration": "20 min", "completed": False},
                {"id": 2, "title": "Market Research", "duration": "25 min", "completed": False}
            ],
            "quizzes": [
                {"id": 1, "title": "Business Quiz", "questions": [
                    {"q": "What is SWOT analysis?", "options": ["Strengths, Weaknesses, Opportunities, Threats", "Sales, Workflow, Operations, Team", "Strategy, Work, Output, Time", "System, Web, Online, Technology"], "correct": 0}
                ]}
            ]
        },
        "6": {
            "id": "6",
            "title": "Digital Marketing",
            "instructor": "Amanda White",
            "category": "Marketing",
            "level": "Beginner",
            "language": "English",
            "rating": 4.7,
            "reviews": 6800,
            "price": 34.99,
            "price_type": "Paid",
            "image": "marketing",
            "description": "Master SEO, social media marketing, content strategy, email marketing, and analytics.",
            "lessons": [
                {"id": 1, "title": "SEO Fundamentals", "duration": "20 min", "completed": False},
                {"id": 2, "title": "Social Media Strategy", "duration": "25 min", "completed": False}
            ],
            "quizzes": [
                {"id": 1, "title": "Marketing Quiz", "questions": [
                    {"q": "What does SEO stand for?", "options": ["Search Engine Optimization", "Social Engagement Online", "Sales Enhancement Operation", "System Engine Output"], "correct": 0}
                ]}
            ]
        }
    })
if not os.path.exists(os.path.join(DATA_DIR, 'enrollments.json')):
    save_data('enrollments.json', {})
if not os.path.exists(os.path.join(DATA_DIR, 'progress.json')):
    save_data('progress.json', {})
if not os.path.exists(os.path.join(DATA_DIR, 'certificates.json')):
    save_data('certificates.json', {})

# ==================== AUTH DECORATORS ====================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        users = load_data('users.json')
        user = users.get(session['user_id'])
        if not user or user.get('role') != 'Student':
            flash('Access denied. Students only.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def instructor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        users = load_data('users.json')
        user = users.get(session['user_id'])
        if not user or user.get('role') != 'Instructor':
            flash('Access denied. Instructors only.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== HELPER FUNCTIONS ====================
def get_user_progress(user_id, course_id):
    progress = load_data('progress.json')
    key = f"{user_id}_{course_id}"
    return progress.get(key, {
        'completed_lessons': [],
        'completed_quizzes': [],
        'quiz_scores': {},
        'overall_progress': 0
    })

def update_progress(user_id, course_id, lesson_id=None, quiz_id=None, score=None):
    progress = load_data('progress.json')
    key = f"{user_id}_{course_id}"
    if key not in progress:
        progress[key] = {
            'completed_lessons': [],
            'completed_quizzes': [],
            'quiz_scores': {},
            'overall_progress': 0
        }

    if lesson_id and lesson_id not in progress[key]['completed_lessons']:
        progress[key]['completed_lessons'].append(lesson_id)

    if quiz_id:
        if quiz_id not in progress[key]['completed_quizzes']:
            progress[key]['completed_quizzes'].append(quiz_id)
        if score is not None:
            progress[key]['quiz_scores'][str(quiz_id)] = score

    # Calculate overall progress
    courses = load_data('courses.json')
    course = courses.get(course_id)
    if course:
        total_items = len(course.get('lessons', [])) + len(course.get('quizzes', []))
        completed_items = len(progress[key]['completed_lessons']) + len(progress[key]['completed_quizzes'])
        progress[key]['overall_progress'] = round((completed_items / total_items) * 100) if total_items > 0 else 0

    save_data('progress.json', progress)
    return progress[key]

def check_certificate_eligible(user_id, course_id):
    progress = get_user_progress(user_id, course_id)
    courses = load_data('courses.json')
    course = courses.get(course_id)
    if not course:
        return False
    total_lessons = len(course.get('lessons', []))
    total_quizzes = len(course.get('quizzes', []))
    return (len(progress['completed_lessons']) >= total_lessons and 
            len(progress['completed_quizzes']) >= total_quizzes)

def generate_certificate(user_id, course_id):
    certificates = load_data('certificates.json')
    cert_id = f"CERT-{user_id}-{course_id}-{datetime.now().strftime('%Y%m%d')}"
    users = load_data('users.json')
    courses = load_data('courses.json')

    certificate = {
        'id': cert_id,
        'user_id': user_id,
        'user_name': users.get(user_id, {}).get('full_name', 'Unknown'),
        'course_id': course_id,
        'course_name': courses.get(course_id, {}).get('title', 'Unknown'),
        'date': datetime.now().strftime('%B %d, %Y'),
        'status': 'completed'
    }

    certificates[cert_id] = certificate
    save_data('certificates.json', certificates)
    return certificate

# ==================== ROUTES ====================
@app.route('/')
def home():
    courses = load_data('courses.json')
    categories = {}
    for course in courses.values():
        cat = course.get('category', 'Other')
        if cat not in categories:
            categories[cat] = {'count': 0, 'courses': []}
        categories[cat]['count'] += 1
        categories[cat]['courses'].append(course)

    stats = {
        'courses': len(courses),
        'students': sum(1 for u in load_data('users.json').values() if u.get('role') == 'Student'),
        'instructors': sum(1 for u in load_data('users.json').values() if u.get('role') == 'Instructor'),
        'countries': 60
    }

    return render_template('index.html', courses=courses, categories=categories, stats=stats)

@app.route('/courses')
def browse_courses():
    courses = load_data('courses.json')
    category = request.args.get('category', '')
    level = request.args.get('level', '')
    language = request.args.get('language', '')
    sort = request.args.get('sort', '')
    search = request.args.get('search', '').lower()

    filtered = dict(courses)

    if search:
        filtered = {k: v for k, v in filtered.items() if search in v['title'].lower() or search in v['description'].lower()}
    if category:
        filtered = {k: v for k, v in filtered.items() if v['category'] == category}
    if level:
        filtered = {k: v for k, v in filtered.items() if v['level'] == level}
    if language:
        filtered = {k: v for k, v in filtered.items() if v['language'] == language}

    if sort == 'rating':
        filtered = dict(sorted(filtered.items(), key=lambda x: x[1]['rating'], reverse=True))
    elif sort == 'price_low':
        filtered = dict(sorted(filtered.items(), key=lambda x: x[1]['price']))
    elif sort == 'price_high':
        filtered = dict(sorted(filtered.items(), key=lambda x: x[1]['price'], reverse=True))

    categories = list(set(c['category'] for c in courses.values()))
    levels = list(set(c['level'] for c in courses.values()))
    languages = list(set(c['language'] for c in courses.values()))

    return render_template('courses.html', courses=filtered, categories=categories, 
                         levels=levels, languages=languages, 
                         selected_category=category, selected_level=level, 
                         selected_language=language, selected_sort=sort, search=search)

@app.route('/course/<course_id>')
def course_details(course_id):
    courses = load_data('courses.json')
    course = courses.get(course_id)
    if not course:
        flash('Course not found', 'danger')
        return redirect(url_for('browse_courses'))

    enrolled = False
    user_progress = None
    if 'user_id' in session:
        enrollments = load_data('enrollments.json')
        enrolled = course_id in enrollments.get(session['user_id'], [])
        if enrolled:
            user_progress = get_user_progress(session['user_id'], course_id)

    return render_template('course_details.html', course=course, enrolled=enrolled, progress=user_progress)

@app.route('/enroll/<course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    courses = load_data('courses.json')
    if course_id not in courses:
        flash('Course not found', 'danger')
        return redirect(url_for('browse_courses'))

    enrollments = load_data('enrollments.json')
    user_id = session['user_id']

    if user_id not in enrollments:
        enrollments[user_id] = []

    if course_id not in enrollments[user_id]:
        enrollments[user_id].append(course_id)
        save_data('enrollments.json', enrollments)
        flash('Successfully enrolled in the course!', 'success')
    else:
        flash('You are already enrolled in this course', 'info')

    return redirect(url_for('course_details', course_id=course_id))

@app.route('/lesson/<course_id>/<int:lesson_id>')
@student_required
def lesson(course_id, lesson_id):
    courses = load_data('courses.json')
    course = courses.get(course_id)
    if not course:
        flash('Course not found', 'danger')
        return redirect(url_for('browse_courses'))

    enrollments = load_data('enrollments.json')
    if course_id not in enrollments.get(session['user_id'], []):
        flash('Please enroll in this course first', 'warning')
        return redirect(url_for('course_details', course_id=course_id))

    lesson = None
    for l in course.get('lessons', []):
        if l['id'] == lesson_id:
            lesson = l
            break

    if not lesson:
        flash('Lesson not found', 'danger')
        return redirect(url_for('course_details', course_id=course_id))

    # Mark lesson as complete
    update_progress(session['user_id'], course_id, lesson_id=lesson_id)

    progress = get_user_progress(session['user_id'], course_id)

    return render_template('lesson.html', course=course, lesson=lesson, progress=progress)

@app.route('/quiz/<course_id>/<int:quiz_id>', methods=['GET', 'POST'])
@student_required
def quiz(course_id, quiz_id):
    courses = load_data('courses.json')
    course = courses.get(course_id)
    if not course:
        flash('Course not found', 'danger')
        return redirect(url_for('browse_courses'))

    enrollments = load_data('enrollments.json')
    if course_id not in enrollments.get(session['user_id'], []):
        flash('Please enroll in this course first', 'warning')
        return redirect(url_for('course_details', course_id=course_id))

    quiz = None
    for q in course.get('quizzes', []):
        if q['id'] == quiz_id:
            quiz = q
            break

    if not quiz:
        flash('Quiz not found', 'danger')
        return redirect(url_for('course_details', course_id=course_id))

    if request.method == 'POST':
        answers = request.form.getlist('answer')
        score = 0
        total = len(quiz['questions'])

        for i, question in enumerate(quiz['questions']):
            if i < len(answers) and int(answers[i]) == question['correct']:
                score += 1

        percentage = round((score / total) * 100) if total > 0 else 0
        update_progress(session['user_id'], course_id, quiz_id=quiz_id, score=percentage)

        # Check if certificate eligible
        if check_certificate_eligible(session['user_id'], course_id):
            cert = generate_certificate(session['user_id'], course_id)
            flash(f'Congratulations! You earned a certificate: {cert["id"]}', 'success')

        return render_template('quiz_result.html', course=course, quiz=quiz, 
                             score=score, total=total, percentage=percentage)

    progress = get_user_progress(session['user_id'], course_id)
    return render_template('quiz.html', course=course, quiz=quiz, progress=progress)

@app.route('/dashboard')
@login_required
def dashboard():
    users = load_data('users.json')
    courses = load_data('courses.json')
    enrollments = load_data('enrollments.json')
    certificates = load_data('certificates.json')

    user = users.get(session['user_id'])
    user_courses = []
    user_certificates = []

    if user and user.get('role') == 'Student':
        enrolled_ids = enrollments.get(session['user_id'], [])
        for cid in enrolled_ids:
            if cid in courses:
                course = courses[cid].copy()
                progress = get_user_progress(session['user_id'], cid)
                course['progress'] = progress['overall_progress']
                user_courses.append(course)

        for cert in certificates.values():
            if cert['user_id'] == session['user_id']:
                user_certificates.append(cert)

    return render_template('dashboard.html', user=user, courses=user_courses, certificates=user_certificates)

@app.route('/progress')
@student_required
def progress():
    users = load_data('users.json')
    courses = load_data('courses.json')
    enrollments = load_data('enrollments.json')

    user_courses = []
    enrolled_ids = enrollments.get(session['user_id'], [])
    total_progress = 0

    for cid in enrolled_ids:
        if cid in courses:
            course = courses[cid].copy()
            progress = get_user_progress(session['user_id'], cid)
            course['progress'] = progress['overall_progress']
            course['completed_lessons'] = len(progress['completed_lessons'])
            course['total_lessons'] = len(course.get('lessons', []))
            course['completed_quizzes'] = len(progress['completed_quizzes'])
            course['total_quizzes'] = len(course.get('quizzes', []))
            user_courses.append(course)
            total_progress += progress['overall_progress']

    avg_progress = round(total_progress / len(user_courses)) if user_courses else 0

    return render_template('progress.html', courses=user_courses, avg_progress=avg_progress)

@app.route('/certificates')
@student_required
def certificates():
    certificates_data = load_data('certificates.json')
    user_certs = [c for c in certificates_data.values() if c['user_id'] == session['user_id']]
    return render_template('certificates.html', certificates=user_certs)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    users = load_data('users.json')
    user = users.get(session['user_id'])

    if request.method == 'POST':
        user['full_name'] = request.form.get('full_name', user['full_name'])
        user['email'] = request.form.get('email', user['email'])
        if request.form.get('password'):
            user['password'] = generate_password_hash(request.form.get('password'))
        users[session['user_id']] = user
        save_data('users.json', users)
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        users = load_data('users.json')
        user = None
        user_id = None

        for uid, u in users.items():
            if u['email'] == email:
                user = u
                user_id = uid
                break

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user_id
            session['user_name'] = user['full_name']
            session['user_role'] = user['role']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'Student')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')

        users = load_data('users.json')

        for u in users.values():
            if u['email'] == email:
                flash('Email already registered', 'danger')
                return render_template('register.html')

        user_id = f"user_{len(users) + 1}"
        users[user_id] = {
            'id': user_id,
            'full_name': full_name,
            'email': email,
            'password': generate_password_hash(password),
            'role': role,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        save_data('users.json', users)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/instructor/dashboard')
@instructor_required
def instructor_dashboard():
    users = load_data('users.json')
    courses = load_data('courses.json')
    enrollments = load_data('enrollments.json')

    # Get courses created by this instructor (simplified - in real app, filter by instructor_id)
    my_courses = [c for c in courses.values() if c['instructor'] == users.get(session['user_id'], {}).get('full_name')]

    total_students = 0
    for course in my_courses:
        for uid, enrolled in enrollments.items():
            if course['id'] in enrolled:
                total_students += 1

    return render_template('instructor_dashboard.html', courses=my_courses, total_students=total_students)

# ==================== API ENDPOINTS ====================
@app.route('/api/mark-lesson-complete', methods=['POST'])
@student_required
def mark_lesson_complete():
    data = request.get_json()
    course_id = data.get('course_id')
    lesson_id = data.get('lesson_id')

    update_progress(session['user_id'], course_id, lesson_id=lesson_id)
    progress = get_user_progress(session['user_id'], course_id)

    return jsonify({'success': True, 'progress': progress['overall_progress']})

@app.route('/api/search-courses')
def search_courses():
    query = request.args.get('q', '').lower()
    courses = load_data('courses.json')
    results = [c for c in courses.values() if query in c['title'].lower() or query in c['description'].lower()]
    return jsonify({'courses': results[:5]})

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)