from flask import Flask, request, jsonify, render_template
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import threading

app = Flask(__name__)

def plot_graph(data):
    unit, pam, tam, sam, som, conversion_rate, growth_rate, cost, year = data

    # Генерация круговой диаграммы
    values = [pam, tam, sam, som]
    colors = ['#FF6B6B', '#FFC93C', '#6BCB77', '#4D96FF']
    labels = ['PAM', 'TAM', 'SAM', 'SOM']

    # Вычисляем радиусы кругов
    radii = [value / max(values) * 0.7 for value in values]
    max_radius = max(radii)

    # Вычисляем координаты центров кругов
    x_centers = [0, 0, 0, 0]
    y_centers = [radius for radius in radii]

    # Создаем фигуру и оси
    fig, ax = plt.subplots(figsize=(8, 6))

    # Рисуем круги
    for i in range(len(radii)):
        circle = plt.Circle((x_centers[i], y_centers[i]), radii[i], color=colors[i], fill=True, alpha=0.5)
        ax.add_artist(circle)

    # Добавляем легенду
    legend_x = max_radius + 0.3
    legend_y = np.linspace(0, max_radius * 2, len(labels))[::-1]
    for i in range(len(labels)):
        ax.text(legend_x, legend_y[i], f"{labels[i]}: {values[i]:.2f} {unit}", va='center', fontsize=12)

    # Настраиваем оси
    ax.set_xlim(-(max_radius + 0.2), max_radius + 0.5)
    ax.set_ylim(-(max_radius + 0.2), max_radius + 0.8)
    ax.set_aspect('equal')
    ax.axis('off')  # Скрываем оси координат

    # Центрируем заголовок по вертикали
    title = ax.set_title('Емкость рынка', fontsize=16, fontweight='bold')
    title.set_y(1.05)
    fig.subplots_adjust(top=0.85)

    # Сохранение диаграммы в виде base64-закодированного изображения
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Расчет прогноза финансовых результатов
    revenue_year1 = som * conversion_rate / 100
    revenue_year2 = revenue_year1 * (1 + growth_rate / 100)
    revenue_year3 = revenue_year2 * (1 + growth_rate / 100)
    revenue_year4 = revenue_year3 * (1 + growth_rate / 100)

    if 0 <= cost < 1:
        profit_year1 = revenue_year1 * (1 - cost)
        profit_year2 = revenue_year2 * (1 - cost)
        profit_year3 = revenue_year3 * (1 - cost)
        profit_year4 = revenue_year4 * (1 - cost)
    else:
        profit_year1 = revenue_year1 - cost
        profit_year2 = revenue_year2 - cost
        profit_year3 = revenue_year3 - cost
        profit_year4 = revenue_year4 - cost

    # Создание диаграммы прогноза финансовых результатов
    fig, ax = plt.subplots(figsize=(8, 6))
    x = [f'{year+i}' for i in range(1, 5)]
    revenue = [revenue_year1, revenue_year2, revenue_year3, revenue_year4]
    profit = [profit_year1, profit_year2, profit_year3, profit_year4]
    cost_line = [cost, cost, cost, cost]
    ax.plot(x, revenue, label='Выручка')
    ax.plot(x, profit, label='Прибыль')
    ax.plot(x, cost_line, label='Затраты')

    # Добавление сетки координат
    ax.grid(True)

    ax.set_xlabel('Год', fontsize=14, fontweight='bold')
    ax.set_ylabel(unit, fontsize=14, fontweight='bold')
    ax.set_title('Прогноз финансовых результатов', fontsize=16, fontweight='bold')
    ax.legend()

    # Сохранение диаграммы в виде base64-закодированного изображения
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    forecast_chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return {
        'chart': chart_base64,
        'forecastChart': forecast_chart_base64
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    unit = data['unit']
    pam = float(data['pam'])
    tam = float(data['tam'])
    sam = float(data['sam'])
    som = float(data['som'])
    conversion_rate = float(data['conversionRate'])
    growth_rate = float(data['growthRate'])
    cost = float(data['cost'])
    year = int(data['year'])

    result = plot_graph((unit, pam, tam, sam, som, conversion_rate, growth_rate, cost, year))

    return jsonify({
        'unit': unit,
        'pam': pam,
        'tam': tam,
        'sam': sam,
        'som': som,
        'conversionRate': conversion_rate * 100,
        'cost': cost,
        'chart': result['chart'],
        'forecastChart': result['forecastChart']
    })

if __name__ == '__main__':
    app.run(debug=True)