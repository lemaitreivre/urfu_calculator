'''App,that works with math expressions'''
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])

def calculate():
    '''function,that gets 2 nums from user,
	then working with expression'''
    data = request.get_json()
    first_num = data.get('first_num')
    second_num = data.get('second_num')
    operator = data.get('operator')

    if first_num is None or second_num is None or operator is None:
        return jsonify({'error': 'Invalid input'}), 400

    try:
        first_num = int(first_num)
        second_num = int(second_num)
    except ValueError:
        return jsonify({'error': 'Invalid numbers'}), 400

    if operator == '+':
        result = first_num + second_num
    elif operator == '-':
        result = first_num - second_num
    elif operator == '*':
        result = first_num * second_num
    elif operator == '/':
        if second_num == 0:
            return jsonify({'error': 'Division by zero'}), 400
        result = first_num / second_num
    else:
        return jsonify({'error': 'Invalid operator'}), 400
    return jsonify({'result': result}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)