import pandas as pd
import json
import os

def update_main_js():
    pbi_path = 'powerbi/PresupuestoNacionalRD_PowerBI_Unificado.csv'
    df = pd.read_csv(pbi_path)
    
    # Fill NaNs
    df['Seccion_Institucional'] = df['Seccion_Institucional'].fillna('No especificada')
    df['Capitulo'] = df['Capitulo'].fillna('No especificado')
    df['Sub_Capitulo'] = df['Sub_Capitulo'].fillna('No especificado')
    df['Finalidad'] = df['Finalidad'].fillna('No especificada')
    df['Funcion'] = df['Funcion'].fillna('No especificada')
    df['Sub_Funcion'] = df['Sub_Funcion'].fillna('No especificada')
    
    group_cols = [
        'Periodo_Anio', 
        'Seccion_Institucional', 
        'Capitulo',
        'Sub_Capitulo',
        'Finalidad', 
        'Funcion',
        'Sub_Funcion',
        'Tipo_Presupuesto', 
        'Fuente_Financiamiento'
    ]
    
    agg = df.groupby(group_cols).agg({
        'Presupuesto_Inicial': 'sum',
        'Presupuesto_Vigente': 'sum',
        'Devengado_Aprobado': 'sum'
    }).reset_index()
    
    agg.columns = ['year', 'seccion', 'capitulo', 'subcapitulo', 'finalidad', 'funcion', 'subfuncion', 'tipo', 'fuente', 'initial', 'budget', 'spent']
    
    # Precision 6 decimals
    agg['initial'] = (agg['initial'] / 1000000).round(6)
    agg['budget'] = (agg['budget'] / 1000000).round(6)
    agg['spent'] = (agg['spent'] / 1000000).round(6)
    
    agg = agg[(agg['initial'] != 0) | (agg['budget'] != 0) | (agg['spent'] != 0)]
    
    records_json = json.dumps(agg.to_dict('records'), indent=2, ensure_ascii=False)
    
    # Constants for filters
    secciones = sorted(df['Seccion_Institucional'].unique().tolist())
    finalidades = sorted(df['Finalidad'].unique().tolist())
    funciones = sorted(df['Funcion'].unique().tolist())
    subfunciones = sorted(df['Sub_Funcion'].unique().tolist())
    capitulos = sorted(df['Capitulo'].unique().tolist())
    subcapitulos = sorted(df['Sub_Capitulo'].unique().tolist())

    js_content = f"""/**
 * Lógica del Dashboard - Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 */

// --- CONFIGURACIÓN DE CLASIFICACIONES ---
const SECCIONES = {json.dumps(secciones, ensure_ascii=False)};
const FINALIDADES = {json.dumps(finalidades, ensure_ascii=False)};
const FUNCIONES = {json.dumps(funciones, ensure_ascii=False)};
const SUBFUNCIONES = {json.dumps(subfunciones, ensure_ascii=False)};
const CAPITULOS = {json.dumps(capitulos, ensure_ascii=False)};
const SUBCAPITULOS = {json.dumps(subcapitulos, ensure_ascii=False)};

// --- DATOS REALES ---
const MOCK_DATA = {records_json};

// --- DICCIONARIO MULTILINGÜE ---
const TRANSLATIONS = {{
    es: {{
        title: "Análisis del Presupuesto Nacional RD",
        author: "Autor: Lic. Manuel Mañana Santana",
        kpi_initial: "Presupuesto Inicial",
        kpi_budget: "Presupuesto Vigente",
        kpi_spent: "Total Devengado",
        kpi_exec: "% Ejecución",
        kpi_variation: "Variación Neta",
        variation_up: "Aumento Presupuestario",
        variation_down: "Disminución Presupuestaria",
        filter_title: "Filtros de Control",
        all: "Todos/Todas",
        label_year: "Año Fiscal:",
        label_secc: "Sección Institucional:",
        label_fin: "Finalidad:",
        label_fun: "Función:",
        label_subfun: "Sub-Función:",
        label_cap: "Capítulo:",
        label_subcap: "Sub-Capítulo:",
        btn_gasto: "Gasto",
        btn_aplicacion: "Aplicaciones Financieras",
        chart_inst: "Ejecución por Sección (RD$ MM)",
        chart_finality: "Presupuesto por Finalidad",
        chart_source: "Fuente de Financiamiento",
        chart_top_up: "Top 5 Aumentos (Vigente vs Inicial)",
        chart_top_down: "Top 5 Disminuciones (Vigente vs Inicial)",
        chart_fun_stacked_high: "Top 10 Funciones con Mayor Presupuesto",
        chart_fun_stacked_low: "Top 10 Funciones con Menor Presupuesto",
        table_priority_high: "Prioridad Alta: Top 10 Funciones y Sub-Funciones",
        table_priority_low: "Prioridad Baja: Top 10 Funciones y Sub-Funciones",
        table_title: "Detalle de Ejecución por Finalidad",
        th_fin: "Finalidad",
        th_initial: "Inicial (RD$ MM)",
        th_budget: "Vigente (RD$ MM)",
        th_spent: "Devengado (RD$ MM)",
        th_variation: "Variación (RD$ MM)",
        th_pct: "% Ejecución",
        th_priority_fun: "Función",
        th_priority_sub: "Sub-Función",
        th_priority_budget: "Presupuesto (RD$ MM)",
        th_priority_pct: "% del Total",
        footer: "© 2026 - Maestría en Ciencias de Datos e Inteligencia Artificial (UASD)",
        sections: {{
            "Administración central": "Administración central",
            "Instituciones públicas descentralizadas y autónomas no financieras": "Inst. descentralizadas/autónomas",
            "Instituciones de la seguridad social": "Seguridad Social"
        }}
    }},
    en: {{
        title: "DR National Budget Analysis",
        author: "Author: Lic. Manuel Mañana Santana",
        kpi_initial: "Initial Budget",
        kpi_budget: "Current Budget",
        kpi_spent: "Total Spent",
        kpi_exec: "Execution %",
        kpi_variation: "Net Variation",
        variation_up: "Budget Increase",
        variation_down: "Budget Decrease",
        filter_title: "Control Filters",
        all: "All",
        label_year: "Fiscal Year:",
        label_secc: "Institutional Section:",
        label_fin: "Purpose:",
        label_fun: "Function:",
        label_subfun: "Sub-Function:",
        label_cap: "Chapter:",
        label_subcap: "Sub-Chapter:",
        btn_gasto: "Expense",
        btn_aplicacion: "Financial Applications",
        chart_inst: "Execution by Section (RD$ MM)",
        chart_finality: "Budget by Purpose",
        chart_source: "Funding Source",
        chart_top_up: "Top 5 Increases",
        chart_top_down: "Top 5 Decreases",
        chart_fun_stacked_high: "Top 10 Functions (Highest Budget)",
        chart_fun_stacked_low: "Top 10 Functions (Lowest Budget)",
        table_priority_high: "High Priority: Top 10 Functions and Sub-Functions",
        table_priority_low: "Low Priority: Top 10 Functions and Sub-Functions",
        table_title: "Execution Detail by Purpose",
        th_fin: "Purpose",
        th_initial: "Initial (RD$ MM)",
        th_budget: "Current (RD$ MM)",
        th_spent: "Spent (RD$ MM)",
        th_variation: "Variation (RD$ MM)",
        th_pct: "Execution %",
        th_priority_fun: "Function",
        th_priority_sub: "Sub-Function",
        th_priority_budget: "Budget (RD$ MM)",
        th_priority_pct: "% of Total",
        footer: "© 2026 - MSc in Data Science and AI (UASD)",
        sections: {{
            "Administración central": "Central Administration",
            "Instituciones públicas descentralizadas y autónomas no financieras": "Decentralized/Autonomous Inst.",
            "Instituciones de la seguridad social": "Social Security"
        }}
    }}
}};

// --- ESTADO ---
let state = {{
    lang: 'es',
    year: 'all',
    seccion: 'all',
    finalidad: 'all',
    funcion: 'all',
    subfuncion: 'all',
    capitulo: 'all',
    subcapitulo: 'all',
    tipo: 'Gasto'
}};

let activeCharts = {{}};

document.addEventListener('DOMContentLoaded', () => {{
    initFilters();
    setupEvents();
    updateDashboard();
}});

function initFilters() {{
    const t = TRANSLATIONS[state.lang];
    
    fillSelect('filter-year', [...new Set(MOCK_DATA.map(d => d.year))].sort((a,b)=>b-a), t.all);
    fillSelect('filter-seccion', SECCIONES, t.all, s => t.sections[s] || s);
    fillSelect('filter-finalidad', FINALIDADES, t.all);
    fillSelect('filter-funcion', FUNCIONES, t.all);
    fillSelect('filter-subfuncion', SUBFUNCIONES, t.all);
    fillSelect('filter-capitulo', CAPITULOS, t.all);
    fillSelect('filter-subcapitulo', SUBCAPITULOS, t.all);
}}

function fillSelect(id, items, allText, labelFn = null) {{
    const sel = document.getElementById(id);
    const current = sel.value;
    while(sel.options.length > 0) sel.remove(0);
    const optAll = document.createElement('option');
    optAll.value = 'all';
    optAll.textContent = allText;
    sel.appendChild(optAll);
    items.forEach(item => {{
        const opt = document.createElement('option');
        opt.value = item;
        opt.textContent = labelFn ? labelFn(item) : item;
        sel.appendChild(opt);
    }});
    sel.value = current || 'all';
}}

function setupEvents() {{
    document.getElementById('lang-toggle').addEventListener('change', e => {{
        state.lang = e.target.checked ? 'en' : 'es';
        updateUIStrings();
        initFilters();
        updateDashboard();
    }});

    ['year', 'seccion', 'finalidad', 'funcion', 'subfuncion', 'capitulo', 'subcapitulo'].forEach(key => {{
        const id = 'filter-' + key;
        document.getElementById(id).addEventListener('change', e => {{
            state[key] = e.target.value;
            updateDashboard();
        }});
    }});

    document.getElementById('btn-gasto').addEventListener('click', () => {{
        state.tipo = 'Gasto';
        document.getElementById('btn-gasto').classList.add('active');
        document.getElementById('btn-aplicacion').classList.remove('active');
        updateDashboard();
    }});

    document.getElementById('btn-aplicacion').addEventListener('click', () => {{
        state.tipo = 'Aplicaciones Financieras';
        document.getElementById('btn-aplicacion').classList.add('active');
        document.getElementById('btn-gasto').classList.remove('active');
        updateDashboard();
    }});
}}

function updateUIStrings() {{
    const t = TRANSLATIONS[state.lang];
    document.querySelector('h1').textContent = t.title;
    document.querySelector('.author').textContent = t.author;
    document.getElementById('filters-h2').textContent = t.filter_title;
    ['year', 'secc', 'fin', 'fun', 'subfun', 'cap', 'subcap'].forEach(k => {{
        const el = document.getElementById('label-'+k);
        if(el) el.textContent = t['label_'+k];
    }});
    document.getElementById('btn-gasto').textContent = t.btn_gasto;
    document.getElementById('btn-aplicacion').textContent = t.btn_aplicacion;
    
    const h2Ids = [
        'chart-inst-h2', 'chart-finality-h2', 'chart-source-h2', 
        'chart-top-up-h2', 'chart-top-down-h2', 
        'chart-fun-stacked-high-h2', 'chart-fun-stacked-low-h2',
        'table-priority-high-h2', 'table-priority-low-h2',
        'table-h2'
    ];
    h2Ids.forEach(id => {{
        const el = document.getElementById(id);
        if(el) el.textContent = t[id.replace('-h2', '').replace(/-/g, '_')];
    }});

    const priorityHeaders = [
        ['th-priority-fun-h', 'th-priority-fun'], ['th-priority-sub-h', 'th-priority-sub'], 
        ['th-priority-budget-h', 'th-priority-budget'], ['th-priority-pct-h', 'th-priority-pct'],
        ['th-priority-fun-l', 'th-priority-fun'], ['th-priority-sub-l', 'th-priority-sub'], 
        ['th-priority-budget-l', 'th-priority-budget'], ['th-priority-pct-l', 'th-priority-pct']
    ];
    priorityHeaders.forEach(h => {{
        const el = document.getElementById(h[0]);
        if(el) el.textContent = t[h[1]];
    }});

    const tableHeaders = document.querySelectorAll('.data-table:not(.wide) th');
    if(tableHeaders.length >= 6) {{
        tableHeaders[0].textContent = t.th_fin;
        tableHeaders[1].textContent = t.th_initial;
        tableHeaders[2].textContent = t.th_budget;
        tableHeaders[3].textContent = t.th_spent;
        tableHeaders[4].textContent = t.th_variation;
        tableHeaders[5].textContent = t.th_pct;
    }}
    document.querySelector('footer p').textContent = t.footer;
}}

function updateDashboard() {{
    const filtered = MOCK_DATA.filter(d => {{
        return (state.year === 'all' || d.year.toString() === state.year) &&
               (state.seccion === 'all' || d.seccion === state.seccion) &&
               (state.finalidad === 'all' || d.finalidad === state.finalidad) &&
               (state.funcion === 'all' || d.funcion === state.funcion) &&
               (state.subfuncion === 'all' || d.subfuncion === state.subfuncion) &&
               (state.capitulo === 'all' || d.capitulo === state.capitulo) &&
               (state.subcapitulo === 'all' || d.subcapitulo === state.subcapitulo) &&
               (d.tipo === state.tipo);
    }});

    const totalInitial = filtered.reduce((s, d) => s + d.initial, 0);
    const totalBudget = filtered.reduce((s, d) => s + d.budget, 0);
    const totalSpent = filtered.reduce((s, d) => s + d.spent, 0);
    const pct = totalBudget > 0 ? (totalSpent / totalBudget) * 100 : 0;
    const variation = totalBudget - totalInitial;

    const t = TRANSLATIONS[state.lang];
    updateKPI('kpi-initial', t.kpi_initial, `RD$ ${{totalInitial.toLocaleString(undefined, {{minimumFractionDigits: 2}})}}M`);
    updateKPI('kpi-budget', t.kpi_budget, `RD$ ${{totalBudget.toLocaleString(undefined, {{minimumFractionDigits: 2}})}}M`);
    updateKPI('kpi-spent', t.kpi_spent, `RD$ ${{totalSpent.toLocaleString(undefined, {{minimumFractionDigits: 2}})}}M`);
    updateKPI('kpi-pct', t.kpi_exec, `${{pct.toFixed(2)}}%`);
    
    const varLabel = variation >= 0 ? t.variation_up : t.variation_down;
    updateKPI('kpi-variation', varLabel, `RD$ ${{Math.abs(variation).toLocaleString(undefined, {{minimumFractionDigits: 2}})}}M`);

    renderCharts(filtered);
    renderPriorityTables(filtered, totalBudget);
    renderMainTable(filtered);
}}

function updateKPI(id, label, value) {{
    const el = document.getElementById(id);
    if(el) {{
        el.querySelector('h3').textContent = label;
        el.querySelector('p').textContent = value;
    }}
}}

function renderCharts(data) {{
    const t = TRANSLATIONS[state.lang];
    
    updateChart('chart-seccion', 'bar', sumBy(data, 'seccion', 'spent', k => t.sections[k] || k), '#003876');
    updateChart('chart-finalidad', 'bar', sumBy(data, 'finalidad', 'budget'), '#ce1126', true);
    updateChart('chart-fuente', 'doughnut', sumBy(data, 'fuente', 'budget'));

    renderTopVariations(data);
    
    renderStackedChart('chart-fun-stacked-high', data, 'funcion', 'subfuncion', 10, 'desc');
    renderStackedChart('chart-fun-stacked-low', data, 'funcion', 'subfuncion', 10, 'asc');
}}

function sumBy(data, field, sumField, labelFn = null) {{
    const groups = {{}};
    data.forEach(d => {{
        const label = labelFn ? labelFn(d[field]) : d[field];
        groups[label] = (groups[label] || 0) + d[sumField];
    }});
    return groups;
}}

function renderTopVariations(data) {{
    const capGroups = sumBy(data, 'capitulo', 'budget');
    const iniGroups = sumBy(data, 'capitulo', 'initial');

    const variations = Object.keys(capGroups).map(cap => ({{
        name: cap,
        diff: capGroups[cap] - (iniGroups[cap] || 0)
    }}));

    const topUp = variations.filter(v => v.diff > 0).sort((a,b) => b.diff - a.diff).slice(0, 5);
    const topDown = variations.filter(v => v.diff < 0).sort((a,b) => a.diff - b.diff).slice(0, 5);

    const upData = {{}}; topUp.forEach(v => upData[v.name.substring(0,25)] = v.diff);
    updateChart('chart-top-up', 'bar', upData, '#28a745', true);

    const downData = {{}}; topDown.forEach(v => downData[v.name.substring(0,25)] = Math.abs(v.diff));
    updateChart('chart-top-down', 'bar', downData, '#ce1126', true);
}}

function renderPriorityTables(data, grandTotal) {{
    const groups = {{}};
    data.forEach(d => {{
        const key = d.funcion + '||' + d.subfuncion;
        if(!groups[key]) groups[key] = 0;
        groups[key] += d.budget;
    }});

    const list = Object.keys(groups).map(k => {{
        const [fun, sub] = k.split('||');
        return {{ fun, sub, budget: groups[k] }};
    }}).filter(i => i.budget > 0);

    const high = [...list].sort((a,b) => b.budget - a.budget).slice(0, 10);
    const low = [...list].sort((a,b) => a.budget - b.budget).slice(0, 10);

    fillPriorityTable('table-priority-high-body', high, grandTotal);
    fillPriorityTable('table-priority-low-body', low, grandTotal);
}}

function fillPriorityTable(tbodyId, items, grandTotal) {{
    const tbody = document.getElementById(tbodyId);
    if(!tbody) return;
    tbody.innerHTML = '';
    items.forEach(item => {{
        const pct = grandTotal > 0 ? (item.budget / grandTotal) * 100 : 0;
        tbody.innerHTML += `
            <tr>
                <td>${{item.fun}}</td>
                <td>${{item.sub}}</td>
                <td>${{item.budget.toLocaleString(undefined, {{minimumFractionDigits: 1}})}}</td>
                <td>${{pct.toFixed(2)}}%</td>
            </tr>
        `;
    }});
}}

function renderStackedChart(id, data, mainField, subField, limit, order) {{
    const mainTotals = sumBy(data, mainField, 'budget');
    const sortedMain = Object.keys(mainTotals)
        .filter(m => mainTotals[m] > 0)
        .sort((a,b) => order === 'desc' ? mainTotals[b] - mainTotals[a] : mainTotals[a] - mainTotals[b])
        .slice(0, limit);

    const filtered = data.filter(d => sortedMain.includes(d[mainField]));
    const subs = [...new Set(filtered.map(d => d[subField]))];

    const datasets = subs.map((sub, i) => ({{
        label: sub.substring(0, 20),
        data: sortedMain.map(main => {{
            return filtered.filter(d => d[mainField] === main && d[subField] === sub)
                           .reduce((s, d) => s + d.budget, 0);
        }}),
        backgroundColor: getPaletteColor(i)
    }}));

    const canvas = document.getElementById(id);
    if(!canvas) return;
    if(activeCharts[id]) activeCharts[id].destroy();

    activeCharts[id] = new Chart(canvas, {{
        type: 'bar',
        data: {{ labels: sortedMain.map(m => m.substring(0, 20)), datasets: datasets }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            scales: {{ x: {{ stacked: true }}, y: {{ stacked: true, ticks: {{ callback: v => v + 'M' }} }} }},
            plugins: {{ legend: {{ display: false }} }}
        }}
    }});
}}

function getPaletteColor(i) {{
    const colors = ['#003876', '#ce1126', '#00a8e8', '#28a745', '#ffc107', '#6c757d', '#fd7e14', '#20c997', '#e83e8c', '#6610f2'];
    return colors[i % colors.length];
}}

function updateChart(id, type, groups, color = null, horizontal = false) {{
    const labels = Object.keys(groups).filter(l => groups[l] !== 0);
    const values = labels.map(l => groups[l]);
    const canvas = document.getElementById(id);
    if(!canvas) return;
    if (activeCharts[id]) activeCharts[id].destroy();

    activeCharts[id] = new Chart(canvas, {{
        type: type,
        data: {{
            labels: labels,
            datasets: [{{
                data: values,
                backgroundColor: color || ['#003876', '#ce1126', '#00a8e8', '#28a745', '#ffc107', '#6c757d']
            }}]
        }},
        options: {{
            indexAxis: horizontal ? 'y' : 'x',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ 
                legend: {{ display: type !== 'bar', position: 'bottom' }},
                tooltip: {{ callbacks: {{ label: c => `RD$ ${{c.raw.toLocaleString()}} MM` }} }}
            }},
            scales: type === 'bar' ? {{ [horizontal ? 'x' : 'y']: {{ ticks: {{ callback: v => v + 'M' }} }} }} : {{}}
        }}
    }});
}}

function renderMainTable(data) {{
    const finGroups = {{}};
    data.forEach(d => {{
        if (!finGroups[d.finalidad]) finGroups[d.finalidad] = {{ initial: 0, budget: 0, spent: 0 }};
        finGroups[d.finalidad].initial += d.initial;
        finGroups[d.finalidad].budget += d.budget;
        finGroups[d.finalidad].spent += d.spent;
    }});

    const tbody = document.getElementById('table-body');
    if(!tbody) return;
    tbody.innerHTML = '';

    Object.keys(finGroups).sort().forEach(f => {{
        const {{ initial, budget, spent }} = finGroups[f];
        const variation = budget - initial;
        const pct = budget > 0 ? (spent / budget) * 100 : 0;
        tbody.innerHTML += `
            <tr>
                <td>${{f}}</td>
                <td>${{initial.toLocaleString(undefined, {{minimumFractionDigits: 1}})}}</td>
                <td>${{budget.toLocaleString(undefined, {{minimumFractionDigits: 1}})}}</td>
                <td>${{spent.toLocaleString(undefined, {{minimumFractionDigits: 1}})}}</td>
                <td class="${{variation >= 0 ? 'text-success' : 'text-danger'}}">${{variation.toLocaleString(undefined, {{minimumFractionDigits: 1}})}}</td>
                <td><span class="pct-badge ${{pct > 90 ? 'high' : 'low'}}">${{pct.toFixed(1)}}%</span></td>
            </tr>
        `;
    }});
}}"""
    
    with open('dashboard/main.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("dashboard/main.js actualizado con nuevos filtros y tablas de prioridad funcional.")

if __name__ == "__main__":
    update_main_js()
