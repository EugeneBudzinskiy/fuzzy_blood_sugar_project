import numpy as np
from matplotlib import pyplot as plt


SEED = 113
np.random.seed(seed=SEED)


# Define trapezoid membership function
def trapezoid(x, a, b, c, d):
    if a < x < b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1
    elif c < x < d:
        return (x - d) / (c - d)
    else:
        return 0


# Define input parameters with membership functions
def fuzzify_age(age):
    return {
        'young': trapezoid(age, a=0, b=0, c=30, d=45),
        'middle_aged': trapezoid(age, a=30, b=45, c=55, d=70),
        'old': trapezoid(age, a=55, b=70, c=100, d=100)
    }


def fuzzify_bmi(bmi):
    return {
        'low': trapezoid(bmi, a=10, b=10, c=18.5, d=20),
        'normal': trapezoid(bmi, a=18.5, b=20, c=25, d=30),
        'high': trapezoid(bmi, a=25, b=30, c=45, d=45),
    }


def fuzzify_activity(activity):
    return {
        'sedentary': trapezoid(activity, a=0, b=0, c=5, d=7),
        'moderate': trapezoid(activity, a=5, b=7, c=8, d=9),
        'active': trapezoid(activity, a=8, b=9, c=10, d=10)
    }


# Define output membership functions
def fuzzify_blood_sugar(blood_sugar):
    return {
        'low': trapezoid(blood_sugar, a=50, b=50, c=70, d=90),
        'normal': trapezoid(blood_sugar, a=70, b=90, c=100, d=110),
        'high': trapezoid(blood_sugar, a=100, b=110, c=200, d=200)
    }


# Define fuzzy rules
def apply_rules(age_fuzzy, bmi_fuzzy, activity_fuzzy):
    # noinspection PyListCreation
    rules = []

    # Rule 1: If age is young and BMI is normal and activity is active, then blood sugar is normal
    rules.append(('low', min(age_fuzzy['young'], bmi_fuzzy['low'], activity_fuzzy['active'])))

    # Rule 2: If age is young and BMI is high and activity is sedentary, then blood sugar is high
    rules.append(('high', min(age_fuzzy['young'], bmi_fuzzy['high'], activity_fuzzy['sedentary'])))

    # Rule 3: If age is middle-aged and BMI is normal and activity is moderate, then blood sugar is normal
    rules.append(('normal', min(age_fuzzy['middle_aged'], bmi_fuzzy['normal'], activity_fuzzy['moderate'])))

    # Rule 4: If age is middle-aged and BMI is high and activity is sedentary, then blood sugar is high
    rules.append(('high', min(age_fuzzy['middle_aged'], bmi_fuzzy['high'], activity_fuzzy['sedentary'])))

    # Rule 5: If age is old and BMI is low and activity is active, then blood sugar is normal
    rules.append(('normal', min(age_fuzzy['old'], bmi_fuzzy['low'], activity_fuzzy['active'])))

    # Rule 6: If age is old and BMI is high and activity is sedentary, then blood sugar is high
    rules.append(('high', min(age_fuzzy['old'], bmi_fuzzy['high'], activity_fuzzy['sedentary'])))

    # Rule 7: If age is young and BMI is normal and activity is sedentary, then blood sugar is normal
    rules.append(('normal', min(age_fuzzy['young'], bmi_fuzzy['normal'], activity_fuzzy['sedentary'])))

    # Rule 8: If age is old and BMI is normal and activity is moderate, then blood sugar is normal
    rules.append(('normal', min(age_fuzzy['old'], bmi_fuzzy['normal'], activity_fuzzy['moderate'])))

    # Rule 9: If age is middle-aged and BMI is low and activity is active, then blood sugar is low
    rules.append(('low', min(age_fuzzy['middle_aged'], bmi_fuzzy['low'], activity_fuzzy['active'])))

    return rules


# Defuzzification using centroid method
def defuzzify(rules, blood_sugar_levels):
    numerator = 0
    denominator = 0
    for level, weight in rules:
        if weight > 0:
            centroid = np.mean(blood_sugar_levels[level])
            numerator += weight * centroid
            denominator += weight

    return numerator / denominator if denominator != 0 else np.mean(blood_sugar_levels["low"])


# Predict blood sugar level based on inputs
def predict_blood_sugar(age_input, bmi_input, activity_input):
    # Fuzzify inputs
    age_fuzzy = fuzzify_age(age_input)
    bmi_fuzzy = fuzzify_bmi(bmi_input)
    activity_fuzzy = fuzzify_activity(activity_input)

    # Apply fuzzy rules
    rules = apply_rules(age_fuzzy, bmi_fuzzy, activity_fuzzy)

    # Define output membership function ranges
    blood_sugar_levels = {
        'low': np.arange(50, 91, 1),
        'normal': np.arange(70, 111, 1),
        'high': np.arange(100, 201, 1)
    }

    # Defuzzify the result to get a crisp value
    predicted_blood_sugar = defuzzify(rules, blood_sugar_levels)

    return predicted_blood_sugar


# Simulate input data streams
time_steps = 100
time_space = np.linspace(start=0, stop=1, num=time_steps)

ages = (80 - 10) * time_space + 10  # Age changes from 20 to 70 over time
bmis = 20 + 3 * (2 * np.random.rand(time_steps) - 1) + 6 * time_space  # BMI changes from
activities = 8 + 2 * (2 * np.random.rand(time_steps) - 1) - 2 * time_space  # Activity level changes

# Predict blood sugar levels for each time step
predicted_blood_sugars = [predict_blood_sugar(ages[t], bmis[t], activities[t]) for t in range(time_steps)]

# Plotting
plt.figure(figsize=(10, 9))

plt.subplot(4, 1, 1)
plt.plot(ages, color="tab:blue", label='Age')
plt.title('Age over Time')
plt.ylabel('Age')
plt.xticks([])
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(bmis, color="tab:orange", label='BMI')
plt.title('BMI over Time')
plt.ylabel('BMI')
plt.xticks([])
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(activities, color="tab:green", label='Activity')
plt.title('Activity Level over Time')
plt.ylabel('Activity')
plt.xticks([])
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(predicted_blood_sugars, color="tab:red", label='Blood Sugar')
plt.title('Predicted Blood Sugar over Time')
plt.xlabel('Time Steps')
plt.ylabel('Blood Sugar Level')
plt.xticks([])
plt.legend()

plt.tight_layout()
plt.show()
