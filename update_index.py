import re

with open('dashboard/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for Data Bars
css_addition = '''
        .data-bar-cell {
            position: relative;
            z-index: 1;
        }
        .data-bar {
            position: absolute;
            top: 10%;
            left: 0;
            height: 80%;
            background-color: rgba(90, 141, 238, 0.2);
            border-radius: 4px;
            z-index: -1;
            transition: width 0.5s ease;
        }
'''
content = content.replace('</style>', css_addition + '</style>')

# 2. Add Puestos Table UI next to Mesa Explorer
ui_old = '''        <!-- EXPLORADOR DE MESAS -->
        <div class="header" style="margin-top: 48px;">
            <h2>Buscador de Mesas (Top 5 Cámara)</h2>
            <div class="controls">
                <select id="select-mun-mesa" aria-label="Seleccionar Municipio para Mesa"></select>
                <select id="select-puesto" aria-label="Seleccionar Puesto"></select>
                <select id="select-mesa" aria-label="Seleccionar Mesa"></select>
            </div>
        </div>

        <div class="card">
            <div class="table-responsive">
                <table id="table-mesa-top5">
                    <thead>
                        <tr>
                            <th>Candidato</th>
                            <th>Partido</th>
                            <th class="num-col">Votos</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>'''

ui_new = '''        <!-- EXPLORADOR DE MESAS Y PUESTOS -->
        <div class="header" style="margin-top: 48px;">
            <h2>Participación por Puestos y Mesas (Cámara)</h2>
            <div class="controls">
                <select id="select-mun-mesa" aria-label="Seleccionar Municipio para Mesa"></select>
            </div>
        </div>

        <div class="grid-2">
            <!-- PUESTOS (DATA BARS) -->
            <div class="card">
                <h2>Top Puestos de Votación</h2>
                <div class="table-responsive">
                    <table id="table-puestos">
                        <thead>
                            <tr>
                                <th>Puesto</th>
                                <th class="num-col">Votos</th>
                            </tr>
                        </thead>
                        <tbody></tbody>
                    </table>
                </div>
            </div>

            <!-- MESAS -->
            <div class="card">
                <h2>Detalle por Mesa</h2>
                <div class="controls" style="margin-bottom: 16px;">
                    <select id="select-puesto" aria-label="Seleccionar Puesto"></select>
                    <select id="select-mesa" aria-label="Seleccionar Mesa"></select>
                </div>
                <div class="table-responsive">
                    <table id="table-mesa-top5">
                        <thead>
                            <tr>
                                <th>Candidato</th>
                                <th>Partido</th>
                                <th class="num-col">Votos</th>
                            </tr>
                        </thead>
                        <tbody></tbody>
                    </table>
                </div>
            </div>
        </div>'''
content = content.replace(ui_old, ui_new)

# 3. Add JS for Puestos Table Rendering
js_puestos_render = '''        function updatePuestoSelect() {
            const selectMun = document.getElementById('select-mun-mesa').value;
            const selectPuesto = document.getElementById('select-puesto');
            
            // --- Render Puestos Table with Data Bars ---
            const tbodyPuestos = document.querySelector('#table-puestos tbody');
            tbodyPuestos.innerHTML = '';
            if(typeof puestosData !== 'undefined' && puestosData[selectMun]) {
                const puestos = puestosData[selectMun];
                const maxVotos = puestos.length > 0 ? puestos[0].votos : 1;
                
                // Show top 15 puestos
                puestos.slice(0, 15).forEach(p => {
                    const tr = document.createElement('tr');
                    const pct = (p.votos / maxVotos) * 100;
                    tr.innerHTML = `
                        <td>${p.puesto.startsWith('PUESTO_') ? p.puesto.replace('PUESTO_', 'Puesto ') : p.puesto}</td>
                        <td class="num-col data-bar-cell">
                            <div class="data-bar" style="width: ${pct}%"></div>
                            ${p.votos.toLocaleString()}
                        </td>
                    `;
                    tbodyPuestos.appendChild(tr);
                });
            }
            // -------------------------------------------

            selectPuesto.innerHTML = '';
            
            if(typeof mesasData !== 'undefined' && mesasData[selectMun]) {
                const puestos = Object.keys(mesasData[selectMun]).sort();
                puestos.forEach(p => {
                    const opt = document.createElement('option');
                    opt.value = p;
                    opt.textContent = p.startsWith('PUESTO_') ? p.replace('PUESTO_', 'Puesto ') : p;
                    selectPuesto.appendChild(opt);
                });
                
                if(puestos.length > 0) {
                    selectPuesto.value = puestos[0];
                }
            }
            updateMesaSelect();
        }'''

# Replace updatePuestoSelect function
content = re.sub(r'function updatePuestoSelect\(\) \{.*?\n        \}', js_puestos_render, content, flags=re.DOTALL)


# 4. Modify exportExcel to add third sheet with Data Bars
export_excel_addition = '''
                    // Hoja 3: Votos por Puesto (Con Data Bars)
                    const puestosSheet = workbook.addWorksheet('Votos por Puesto');
                    puestosSheet.columns = [
                        { header: 'Puesto de Votación', key: 'puesto', width: 35 },
                        { header: 'Votos', key: 'votos', width: 20 }
                    ];

                    puestosSheet.getRow(1).font = { bold: true, color: { argb: 'FFFFFFFF' } };
                    puestosSheet.getRow(1).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF1E293B' } };
                    puestosSheet.getRow(1).alignment = { horizontal: 'center' };
                    puestosSheet.autoFilter = 'A1:B1';

                    if(typeof puestosData !== 'undefined' && puestosData[currentMunicipio]) {
                        const puestos = puestosData[currentMunicipio];
                        puestos.forEach(p => {
                            puestosSheet.addRow({
                                puesto: p.puesto.startsWith('PUESTO_') ? p.puesto.replace('PUESTO_', 'Puesto ') : p.puesto,
                                votos: p.votos
                            });
                        });
                        
                        // Agregar Formato Condicional (Data Bars Nativos)
                        if(puestos.length > 0) {
                            const lastRow = puestos.length + 1;
                            puestosSheet.addConditionalFormatting({
                                ref: `B2:B${lastRow}`,
                                rules: [
                                    {
                                        type: 'dataBar',
                                        cfvo: [{ type: 'min', value: 0 }, { type: 'max' }],
                                        color: { argb: 'FF5A8DEE' }
                                    }
                                ]
                            });
                        }
                    }

                    const buffer = await workbook.xlsx.writeBuffer();'''

content = content.replace('                    const buffer = await workbook.xlsx.writeBuffer();', export_excel_addition)


with open('dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Modificaciones completadas exitosamente.")
