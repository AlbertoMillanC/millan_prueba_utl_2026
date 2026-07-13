import re

with open('dashboard/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add footer HTML
footer_html = '''        </div>

        <div style="text-align: center; padding: 32px 0 16px 0; color: var(--text-secondary); font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px;">
            Elaborado por: Alberto Millán.
        </div>
    </div>'''
content = content.replace('        </div>\n\n    </div>', footer_html)

# 2. Update chart options
old_chart_opts = '''                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { 
                            display: true,
                            position: 'right'
                        }
                    }
                }'''
new_chart_opts = '''                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { 
                            display: true,
                            position: 'right',
                            labels: {
                                font: { size: 13, family: 'Inter' },
                                padding: 20
                            }
                        },
                        tooltip: {
                            titleFont: { size: 14, family: 'Inter' },
                            bodyFont: { size: 15, weight: 'bold', family: 'Inter' },
                            padding: 12,
                            backgroundColor: 'rgba(15, 23, 42, 0.9)'
                        }
                    }
                }'''
content = content.replace(old_chart_opts, new_chart_opts)


# 3. Add credit to Excel
excel_credit_1 = '''
                    // Crédito Hoja 1
                    sheet.addRow([]);
                    sheet.addRow(['Elaborado por: Alberto Millán.']).font = { italic: true, color: { argb: 'FF888888' } };

                    // Hoja 2: Desglose Mesas'''
content = content.replace('                    // Hoja 2: Desglose Mesas', excel_credit_1)

excel_credit_2 = '''
                    // Crédito Hoja 2
                    mesasSheet.addRow([]);
                    mesasSheet.addRow(['Elaborado por: Alberto Millán.']).font = { italic: true, color: { argb: 'FF888888' } };

                    // Hoja 3: Votos por Puesto (Con Data Bars)'''
content = content.replace('                    // Hoja 3: Votos por Puesto (Con Data Bars)', excel_credit_2)

excel_credit_3 = '''
                    // Crédito Hoja 3
                    puestosSheet.addRow([]);
                    puestosSheet.addRow(['Elaborado por: Alberto Millán.']).font = { italic: true, color: { argb: 'FF888888' } };

                    const buffer = await workbook.xlsx.writeBuffer();'''
content = content.replace('                    const buffer = await workbook.xlsx.writeBuffer();', excel_credit_3)

with open('dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Modificaciones aplicadas')
