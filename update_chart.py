import re

with open('dashboard/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HTML structure
old_html = '''        <div class="card">
            <h2>Comparativo: Votos Totales Cámara (4 Municipios)</h2>
            <div style="position: relative; height: 280px; width: 100%;">
                <canvas id="chart-totales" role="img" aria-label="Gráfico de barras comparativo de votos totales cámara por municipio"></canvas>
            </div>
        </div>'''

new_html = '''        <div class="grid-2">
            <div class="card" style="display: flex; flex-direction: column;">
                <h2>Distribución de Votos (Cámara)</h2>
                <div style="position: relative; height: 280px; width: 100%; display: flex; justify-content: center; align-items: center; margin-top: auto; margin-bottom: auto;">
                    <canvas id="chart-totales" role="img" aria-label="Gráfico de distribución de votos totales cámara por municipio"></canvas>
                </div>
            </div>
            <div class="card">
                <h2>Resumen Departamental (4 Municipios)</h2>
                <div class="table-responsive">
                    <table id="table-resumen-mun">
                        <thead>
                            <tr>
                                <th>Municipio</th>
                                <th class="num-col">Votos</th>
                                <th class="num-col">% Total</th>
                            </tr>
                        </thead>
                        <tbody></tbody>
                    </table>
                </div>
            </div>
        </div>'''

content = content.replace(old_html, new_html)

# 2. Update JS function
old_js = '''        function renderTotalesChart() {
            const ctx = document.getElementById('chart-totales').getContext('2d');
            const labels = dashboardData.totales_ca_mun.map(d => d.municipio);
            const data = dashboardData.totales_ca_mun.map(d => d.votos);

            const bgColors = [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)'
            ];
            const borderColors = [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ];

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Votos Totales Cámara',
                        data: data,
                        backgroundColor: bgColors,
                        borderColor: borderColors,
                        borderWidth: 1,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }'''

new_js = '''        function renderTotalesChart() {
            const ctx = document.getElementById('chart-totales').getContext('2d');
            const labels = dashboardData.totales_ca_mun.map(d => d.municipio);
            const data = dashboardData.totales_ca_mun.map(d => d.votos);
            const totalVotos = data.reduce((a, b) => a + b, 0);

            // Populate table
            const tbody = document.querySelector('#table-resumen-mun tbody');
            tbody.innerHTML = '';
            
            const bgColors = [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)'
            ];
            const borderColors = [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ];

            dashboardData.totales_ca_mun.forEach((row, index) => {
                const tr = document.createElement('tr');
                const pct = ((row.votos / totalVotos) * 100).toFixed(1) + '%';
                tr.innerHTML = `
                    <td><span class="partido-color" style="background-color: ${borderColors[index]}"></span>${row.municipio}</td>
                    <td class="num-col">${row.votos.toLocaleString()}</td>
                    <td class="num-col">${pct}</td>
                `;
                tbody.appendChild(tr);
            });

            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Votos Totales Cámara',
                        data: data,
                        backgroundColor: bgColors,
                        borderColor: borderColors,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { 
                            display: true,
                            position: 'right'
                        }
                    }
                }
            });
        }'''

content = content.replace(old_js, new_js)

with open('dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
