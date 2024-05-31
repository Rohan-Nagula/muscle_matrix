import math

def calculate_bmi(weight, height):
    """
    Calculate BMI (Body Mass Index) using weight in kilograms and height in centimeters.
    Formula: BMI = weight (kg) / (height (m) ^ 2)
    """
    height_meters = height / 100  # Convert height from centimeters to meters
    bmi = weight / (height_meters ** 2)
    return round(bmi, 4)

def calculate_bmr(weight, height, age, gender):
    """
    Calculate BMR (Basal Metabolic Rate) using weight in kilograms, height in centimeters, age in years, and gender.
    The Harris-Benedict equation is used for BMR calculation.
    """
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender.lower() == 'female':
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError("Gender should be 'male' or 'female'.")
    return round(bmr, 4)

def calculate_ideal_weight(height, gender):
    """
    Calculate ideal weight using the Devine formula.
    For males: Ideal weight (kg) = 50 + 0.9 * (height (cm) - 152)
    For females: Ideal weight (kg) = 45.5 + 0.9 * (height (cm) - 152)
    """
    if gender.lower() == 'male':
        ideal_weight = 50 + 0.9 * (height - 152)
    elif gender.lower() == 'female':
        ideal_weight = 45.5 + 0.9 * (height - 152)
    else:
        raise ValueError("Gender should be 'male' or 'female'.")
    return round(ideal_weight, 4)

def calculate_body_fat(bmi, age, gender):
    """
    Calculate body fat percentage using BMI, age, and gender.
    The formula used here is based on the BMI and gender.
    """
    if gender.lower() == 'male':
        body_fat = 1.20 * bmi + 0.23 * age - 16.2
    elif gender.lower() == 'female':
        body_fat = 1.20 * bmi + 0.23 * age - 5.4
    else:
        raise ValueError("Gender should be 'male' or 'female'.")
    return round(body_fat, 4)

def calculate_lean_body_mass(weight, body_fat_percentage):
    """
    Calculate lean body mass using weight in kilograms and body fat percentage.
    """
    lean_body_mass = weight * (1 - body_fat_percentage / 100)
    return round(lean_body_mass, 4)

def calculate_protein_intake(weight, activity_level, fitness_goal):
    """
    Calculate protein intake recommendation based on weight, activity level, and fitness goal.
    """
    if activity_level.lower() == 'sedentary':
        activity_factor = 0.8
    elif activity_level.lower() == 'lightly active':
        activity_factor = 1.0
    elif activity_level.lower() == 'moderately active':
        activity_factor = 1.2
    elif activity_level.lower() == 'very active':
        activity_factor = 1.4
    else:
        raise ValueError("Activity level should be one of: sedentary, lightly active, moderately active, very active.")

    if fitness_goal.lower() == 'maintenance':
        protein_intake = 1.2 * weight * activity_factor
    elif fitness_goal.lower() == 'muscle gain':
        protein_intake = 1.6 * weight * activity_factor
    elif fitness_goal.lower() == 'fat loss':
        protein_intake = 1.0 * weight * activity_factor
    else:
        raise ValueError("Fitness goal should be one of: maintenance, muscle gain, fat loss.")

    return round(protein_intake, 4)

def calculate_calorie_intake(weight, height, age, gender, activity_level, weight_goal):
    """
    Calculate daily calorie intake recommendation based on weight, height, age, gender, activity level, and weight goal.
    """
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Gender should be 'male' or 'female'.")

    if activity_level.lower() == 'sedentary':
        activity_factor = 1.2
    elif activity_level.lower() == 'lightly active':
        activity_factor = 1.375
    elif activity_level.lower() == 'moderately active':
        activity_factor = 1.55
    elif activity_level.lower() == 'very active':
        activity_factor = 1.725
    else:
        raise ValueError("Activity level should be one of: sedentary, lightly active, moderately active, very active.")

    if weight_goal.lower() == 'maintenance':
        calorie_intake = bmr * activity_factor
    elif weight_goal.lower() == 'weight loss':
        calorie_intake = bmr * activity_factor - 500
    elif weight_goal.lower() == 'weight gain':
        calorie_intake = bmr * activity_factor + 500
    else:
        raise ValueError("Weight goal should be one of: maintenance, weight loss, weight gain.")

    return round(calorie_intake, 4)

def calculate_fat_intake(weight, activity_level, dietary_preference):
    """
    Calculate daily fat intake recommendation based on weight, activity level, and dietary preference.
    """
    if activity_level.lower() == 'sedentary':
        activity_factor = 0.8
    elif activity_level.lower() == 'lightly active':
        activity_factor = 1.0
    elif activity_level.lower() == 'moderately active':
        activity_factor = 1.2
    elif activity_level.lower() == 'very active':
        activity_factor = 1.4
    else:
        raise ValueError("Activity level should be one of: sedentary, lightly active, moderately active, very active.")

    if dietary_preference.lower() == 'balanced':
        fat_intake = 0.25 * weight * activity_factor
    elif dietary_preference.lower() == 'low fat':
        fat_intake = 0.2 * weight * activity_factor
    elif dietary_preference.lower() == 'high fat':
        fat_intake = 0.3 * weight * activity_factor
    else:
        raise ValueError("Dietary preference should be one of: balanced, low fat, high fat.")

    return round(fat_intake, 4)

def calculate_carbohydrate_intake(weight, activity_level, dietary_goal):
    """
    Calculate daily carbohydrate intake recommendation based on weight, activity level, and dietary goal.
    """
    if activity_level.lower() == 'sedentary':
        activity_factor = 0.8
    elif activity_level.lower() == 'lightly active':
        activity_factor = 1.0
    elif activity_level.lower() == 'moderately active':
        activity_factor = 1.2
    elif activity_level.lower() == 'very active':
        activity_factor = 1.4
    else:
        raise ValueError("Activity level should be one of: sedentary, lightly active, moderately active, very active.")

    if dietary_goal.lower() == 'maintenance':
        carbohydrate_intake = 3.0 * weight * activity_factor
    elif dietary_goal.lower() == 'weight loss':
        carbohydrate_intake = 2.0 * weight * activity_factor
    elif dietary_goal.lower() == 'weight gain':
        carbohydrate_intake = 4.0 * weight * activity_factor
    else:
        raise ValueError("Dietary goal should be one of: maintenance, weight loss, weight gain.")

    return round(carbohydrate_intake, 4)

def calculate_water_intake(weight, activity_level, climate):
    """
    Calculate daily water intake recommendation based on weight, activity level, and climate.
    """
    if activity_level.lower() == 'sedentary':
        activity_factor = 30
    elif activity_level.lower() == 'lightly active':
        activity_factor = 35
    elif activity_level.lower() == 'moderately active':
        activity_factor = 40
    elif activity_level.lower() == 'very active':
        activity_factor = 45
    else:
        raise ValueError("Activity level should be one of: sedentary, lightly active, moderately active, very active.")

    if climate.lower() == 'hot':
        climate_factor = 0.03
    elif climate.lower() == 'moderate':
        climate_factor = 0.02
    elif climate.lower() == 'cold':
        climate_factor = 0.01
    else:
        raise ValueError("Climate should be one of: hot, moderate, cold.")

    water_intake = weight * activity_factor + climate_factor * weight

    return round(water_intake, 4)

def calculate_tdee(weight, height, age, gender, activity_level):
    """
    Calculate Total Daily Energy Expenditure (TDEE) based on weight, height, age, gender, and activity level.
    """
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Gender should be 'male' or 'female'.")

    if activity_level.lower() == 'sedentary':
        activity_factor = 1.2
    elif activity_level.lower() == 'lightly active':
        activity_factor = 1.375
    elif activity_level.lower() == 'moderately active':
        activity_factor = 1.55
    elif activity_level.lower() == 'very active':
        activity_factor = 1.725
    else:
        raise ValueError("Activity level should be one of: sedentary, lightly active, moderately active, very active.")

    tdee = bmr * activity_factor

    return round(tdee, 4)

def calculate_waist_to_hip_ratio(waist_circumference, hip_circumference):
    """
    Calculate waist-to-hip ratio using waist circumference and hip circumference.
    Formula: Waist-to-Hip Ratio = waist circumference / hip circumference
    """
    if hip_circumference == 0:
        raise ValueError("Hip circumference cannot be zero.")
    ratio = waist_circumference / hip_circumference
    return round(ratio, 4)

def calculate_waist_to_height_ratio(waist_circumference, height):
    """
    Calculate waist-to-height ratio using waist circumference and height.
    Formula: Waist-to-Height Ratio = waist circumference / height
    """
    if height == 0:
        raise ValueError("Height cannot be zero.")
    ratio = waist_circumference / height
    return round(ratio, 4)

'''
height_cm = 183
weight_kg = 79
age = 22
gender = 'male'
waist_circumference_cm = 80
hip_circumference_cm = 85
activity_level = 'very active'
fitness_goal = 'maintenance'
weight_goal = 'maintenance'
dietary_preference = 'balanced'
climate = 'moderate'

print()

bmi = calculate_bmi(weight_kg, height_cm)
print("Your BMI is:", bmi)

bmr = calculate_bmr(weight_kg, height_cm, age, gender)
print("Your BMR is:", bmr, "calories per day.")

ideal_weight = calculate_ideal_weight(height_cm, gender)
print("Your ideal body weight range is:", ideal_weight - 10 , "kg to", ideal_weight + 10, "kg.")

body_fat_percentage = calculate_body_fat(bmi, age, gender)
print("Your estimated body fat percentage is:", body_fat_percentage, "%.")

lean_body_mass = calculate_lean_body_mass(weight_kg, body_fat_percentage)
print("Your lean body mass is:", lean_body_mass, "kilograms.")

waist_to_hip_ratio = calculate_waist_to_hip_ratio(waist_circumference_cm, hip_circumference_cm)
print("Your waist-to-hip ratio is:", waist_to_hip_ratio)    

waist_to_height_ratio = calculate_waist_to_height_ratio(waist_circumference_cm, height_cm)
print("Your waist-to-height ratio is:", waist_to_height_ratio)

print()

protein_intake = calculate_protein_intake(weight_kg, activity_level, fitness_goal)
print("Your recommended daily protein intake is:", protein_intake, "grams.")

calorie_intake = calculate_calorie_intake(weight_kg, height_cm, age, gender, activity_level, weight_goal)
print("Your recommended daily calorie intake is:", calorie_intake, "calories.")

fat_intake = calculate_fat_intake(weight_kg, activity_level, dietary_preference)
print("Your recommended daily fat intake is:", fat_intake, "grams.")

carbohydrate_intake = calculate_carbohydrate_intake(weight_kg, activity_level, weight_goal)
print("Your recommended daily carbohydrate intake is:", carbohydrate_intake, "grams.")

water_intake = calculate_water_intake(weight_kg, activity_level, climate)
print("Your recommended daily water intake is:", water_intake, "milliliters.")

tdee = calculate_tdee(weight_kg, height_cm, age, gender, activity_level)
print("Your Total Daily Energy Expenditure (TDEE) is:", tdee, "calories.")
'''

