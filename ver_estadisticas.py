# ver_estadisticas.py
from flask import Blueprint, render_template_string
from models import Evento
from extensiones import db
from sqlalchemy import func

ver_estadisticas_bp = Blueprint('ver_estadisticas', __name__, url_prefix='/estadisticas')

@ver_estadisticas_bp.route('/')
def dashboard():
    # TOTAL DE EVENTOS
    total_eventos = db.session.query(func.count(Evento.id)).scalar() or 0

    # EVENTOS POR TIPO
    eventos_tipo = db.session.query(Evento.tipo_evento, func.count(Evento.id)) \
                             .group_by(Evento.tipo_evento).all()
    tipos = [t[0] for t in eventos_tipo]
    conteos_tipo = [t[1] for t in eventos_tipo]

    # TOTAL DE INGRESOS, ANTICIPOS Y RESTANTES
    suma_total = db.session.query(func.coalesce(func.sum(Evento.total), 0)).scalar() or 0
    suma_anticipo = db.session.query(func.coalesce(func.sum(Evento.anticipo), 0)).scalar() or 0
    suma_restan = db.session.query(func.coalesce(func.sum(Evento.restan), 0)).scalar() or 0

    # EVENTOS POR MUNICIPIO
    eventos_municipio = db.session.query(Evento.municipio, func.count(Evento.id)) \
                                  .group_by(Evento.municipio).all()
    municipios = [m[0] for m in eventos_municipio]
    conteos_municipio = [m[1] for m in eventos_municipio]

    return render_template_string("""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>📊 Dashboard de Estadísticas</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<style>
body { font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #e0f2fe, #93c5fd); min-height:100vh; }
.card { background: rgba(255,255,255,0.9); border-radius:1rem; padding:1.5rem; box-shadow:0 10px 30px rgba(0,0,0,0.1);}
</style>
</head>
<body class="p-6">

<div class="max-w-7xl mx-auto space-y-6">

<h1 class="text-3xl font-bold text-blue-700 mb-4">📊 Dashboard de Estadísticas</h1>

<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
    <div class="card text-center">
        <h2 class="font-semibold">Total de Eventos</h2>
        <p class="text-2xl font-bold">{{ total_eventos }}</p>
    </div>
    <div class="card text-center">
        <h2 class="font-semibold">Ingresos Totales</h2>
        <p class="text-2xl font-bold">${{ "{:,.2f}".format(suma_total) }}</p>
    </div>
    <div class="card text-center">
        <h2 class="font-semibold">Anticipos</h2>
        <p class="text-2xl font-bold">${{ "{:,.2f}".format(suma_anticipo) }}</p>
    </div>
    <div class="card text-center">
        <h2 class="font-semibold">Restan por cobrar</h2>
        <p class="text-2xl font-bold">${{ "{:,.2f}".format(suma_restan) }}</p>
    </div>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
    <div class="card">
        <h2 class="text-lg font-semibold mb-2">Eventos por Tipo</h2>
        <canvas id="tipoChart"></canvas>
    </div>

    <div class="card">
        <h2 class="text-lg font-semibold mb-2">Eventos por Municipio</h2>
        <canvas id="municipioChart"></canvas>
    </div>
</div>

<script>
const tipoCtx = document.getElementById('tipoChart').getContext('2d');
new Chart(tipoCtx, {
    type: 'doughnut',
    data: {
        labels: {{ tipos|tojson }},
        datasets: [{
            label: 'Eventos por tipo',
            data: {{ conteos_tipo|tojson }},
            backgroundColor: ['#f87171','#60a5fa','#34d399','#fbbf24','#a78bfa','#f472b6'],
        }]
    }
});

const municipioCtx = document.getElementById('municipioChart').getContext('2d');
new Chart(municipioCtx, {
    type: 'bar',
    data: {
        labels: {{ municipios|tojson }},
        datasets: [{
            label: 'Eventos por Municipio',
            data: {{ conteos_municipio|tojson }},
            backgroundColor: '#3b82f6'
        }]
    },
    options: {
        scales: {
            y: { beginAtZero:true }
        }
    }
});
</script>

</div>
</body>
</html>
""",
        total_eventos=total_eventos,
        suma_total=suma_total,
        suma_anticipo=suma_anticipo,
        suma_restan=suma_restan,
        tipos=tipos,
        conteos_tipo=conteos_tipo,
        municipios=municipios,
        conteos_municipio=conteos_municipio
    )
