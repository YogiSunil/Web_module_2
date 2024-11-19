from flask import Flask, request, render_template
import random

app = Flask(__name__)

def sort_letters(message):
    """A helper method to sort the characters of a string in alphabetical order
    and return the new string."""
    return ''.join(sorted(list(message)))


@app.route('/')
def homepage():
    """A homepage with handy links for your convenience."""
    return render_template('home.html')


@app.route('/froyo')
def choose_froyo():
    """Shows a form to collect the user's Fro-Yo order."""
    return render_template('froyo_form.html')


@app.route('/froyo_results')
def show_froyo_results():
    """Shows the user what they ordered from the previous page."""
    flavor = request.args.get('flavor')
    toppings = request.args.getlist('toppings')
    context = {
        'flavor': flavor,
        'toppings': toppings
    }
    return render_template('froyo_results.html', **context)


@app.route('/favorites')
def favorites():
    """Shows the user a form to choose their favorite color, animal, and city."""
    return render_template('favorites_form.html')


@app.route('/favorites_results')
def favorites_results():
    """Shows the user a nice message using their form results."""
    color = request.args.get('color')
    animal = request.args.get('animal')
    city = request.args.get('city')
    context = {
        'color': color,
        'animal': animal,
        'city': city
    }
    return render_template('favorites_results.html', **context)


@app.route('/secret_message')
def secret_message():
    """Shows the user a form to collect a secret message. Sends the result via
    the POST method to keep it a secret!"""
    return render_template('message_form.html')

@app.route('/message_results', methods=['POST'])
def message_results():
    """Shows the user their message, with the letters in sorted order."""
    message = request.form.get('message')  # This should match the 'name' attribute in the form
    if not message:
        return "No message provided.", 400  # If message is empty, return an error response

    sorted_message = sort_letters(message)
    return render_template('message_results.html', secret_message=message, sorted_message=sorted_message)


@app.route('/calculator')
def calculator_form():
    return render_template('calculator_form.html')

@app.route('/calculator_results', methods=['GET'])
def calculator_results():
    try:
        operand1 = request.args.get('operand1')
        operand2 = request.args.get('operand2')
        operation = request.args.get('operation')

        # Check if all parameters are provided
        if not operand1 or not operand2 or not operation:
            return render_template('calculator_results.html', error="Error: Missing operands or operation.")

        # Convert operands to float
        operand1 = int(operand1)
        operand2 = int(operand2)

        # Perform the calculation based on the selected operation
        if operation == 'add':
            result = operand1 + operand2
        elif operation == 'subtract':
            result = operand1 - operand2
        elif operation == 'multiply':
            result = operand1 * operand2
        elif operation == 'divide':
            if operand2 == 0:
                return render_template('calculator_results.html', error="Error: Division by zero is not allowed.")
            result = operand1 / operand2
        else:
            return render_template('calculator_results.html', error="Error: Invalid operation.")

        # Return the result
        return render_template('calculator_results.html', result=result, operand1=operand1, operand2=operand2, operation=operation)

    except ValueError:
        return render_template('calculator_results.html', error="Error: Invalid input. Please provide numeric values for operands.")

@app.route('/horoscope')
def horoscope():
    """Shows a form to enter your name and select a horoscope sign."""
    return render_template('horoscope_form.html')

@app.route('/horoscope_results')
def horoscope_results():
    """Displays the user's horoscope based on their sign."""
    sign = request.args.get('horoscope_sign')
    name = request.args.get('users_name')

    HOROSCOPE_PERSONALITIES = {
        'aries': 'Adventurous and energetic',
        'taurus': 'Patient and reliable',
        'gemini': 'Witty and versatile',
        'cancer': 'Loyal and empathetic',
        'leo': 'Generous and warmhearted',
        'virgo': 'Analytical and observant',
        'libra': 'Diplomatic and charming',
        'scorpio': 'Passionate and resourceful',
        'sagittarius': 'Optimistic and freedom-loving',
        'capricorn': 'Practical and disciplined',
        'aquarius': 'Inventive and original',
        'pisces': 'Compassionate and artistic'
    }

    lucky_number = random.randint(1, 100)

    personality = HOROSCOPE_PERSONALITIES.get(sign, "Unknown sign")

    return render_template('horoscope_results.html', name=name, sign=sign, personality=personality, lucky_number=lucky_number)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
