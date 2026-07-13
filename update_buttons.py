import re

with open('dashboard/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CSS
css_addition = '''
        .btn-group {
            display: flex;
            gap: 4px;
            background: var(--card-bg);
            padding: 4px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            flex-wrap: wrap;
        }
        .btn-mun {
            padding: 8px 16px;
            border-radius: 6px;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .btn-mun:hover {
            color: var(--text-color);
            background: var(--hover-row-color);
        }
        .btn-mun.active {
            background: var(--text-color);
            color: var(--bg-color);
        }
'''
content = content.replace('</style>', css_addition + '</style>')

# 2. HTML Replace
old_select_html = '<select id="select-municipio" aria-label="Seleccionar Municipio"></select>'
new_select_html = '<div id="btn-group-municipio" class="btn-group"></div>'
content = content.replace(old_select_html, new_select_html)

# 3. JS Replace
old_js = '''                const municipios = dashboardData.totales_ca_mun ? dashboardData.totales_ca_mun.map(m => m.municipio) : Object.keys(dashboardData.top10_ca).sort();
                const select = document.getElementById('select-municipio');
                
                municipios.forEach(m => {
                    const opt = document.createElement('option');
                    opt.value = m;
                    opt.textContent = m;
                    select.appendChild(opt);
                });

                select.addEventListener('change', (e) => {
                    currentMunicipio = e.target.value;
                    updateDashboard();
                });

                renderTotalesChart();
                
                if(municipios.length > 0) {
                    currentMunicipio = municipios[0];
                    updateDashboard();
                }'''

new_js = '''                const municipios = dashboardData.totales_ca_mun ? dashboardData.totales_ca_mun.map(m => m.municipio) : Object.keys(dashboardData.top10_ca).sort();
                const btnGroup = document.getElementById('btn-group-municipio');
                
                municipios.forEach(m => {
                    const btn = document.createElement('button');
                    btn.className = 'btn-mun';
                    btn.textContent = m;
                    btn.onclick = () => {
                        document.querySelectorAll('.btn-mun').forEach(b => b.classList.remove('active'));
                        btn.classList.add('active');
                        currentMunicipio = m;
                        updateDashboard();
                    };
                    btnGroup.appendChild(btn);
                });

                renderTotalesChart();
                
                if(municipios.length > 0) {
                    currentMunicipio = municipios[0];
                    btnGroup.firstChild.classList.add('active');
                    updateDashboard();
                }'''

content = content.replace(old_js, new_js)

with open('dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Modificaciones aplicadas')
