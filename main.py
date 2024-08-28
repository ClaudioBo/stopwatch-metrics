import json, sys, random, time


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"rgba({r}, {g}, {b}, 0.8)"


if len(sys.argv) != 2:
    print("python main.py <json.txt>")
    exit()

file_path = sys.argv[1]
data = []

with open(file_path, "r") as file:
    for line in file:
        line_data = json.loads(line.replace("'", '"'))
        line_data = {k: float(v) for k, v in line_data.items()}
        data.append(line_data)

labels = [f"{i+1}" for i in range(len(data))]
datasets = []
average_line_indices = []

for index, key in enumerate(data[0].keys()):

    values = [d[key] for d in data if key in d]
    avg_value = sum(values) / len(values)
    color = random_color()

    datasets.append({"label": key, "data": values, "fill": False, "borderColor": color, "tension": 0.1, "averageIndex": len(datasets) + 1})
    average_line_indices.append(len(datasets))
    datasets.append({"data": [avg_value] * len(values), "fill": False, "borderColor": color, "borderDash": [5, 5], "tension": 0.1, "averageIndex": None, "hidden": False, "borderWidth": 2})


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
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels)},
                datasets: {json.dumps(datasets)}
            }},
            options: {{
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
                        title: {{
                            display: true,
                            text: 'Muestra'
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        onClick: (e, legendItem, legend) => {{
                            const index = legendItem.datasetIndex;
                            const chart = legend.chart;
                            const dataset = chart.data.datasets[index];
                            const averageIndex = dataset.averageIndex;
                            
                            if (averageIndex !== null) {{
                                const meta = chart.getDatasetMeta(index);
                                const avgMeta = chart.getDatasetMeta(averageIndex);
                                const visibility = !meta.hidden;
                                
                                meta.hidden = visibility;
                                avgMeta.hidden = visibility;
                                
                                chart.update();
                            }}
                        }},
                        labels: {{
                            filter: (legendItem, chartData) => {{
                            return (chartData.datasets[legendItem.datasetIndex].label)
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

filename = f"chart-{int(time.time())}.html"

with open(filename, "w") as f:
    f.write(html_template)

print("Listo:", filename)
