from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from website_folder.forms import RegistrationForm, LoginForm, UpdateAccountForm
from website_folder import app, db, bcrypt
from website_folder.models import User, CalculationResult
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from flask_bcrypt import Bcrypt
from website_folder.python.ARM.bicep import bicep_exercise
from website_folder.python.BACK.pullups import pullup_exercise
from website_folder.python.CARDIO.jumping_jack import jumping_jack_exercise
from website_folder.python.CHEST.bench_press import bench_press_exercise
from website_folder.python.CHEST.pushup import pushup_exercise
from website_folder.python.CORE.crunches import crunches_exercise
from website_folder.python.CORE.plank import plank_exercise
from website_folder.python.LEG.leg_raise import leg_raise_exercise
from website_folder.python.LEG.lunges import lunges_exercise
from website_folder.python.LEG.Squat import squat_exercise
from website_folder.python.SHOULDER.lateral_raise import lateral_raise_exercise
from website_folder.python.SHOULDER.shoulder_press import shoulder_press_exercise
from website_folder.Calculator.calci import calculate_bmi, calculate_bmr, calculate_ideal_weight, calculate_body_fat, calculate_lean_body_mass, calculate_waist_to_hip_ratio, calculate_waist_to_height_ratio, calculate_protein_intake, calculate_calorie_intake, calculate_fat_intake, calculate_carbohydrate_intake, calculate_water_intake, calculate_tdee



@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template('home.html')

@app.route("/about")
@login_required
def about():
    return render_template('about.html', title='About')

@app.route("/basebot")
@login_required
def basebot():
    return render_template('basebot.html', title='Chatbots')

@app.route("/exercise")
@login_required
def exercise():
    return render_template('exercise.html', title='Exercise')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:  # If user exists
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Incorrect password.', 'danger')
        else:
            flash('Login Unsuccessful. User does not exist.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@app.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():
    if request.method == 'POST':
        from website_folder.fitbot_module.chatbot import predict_class, get_response, intents_data
        user_input = request.get_json()['userInput']
        ints = predict_class(user_input)
        response = get_response(ints, intents_data)
        return jsonify({'response': response})
    return render_template('chatbot.html')

@app.route('/melobot', methods=['GET', 'POST'])
@login_required
def melobot():
    if request.method == 'POST':
        from website_folder.melobot_module.chat import predict_class, get_response, intents_data
        user_input = request.get_json()['userInput']
        ints = predict_class(user_input)
        response = get_response(ints, intents_data)
        return jsonify({'response': response})
    return render_template('melobot.html')

@app.route("/bicep-exercise", methods=["GET", "POST"])
@login_required
def bicep_exercise_route():
    if request.method == "POST":
        num_reps = int(request.form.get("num_reps", 0))
        if num_reps > 0:
            bicep_exercise(num_reps)
        else:
            flash("Please enter a valid number of reps.", "error")
    return render_template("exercise.html") 

@app.route("/pullup-exercise", methods=["GET", "POST"])
@login_required
def pullup_exercise_route():
    if request.method == "POST":
        num_reps = int(request.form.get("num_reps", 0))
        if num_reps > 0:
            pullup_exercise(num_reps)
        else:
            flash("Please enter a valid number of reps.", "error")
    return render_template("exercise.html")

@app.route("/jumping-jack-exercise", methods=["GET", "POST"])
@login_required
def jumping_jack_exercise_route():
    if request.method == "POST":
        num_reps = int(request.form.get("num_reps", 0))
        if num_reps > 0:
            jumping_jack_exercise(num_reps)
        else:
            flash("Please enter a valid number of reps.", "error")
    return render_template("exercise.html")

@app.route("/bench-press-exercise", methods=["GET", "POST"])
@login_required
def bench_press_exercise_route():
    if request.method == "POST":
        num_reps = int(request.form.get("num_reps", 0))
        if num_reps > 0:
            bench_press_exercise(num_reps)
        else:
            flash("Please enter a valid number of reps.", "error")
    return render_template("exercise.html")

@app.route("/pushup-exercise", methods=["GET", "POST"])
@login_required
def pushup_exercise_route():
    if request.method == "POST":
        num_reps = int(request.form.get("num_reps", 0))
        if num_reps > 0:
            pushup_exercise(num_reps)
        else:
            flash("Please enter a valid number of reps.", "error")
    return render_template("exercise.html")

@app.route("/crunches-exercise", methods=["GET", "POST"])
@login_required
def crunches_exercise_route():
    if request.method == "POST":
        num_reps = int(request.form.get("num_reps", 0))
        if num_reps > 0:
            crunches_exercise(num_reps)
        else:
            flash("Please enter a valid number of reps.", "error")
    return render_template("exercise.html")

@app.route("/plank-exercise", methods=["GET", "POST"])
@login_required
def plank_exercise_route():
    if request.method == "POST":
        num_reps = int(request.form.get("num_reps", 0))
        if num_reps > 0:
            plank_exercise(num_reps)
        else:
            flash("Please enter a valid number of reps.", "error")
    return render_template("exercise.html")

@app.route("/leg-raise-exercise", methods=["GET", "POST"])
@login_required
def leg_raise_exercise_route():
    if request.method == "POST":
        num_reps = int(request.form.get("num_reps", 0))
        if num_reps > 0:
            leg_raise_exercise(num_reps)
        else:
            flash("Please enter a valid number of reps.", "error")
    return render_template("exercise.html")

@app.route("/lunges-exercise", methods=["GET", "POST"])
@login_required
def lunges_exercise_route():
    if request.method == "POST":
        num_reps = int(request.form.get("num_reps", 0))
        if num_reps > 0:
            lunges_exercise(num_reps)
        else:
            flash("Please enter a valid number of reps.", "error")
    return render_template("exercise.html")

@app.route("/squat-exercise", methods=["GET", "POST"])
@login_required
def squat_exercise_route():
    if request.method == "POST":
        num_reps = int(request.form.get("num_reps", 0))
        if num_reps > 0:
            squat_exercise(num_reps)
        else:
            flash("Please enter a valid number of reps.", "error")
    return render_template("exercise.html")

@app.route("/lateral-raise-exercise", methods=["GET", "POST"])
@login_required
def lateral_raise_exercise_route():
    if request.method == "POST":
        num_reps = int(request.form.get("num_reps", 0))
        if num_reps > 0:
            lateral_raise_exercise(num_reps)
        else:
            flash("Please enter a valid number of reps.", "error")
    return render_template("exercise.html")

@app.route("/shoulder-press-exercise", methods=["GET", "POST"])
@login_required
def shoulder_press_exercise_route():
    if request.method == "POST":
        num_reps = int(request.form.get("num_reps", 0))
        if num_reps > 0:
            shoulder_press_exercise(num_reps)
        else:
            flash("Please enter a valid number of reps.", "error")
    return render_template("exercise.html")

@app.route('/calculate', methods=['GET', 'POST'])
@login_required
def calculate():
    if request.method == 'POST':
        # Retrieve form data
        weight_kg = float(request.form.get('weight', 0))
        height_cm = float(request.form.get('height', 0))
        age = int(request.form.get('age', 0))
        gender = request.form.get('gender', '')
        waist_circumference_cm = float(request.form.get('waist_circumference', 0))
        hip_circumference_cm = float(request.form.get('hip_circumference', 0))
        activity_level = request.form.get('activity_level', '')
        fitness_goal = request.form.get('fitness_goal', '')
        weight_goal = request.form.get('weight_goal', '')
        dietary_preference = request.form.get('dietary_preference', '')
        climate = request.form.get('climate', '')

        
        # Perform calculations
        bmi = calculate_bmi(weight_kg, height_cm)
        bmr = calculate_bmr(weight_kg, height_cm, age, gender)
        ideal_weight = calculate_ideal_weight(height_cm, gender)
        body_fat_percentage = calculate_body_fat(bmi, age, gender)
        lean_body_mass = calculate_lean_body_mass(weight_kg, body_fat_percentage)
        waist_to_hip_ratio = calculate_waist_to_hip_ratio(waist_circumference_cm, hip_circumference_cm)
        waist_to_height_ratio = calculate_waist_to_height_ratio(waist_circumference_cm, height_cm)
        protein_intake = calculate_protein_intake(weight_kg, activity_level, fitness_goal)
        calorie_intake = calculate_calorie_intake(weight_kg, height_cm, age, gender, activity_level, weight_goal)
        fat_intake = calculate_fat_intake(weight_kg, activity_level, dietary_preference)
        carbohydrate_intake = calculate_carbohydrate_intake(weight_kg, activity_level, weight_goal)
        water_intake = calculate_water_intake(weight_kg, activity_level, climate)
        tdee = calculate_tdee(weight_kg, height_cm, age, gender, activity_level)

        calculation_result = CalculationResult.query.filter_by(user=current_user).first()

        if calculation_result:
            calculation_result.bmi = bmi
            calculation_result.bmr = bmr
            calculation_result.ideal_weight = ideal_weight
            calculation_result.body_fat_percentage = body_fat_percentage
            calculation_result.lean_body_mass = lean_body_mass
            calculation_result.waist_to_hip_ratio = waist_to_hip_ratio
            calculation_result.waist_to_height_ratio = waist_to_height_ratio
            calculation_result.protein_intake = protein_intake
            calculation_result.calorie_intake = calorie_intake
            calculation_result.fat_intake = fat_intake
            calculation_result.carbohydrate_intake = carbohydrate_intake
            calculation_result.water_intake = water_intake
            calculation_result.tdee = tdee

        else:      
            calculation_result = CalculationResult(
                bmi=bmi,
                bmr=bmr,
                ideal_weight=ideal_weight,
                body_fat_percentage=body_fat_percentage,
                lean_body_mass=lean_body_mass,
                waist_to_hip_ratio=waist_to_hip_ratio,
                waist_to_height_ratio=waist_to_height_ratio,
                protein_intake=protein_intake,
                calorie_intake=calorie_intake,
                fat_intake=fat_intake,
                carbohydrate_intake=carbohydrate_intake,
                water_intake=water_intake,
                tdee=tdee,
                user=current_user
            )
        db.session.add(calculation_result)
        db.session.commit()

        # Render the template with the calculated results
        return render_template('calculate.html', bmi=bmi, bmr=bmr, ideal_weight=ideal_weight, body_fat_percentage=body_fat_percentage, lean_body_mass=lean_body_mass, waist_to_hip_ratio=waist_to_hip_ratio, waist_to_height_ratio=waist_to_height_ratio, protein_intake=protein_intake, calorie_intake=calorie_intake, fat_intake=fat_intake, carbohydrate_intake=carbohydrate_intake, water_intake=water_intake, tdee=tdee)

    # Render the form template for GET requests
    return render_template('calculateform.html')

@app.route('/calculatorform', methods=['GET'])
@login_required
def calculatorform():
    return render_template('calculatorform.html')

