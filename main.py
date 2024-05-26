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
        'high': trapezoid(blood_sugar, a=100, b=110, c=160, d=160)
    }


# Define fuzzy rules
def apply_rules(age_fuzzy, bmi_fuzzy, activity_fuzzy):
    # noinspection PyListCreation
    rules = []

    # Rule 1: If age is young OR BMI is low, then blood sugar is low
    rules.append(('low', max(age_fuzzy['young'], bmi_fuzzy['low'])))  # OR operation

    # Rule 2: If age is middle-aged AND activity is moderate, then blood sugar is normal
    rules.append(('normal', min(age_fuzzy['middle_aged'], activity_fuzzy['moderate'])))  # AND operation

    # Rule 3: If age is old AND BMI is high, then blood sugar is high
    rules.append(('high', min(age_fuzzy['old'], bmi_fuzzy['high'])))  # AND operation

    # Rule 4: If BMI is high OR activity is sedentary, then blood sugar is high
    rules.append(('high', max(bmi_fuzzy['high'], activity_fuzzy['sedentary'])))  # OR operation

    # Rule 5: If age is young AND activity is active, then blood sugar is low
    rules.append(('low', min(age_fuzzy['young'], activity_fuzzy['active'])))  # AND operation

    return rules


# Defuzzification using "Height Defuzzification"
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
        'high': np.arange(100, 161, 1)
    }

    # Defuzzify the result to get a crisp value
    predicted_blood_sugar = defuzzify(rules, blood_sugar_levels)

    return predicted_blood_sugar


def vectorize_fuzzy_output(lin_space, fuzzyfi_func):
    result = {}
    for x in lin_space:
        fuzzy_age = fuzzyfi_func(x)
        for fuzzy_name in fuzzy_age.keys():
            if fuzzy_name not in result:
                result[fuzzy_name] = []
            result[fuzzy_name].append(fuzzy_age[fuzzy_name])

    for fuzzy_name, value in result.items():
        result[fuzzy_name] = np.array(value)
    return result


def draw_input_fuzzy_variable():
    age_space = np.linspace(start=0, stop=100, num=1000)
    bmi_space = np.linspace(start=10, stop=45, num=1000)
    activity_space = np.linspace(start=0, stop=10, num=1000)
    sugar_space = np.linspace(start=50, stop=160, num=1000)

    age_plot_values = vectorize_fuzzy_output(lin_space=age_space, fuzzyfi_func=fuzzify_age)
    bmi_plot_values = vectorize_fuzzy_output(lin_space=bmi_space, fuzzyfi_func=fuzzify_bmi)
    activity_plot_values = vectorize_fuzzy_output(lin_space=activity_space, fuzzyfi_func=fuzzify_activity)
    sugar_plot_values = vectorize_fuzzy_output(lin_space=sugar_space, fuzzyfi_func=fuzzify_blood_sugar)

    plt.figure(figsize=(10, 9))

    plt.subplot(4, 1, 1)
    plt.title('Fuzzy Age')
    for fuzzy_name, value in age_plot_values.items():
        plt.plot(age_space, value, label=f"{fuzzy_name}")
    plt.hlines(y=0, xmin=np.min(age_space), xmax=np.max(age_space), colors="black")
    plt.legend(loc="center right")

    plt.subplot(4, 1, 2)
    plt.title('Fuzzy BMI')
    for fuzzy_name, value in bmi_plot_values.items():
        plt.plot(bmi_space, value, label=f"{fuzzy_name}")
    plt.hlines(y=0, xmin=np.min(bmi_space), xmax=np.max(bmi_space), colors="black")
    plt.legend(loc="center right")

    plt.subplot(4, 1, 3)
    plt.title('Fuzzy Activity')
    for fuzzy_name, value in activity_plot_values.items():
        plt.plot(activity_space, value, label=f"{fuzzy_name}")
    plt.hlines(y=0, xmin=np.min(activity_space), xmax=np.max(activity_space), colors="black")
    plt.legend(loc="center right")

    plt.subplot(4, 1, 4)
    plt.title('Fuzzy Sugar Level')
    for fuzzy_name, value in sugar_plot_values.items():
        plt.plot(sugar_space, value, label=f"{fuzzy_name}")
    plt.hlines(y=0, xmin=np.min(sugar_space), xmax=np.max(sugar_space), colors="black")
    plt.legend(loc="center right")

    plt.tight_layout()
    plt.show()


def draw_output_over_time():
    # Simulate input data streams
    time_steps = 100
    time_space = np.linspace(start=0, stop=1, num=time_steps)

    noise_1 = (2 * np.random.randn(time_steps) - 1)
    noise_2 = (2 * np.random.randn(time_steps) - 1)

    # Age changes from 10 to 80 over time
    ages = (80 - 10) * time_space + 10

    # BMI changes over time
    bmis = 20 + 0.2 * noise_1 + 6 * time_space

    # Activity level changes
    activities = 9 + 0.2 * noise_2 - 3 * time_space

    # Predict blood sugar levels for each time step
    predicted_blood_sugars = [predict_blood_sugar(ages[t], bmis[t], activities[t]) for t in range(time_steps)]

    # Plotting
    plt.figure(figsize=(10, 9))

    plt.subplot(4, 1, 1)
    plt.plot(ages, color="tab:blue", label='Age')
    plt.title('Age over Time')
    plt.ylabel('Age')
    plt.ylim(ymin=0, ymax=100)
    plt.xticks([])
    plt.legend()

    plt.subplot(4, 1, 2)
    plt.plot(bmis, color="tab:orange", label='BMI')
    plt.title('BMI over Time')
    plt.ylabel('BMI')
    plt.ylim(ymin=18, ymax=28)
    plt.xticks([])
    plt.legend()

    plt.subplot(4, 1, 3)
    plt.plot(activities, color="tab:green", label='Activity')
    plt.title('Activity Level over Time')
    plt.ylabel('Activity')
    plt.ylim(ymin=0, ymax=10)
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


def main():
    draw_input_fuzzy_variable()
    draw_output_over_time()


if __name__ == '__main__':
    main()
