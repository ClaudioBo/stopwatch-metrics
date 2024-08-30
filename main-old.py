import os, json, sys, random, time, webbrowser


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"rgba({r}, {g}, {b}, 0.8)"


if len(sys.argv) != 2:
    print("python main.py <json.txt>")
    exit()

averages = {}

file_path = sys.argv[1]
data = []

with open(file_path, "r") as file:
    for line in file:
        line_data = json.loads(line.replace("'", '"'))
        line_data = {k: float(v) for k, v in line_data.items()}
        data.append(line_data)

datasets = []
for key in data[0].keys():
    values = [float(d[key]) for d in data if key in d]

    # Creating a linear x-axis with numeric indices
    indices = list(range(len(values)))

    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    # Dataset for the original data
    datasets.append({"label": key, "data": [{"x": idx, "y": val} for idx, val in zip(indices, values)], "fill": False, "borderColor": color, "backgroundColor": color, "tension": 0.1, "parsing": False,})  # Structure data as x, y pairs

    # Calculate average
    avg_value = sum(values) / len(values)
    averages[key] = avg_value

html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metricas</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f7f7f7;
            flex-direction: column;
        }}
        #chart-container {{
            width: 100%;
            height: 100%;
        }}
        canvas {{
            max-height: 100%;
            max-width: 100%;
        }}
    </style>
</head>
<body>
    <div id="chart-container">
        <canvas id="myChart"></canvas>
    </div>
    <pre>
        {json.dumps(averages)}
    </pre>
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {{
            type: 'line',
            data: {{
                datasets: {json.dumps(datasets)}
            }},
            options: {{
                animation: false,
                parsing: false,
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Tiempo (ms)'
                        }}
                    }},
                    x: {{
                        type: 'linear',
                        title: {{
                            display: true,
                            text: 'Muestra'
                        }}
                    }}
                }},
                plugins: {{
                    decimation: {{
                        enabled: true,
                        algorithm: 'lttb',
                        samples: 100
                    }},
                }}
            }}
        }});
    </script>
</body>
</html>
"""

filename = f"output/chart-{int(time.time())}.html"

os.makedirs("output", exist_ok=True)

with open(filename, "w") as f:
    f.write(html_template)

print("Listo:", filename)
file_path = os.path.abspath(filename)
webbrowser.open(f"file://{file_path}")
