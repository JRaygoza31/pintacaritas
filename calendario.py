# calendario.py
from flask import Blueprint, render_template_string
from models import Evento

calendario_bp = Blueprint('calendario', __name__, url_prefix='/calendario')

@calendario_bp.route('/', endpoint='ver_calendario')
def ver_calendario():

    eventos = []
    eventos_db = Evento.query.all()

    for e in eventos_db:
        if not e.fecha_evento:
            continue

        eventos.append({
            "id": e.id,
            "title": f"{e.tipo_evento} • {e.nombre_cliente}",
            "start": e.fecha_evento.strftime("%Y-%m-%d"),
            "tipo": e.tipo_evento,
            "nombre": e.nombre_cliente,
            "hora_inicio": e.hora_inicio,
            "hora_termino": e.hora_termino,
            "municipio": e.municipio,
            "salon": e.nombre_salon,
            "direccion": e.direccion,
            "whatsapp": e.whatsapp,
            "allDay": True
        })

    return render_template_string("""
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Calendario</title>

    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.8/index.global.min.js"></script>

    <style>
        body {
            background: linear-gradient(135deg, #3b82f6, #9333ea, #ec4899);
            background-size: 200% 200%;
            animation: fondomove 12s ease infinite;
        }
        @keyframes fondomove {
            0% { background-position: 0% 0%; }
            50% { background-position: 100% 100%; }
            100% { background-position: 0% 0%; }
        }

        .contenedor {
            background: rgba(255, 255, 255, 0.14);
            backdrop-filter: blur(20px);
            border-radius: 28px;
            padding: 40px;
            width: 100%;
            max-width: 1200px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.25);
            border: 1px solid rgba(255,255,255,0.3);
        }

        .titulo {
            font-size: 48px;
            font-weight: 900;
            color: white;
            text-shadow: 0 4px 14px rgba(0,0,0,0.35);
        }
    </style>
</head>

<body>

<div class="min-h-screen flex justify-center items-start p-10">

    <div class="contenedor">

        <h1 class="text-center titulo mb-8">Calendario de Eventos</h1>

        <div class="flex justify-center gap-4 mb-6">
            <select id="mesSelector">
                <option value="0">Enero</option>
                <option value="1">Febrero</option>
                <option value="2">Marzo</option>
                <option value="3">Abril</option>
                <option value="4">Mayo</option>
                <option value="5">Junio</option>
                <option value="6">Julio</option>
                <option value="7">Agosto</option>
                <option value="8">Septiembre</option>
                <option value="9">Octubre</option>
                <option value="10">Noviembre</option>
                <option value="11">Diciembre</option>
            </select>

            <select id="yearSelector"></select>
        </div>

        <div id="calendar" class="rounded-3xl p-4"></div>
    </div>
</div>


<!-- MODAL -->
<div id="eventoModal" class="fixed inset-0 bg-black/60 hidden justify-center items-center">
    <div class="bg-white rounded-2xl p-8 w-full max-w-md shadow-2xl border border-gray-200">
        <h2 class="text-2xl font-bold mb-4 text-purple-700" id="modalTitulo"></h2>

        <p class="mb-2"><strong>Nombre:</strong> <span id="modalNombre"></span></p>
        <p class="mb-2"><strong>Horario:</strong> <span id="modalHorario"></span></p>

        <p class="mb-2"><strong>Salón:</strong> <span id="modalSalon"></span></p>
        <p class="mb-2"><strong>Dirección:</strong> <span id="modalDireccion"></span></p>
        <p class="mb-2"><strong>Municipio:</strong> <span id="modalMunicipio"></span></p>

        <p class="mb-4"><strong>Tipo:</strong> <span id="modalTipo"></span></p>

        <div class="flex justify-between mt-6">
            <button onclick="cerrarModal()"
                class="px-4 py-2 rounded-xl bg-gray-300 hover:bg-gray-400">
                Cerrar
            </button>

            <a id="btnWhatsapp" target="_blank"
                class="px-4 py-2 rounded-xl bg-green-500 text-white font-bold hover:bg-green-600">
                Compartir por WhatsApp
            </a>
        </div>
    </div>
</div>


<script>
document.addEventListener("DOMContentLoaded", () => {

    function colorPorTipo(tipo) {
        tipo = tipo?.toLowerCase() || "";

        if (tipo.includes("pintacaritas")) return "#ec4899";
        if (tipo.includes("glitter")) return "#3b82f6";

        return "#9333ea";
    }

    var calendar = new FullCalendar.Calendar(document.getElementById("calendar"), {
        initialView: "dayGridMonth",
        locale: "es",

        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: ""
        },

        events: {{ eventos | tojson }},

        eventDidMount(info) {
            const color = colorPorTipo(info.event.extendedProps.tipo);

            Object.assign(info.el.style, {
                background: color,
                color: "white",
                padding: "8px 10px",
                borderRadius: "14px",
                border: "none",
                fontWeight: "700",
                boxShadow: "0 6px 16px rgba(0,0,0,0.35)"
            });
        },

        eventClick(info) {
            const datos = info.event.extendedProps;

            document.getElementById("modalTitulo").textContent = info.event.title;
            document.getElementById("modalNombre").textContent = datos.nombre;

            document.getElementById("modalHorario").textContent =
                `${datos.hora_inicio || "?"} a ${datos.hora_termino || "?"}`;

            document.getElementById("modalSalon").textContent = datos.salon || "No registrado";
            document.getElementById("modalDireccion").textContent = datos.direccion || "No registrada";
            document.getElementById("modalMunicipio").textContent = datos.municipio || "No registrado";

            document.getElementById("modalTipo").textContent = datos.tipo;

            const mensaje = encodeURIComponent(
                `📅 *Detalles del evento*\n` +
                `👤 Nombre: ${datos.nombre}\n` +
                `⏰ Horario: ${datos.hora_inicio} a ${datos.hora_termino}\n` +
                `🏢 Salón: ${datos.salon}\n` +
                `📍 Dirección: ${datos.direccion}\n` +
                `🌆 Municipio: ${datos.municipio}\n` +
                `🎨 Tipo: ${datos.tipo}\n` +
                `📆 Fecha: ${info.event.startStr}`
            );

            document.getElementById("btnWhatsapp").href =
                `https://wa.me/?text=${mensaje}`;

            document.getElementById("eventoModal").classList.remove("hidden");
        }
    });

    calendar.render();

    window.cerrarModal = function() {
        document.getElementById("eventoModal").classList.add("hidden");
    };

    const yearSelector = document.getElementById("yearSelector");
    const currentYear = new Date().getFullYear();

    for (let y = currentYear - 5; y <= currentYear + 5; y++) {
        let option = document.createElement("option");
        option.value = y;
        option.textContent = y;
        if (y === currentYear) option.selected = true;
        yearSelector.appendChild(option);
    }

    document.getElementById("mesSelector").addEventListener("change", cambiarFecha);
    yearSelector.addEventListener("change", cambiarFecha);

    function cambiarFecha() {
        const mes = parseInt(document.getElementById("mesSelector").value);
        const año = parseInt(yearSelector.value);
        calendar.gotoDate(new Date(año, mes, 1));
    }
});
</script>

</body>
</html>
""", eventos=eventos)
