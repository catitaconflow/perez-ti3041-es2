from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hola, esta es la app catálogo.")

import json
from django.shortcuts import render
from django.http import HttpResponseNotFound
from pathlib import Path

# catalogo/views.py
from .models import Herramienta

def listado_herramientas(request):
    # Consulta todos los registros desde la BD
    herramientas = Herramienta.objects.all()

    contexto = {
        "herramientas": herramientas,
        "total": herramientas.count(),
        "disponibles": herramientas.filter(stock__gt=0).count(),
    }
    return render(request, "catalogo/lista.html", contexto)


def detalle_herramienta(request, id):
    ruta = Path(__file__).resolve().parent / "data" / "herramientas.json"
    with open(ruta, encoding="utf-8") as f:
        herramientas = json.load(f) 

    print("Herramientas cargadas:", herramientas[:3])  
    print("Buscando id:", id)

    herramienta = next((h for h in herramientas if h.get("id") == id), None)

    if herramienta is None:
        return HttpResponseNotFound("<h2>Herramienta no encontrada</h2>")

    return render(request, "catalogo/detalle.html", {"herramienta": herramienta})


from django.shortcuts import render, redirect

def login_view(request):
    mensaje = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == "cata" and password == "1234":
            request.session["usuario"] = username
            return redirect("herramientas")
        else:
            mensaje = "Credenciales inválidas"

    return render(request, "catalogo/login.html", {"mensaje": mensaje})

import json
from pathlib import Path
from django.shortcuts import render, redirect

# Ruta al archivo JSON
DATA_PATH = Path(__file__).resolve().parent / "data" / "herramientas.json"

def cargar_herramientas():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# Detalle de una herramienta
def detalle_herramienta(request, id):
    herramientas = cargar_herramientas()
    herramienta = next((h for h in herramientas if h["id"] == id), None)
    return render(request, "catalogo/detalle.html", {"herramienta": herramienta})


def guardar_herramientas(herramientas):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(herramientas, f, ensure_ascii=False, indent=2)

# Carrito: agregar producto

def agregar_carrito(request, id):
    if request.method == "POST":
        cantidad = int(request.POST.get("cantidad", 1))
        carrito = request.session.get("carrito", {})
        carrito[str(id)] = carrito.get(str(id), 0) + cantidad
        request.session["carrito"] = carrito
    return redirect("ver_carrito")


# Carrito: ver contenido

def ver_carrito(request):
    herramientas = cargar_herramientas()
    carrito = request.session.get("carrito", {})
    items, total = [], 0

    for id, cantidad in carrito.items():
        herramienta = next((h for h in herramientas if h["id"] == int(id)), None)
        if herramienta:
            subtotal = herramienta["precio"] * cantidad  # ✅ cálculo correcto
            items.append({
                "herramienta": herramienta,
                "cantidad": cantidad,
                "subtotal": subtotal
            })
            total += subtotal

    return render(request, "catalogo/carrito.html", {"items": items, "total": total})



# Carrito: confirmar compra
def confirmar_compra(request):
    herramientas = cargar_herramientas()
    carrito = request.session.get("carrito", {})
    mensajes = []

    for id, cantidad in carrito.items():
        herramienta = next((h for h in herramientas if h["id"] == int(id)), None)
        if herramienta:
            if herramienta["stock"] >= cantidad:
                herramienta["stock"] -= cantidad
                mensajes.append(f"Compra realizada: {herramienta['nombre']} x{cantidad}")
            else:
                mensajes.append(f"No hay stock suficiente de {herramienta['nombre']}")

    guardar_herramientas(herramientas)  # 🔹 guarda los cambios en el JSON
    request.session["carrito"] = {}  # vacía el carrito

    return render(request, "catalogo/confirmacion.html", {"mensajes": mensajes})

def eliminar_del_carrito(request, id):
    carrito = request.session.get("carrito", {})
    id_str = str(id)

    if id_str in carrito:
        if carrito[id_str] > 1:
            carrito[id_str] -= 1  # 🔹 resta una unidad
        else:
            del carrito[id_str]   # 🔹 elimina el producto si llega a 0
        request.session["carrito"] = carrito

    return redirect("ver_carrito")


def cancelar_compra(request):
    request.session["carrito"] = {}
    return redirect("ver_carrito")
