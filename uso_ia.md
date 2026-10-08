Parte 1.
Cambie el nombre de la carpeta de mi proyecto de "back end" a "back end 2", ahora necesito conectar este proyecto a git hub.

R: La ia me entrego los comandos necesarios para poder conectar mi carpeta a mi repositorio de github.

Crear admin y super usuario.
R: La ia me entrego el comando para crear el usuario de admin: python manage.py createsuperuser y donde entrar: http://127.0.0.1:8000/admin/

Registre el modelo en admin.py con list_display (3 campos o más) y search_fields o list_filter.
R: La ia me dijo que agregar en el archivo admin y me explico que significa cada uno.

Ahora el paso 2 Poblamiento inicial generado con IA cargado en la BD; el template y cargue los datos (loaddata o ejecutando el script) y verifíquelos en /admin.
R: La ia me dijo que cree un .json y me dio el comando para poder cargalos: python manage.py loaddata herramientas.json 

Reemplace la lista estática de la ES1: el template principal ahora muestra el listado consultando

R: La ia me dio el código a cambiar para que funcione.
# catalogo/views.py
from django.shortcuts import render
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









Parte 2.
Se utilizo la IA como herramienta para resolver dudas durante la evaluación, en esta ocasión se dispuso nuevamente de Copilot. Esta herramienta tecnológica fue de mucha ayuda para lo que fue la creación del admin super usuario, se consulto paso por paso esa etapa, hasta la etapa de configuración de herramientas, su búsqueda, creación, y eliminación dentro de la página de admin, además también fue útil al resolver problemas en cuanto a lo que fueron errores para poder correr el servidor correctamente y conectar la base de datos de admin con la lista que tenia en html y css. Usar esta herramienta me ayudo mucho a poder avanzar el trabajo, sobre todo cuando surgen errores durante la realización, el modo de trabajo con la IA, es muy útil para poder aprender porque se pueden consultar dudas durante el proceso, sin embargo, en esta segunda evaluación me di cuenta lo importante de ser especifico al momento de realizar una consulta ya que la IA es demasiado especifica. 