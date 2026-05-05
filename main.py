from flask import Flask, render_template, request, redirect, url_for, session
import math

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Доступные тригонометрические функции
FUNCTIONS = {
    'sin': 'sin(x) - Синус',
    'cos': 'cos(x) - Косинус',
    'tan': 'tan(x) - Тангенс',
    'cot': 'cot(x) - Котангенс',
    'asin': 'arcsin(x) - Арксинус',
    'acos': 'arccos(x) - Арккосинус',
    'atan': 'arctan(x) - Арктангенс',
    'acot': 'arccot(x) - Арккотангенс'
}


def calculate_trig_function(func_name, value, unit, precision):
    """Вычисление тригонометрической функции"""
    try:
        # Поддержка чисел с запятой (русский формат)
        value = str(value).replace(',', '.')
        value = float(value)

        # Перевод градусов в радианы для прямых функций
        if unit == 'degrees' and func_name in ['sin', 'cos', 'tan', 'cot']:
            value = math.radians(value)

        # Вычисление функции
        if func_name == 'sin':
            result = math.sin(value)
        elif func_name == 'cos':
            result = math.cos(value)
        elif func_name == 'tan':
            result = math.tan(value)
            if abs(result) > 1e10:
                return "Ошибка: значение близко к полюсу тангенса"
        elif func_name == 'cot':
            sin_val = math.sin(value)
            if abs(sin_val) < 1e-10:
                return "Ошибка: значение близко к полюсу котангенса"
            result = math.cos(value) / sin_val
        elif func_name == 'asin':
            if -1 <= value <= 1:
                result = math.asin(value)
                if unit == 'degrees':
                    result = math.degrees(result)
            else:
                return f"Ошибка: arcsin(x) определен только для x в [-1, 1]"
        elif func_name == 'acos':
            if -1 <= value <= 1:
                result = math.acos(value)
                if unit == 'degrees':
                    result = math.degrees(result)
            else:
                return f"Ошибка: arccos(x) определен только для x в [-1, 1]"
        elif func_name == 'atan':
            result = math.atan(value)
            if unit == 'degrees':
                result = math.degrees(result)
        elif func_name == 'acot':
            if abs(value) < 1e-10:
                result = math.pi / 2 if value >= 0 else -math.pi / 2
            else:
                result = math.atan(1 / value)
                if value < 0:
                    result += math.pi
            if unit == 'degrees':
                result = math.degrees(result)
        else:
            return "Ошибка: неизвестная функция"

        precision = int(precision)
        return round(result, precision)

    except ValueError:
        return "Ошибка: введите корректное число"
    except Exception as e:
        return f"Ошибка: {str(e)}"


@app.route('/', methods=['GET'])
def index():
    """Главная страница - пустая форма"""
    session.clear()
    return render_template(
        'index.html',
        result=None,
        error=None,
        functions=FUNCTIONS,
        selected_function='sin',
        selected_unit='radians',
        selected_precision=4,
        input_value=''
    )


@app.route('/', methods=['POST'])
def calculate():
    """Обработка формы - вычисление и перенаправление"""
    input_value = request.form.get('value', '')
    selected_function = request.form.get('function', 'sin')
    selected_unit = request.form.get('unit', 'radians')
    selected_precision = request.form.get('precision', 4)

    result = calculate_trig_function(
        selected_function, input_value, selected_unit, selected_precision
    )

    # Сохранение в сессию
    session['result'] = str(result) if not (isinstance(result, str) and result.startswith('Ошибка')) else None
    session['error'] = result if (isinstance(result, str) and result.startswith('Ошибка')) else None
    session['selected_function'] = selected_function
    session['selected_unit'] = selected_unit
    session['selected_precision'] = selected_precision
    session['input_value'] = input_value

    return redirect(url_for('index_with_result'))


@app.route('/result')
def index_with_result():
    """Страница с результатом из сессии"""
    result_str = session.get('result', None)
    error = session.get('error', None)
    selected_function = session.get('selected_function', 'sin')
    selected_unit = session.get('selected_unit', 'radians')
    selected_precision = session.get('selected_precision', 4)
    input_value = session.get('input_value', '')

    result = None
    if result_str and result_str != 'None':
        try:
            result = float(result_str)
        except:
            result = None

    return render_template(
        'index.html',
        result=result,
        error=error,
        functions=FUNCTIONS,
        selected_function=selected_function,
        selected_unit=selected_unit,
        selected_precision=int(selected_precision),
        input_value=input_value
    )


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)