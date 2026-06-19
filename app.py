from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

camiones = {
    "Camión Norte": [],
    "Camión Centro": [],
    "Camión Sur": []
}

def carga_total(camion):
    return sum(envio["peso"] for envio in camiones[camion])

@app.route("/")
def inicio():

    html = """
    <h1>🚚 Empresa de Reparto con IA Distribuida</h1>

    <form action="/crear" method="post">
        <input name="codigo" placeholder="Código" required>
        <input name="destino" placeholder="Destino" required>
        <input name="peso" type="number" placeholder="Peso" required>
        <button type="submit">Crear Envío</button>
    </form>

    <hr>

    {% for camion, envios in camiones.items() %}
        <h2>{{ camion }}</h2>
        <p>Carga Total: {{ cargas[camion] }} kg</p>

        <ul>
        {% for envio in envios %}
            <li>
                {{ envio["codigo"] }} -
                {{ envio["destino"] }} -
                {{ envio["peso"] }} kg

                <a href="/eliminar/{{ envio['codigo'] }}">
                    Eliminar
                </a>
            </li>
        {% endfor %}
        </ul>
    {% endfor %}
    """

    cargas = {
        camion: carga_total(camion)
        for camion in camiones
    }

    return render_template_string(
        html,
        camiones=camiones,
        cargas=cargas
    )

@app.route("/crear", methods=["POST"])
def crear():

    codigo = request.form["codigo"]
    destino = request.form["destino"]
    peso = float(request.form["peso"])

    # IA Distribuida:
    # Buscar el camión menos cargado
    mejor_camion = min(
        camiones,
        key=lambda c: carga_total(c)
    )

    camiones[mejor_camion].append({
        "codigo": codigo,
        "destino": destino,
        "peso": peso
    })

    return redirect("/")

@app.route("/eliminar/<codigo>")
def eliminar(codigo):

    for camion in camiones:
        camiones[camion] = [
            envio for envio in camiones[camion]
            if envio["codigo"] != codigo
        ]

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)