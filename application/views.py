from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password , check_password
from .models import Usuario, Reserva
from .forms import LoginForm, UsuarioForm, ReservaForm

def index(request):
    return render(request, "index.html")

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data["correo"]
            password = form.cleaned_data["password"]

            try:
                usuario = Usuario.objects.get(correo=correo)

                if check_password(password, usuario.password):
                    request.session["usuario_id"] = usuario.id
                    return redirect("dashboard")
                
                else:
                    return render(request, "login.html", {"form": form, "error": "Credenciales inválidas"})
    

            except Usuario.DoesNotExist:
                return render(request, "login.html", {"form": form, "error": "Credenciales inválidas"})
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def registro(request):
    if request.method =="POST":
      form = UsuarioForm(request.POST)

      if form.is_valid():
        nombre = form.cleaned_data["nombre"]
        correo = form.cleaned_data["correo"]
        telefono = form.cleaned_data["telefono"]
        password = form.cleaned_data["password"]
        confirmPassword = request.POST["confirmPassword"]

        if(password!=confirmPassword):
            
                return render(
                    request,
                    "registro.html",
                    {
                        "form": form,
                        "error": "Las contraseñas no coinciden"
                    }
                )
        hashed_password = make_password(password)

        Usuario.objects.create(
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                password=hashed_password
            )
        
        return redirect("login")
    else:
        form = UsuarioForm()

    return render(request, "registro.html", {"form": form})



def logout(request):
    request.session.flush()
    return redirect("index")


def dashboard(request):
    if "usuario_id" not in request.session:
        return redirect("login")

    try:

        usuario = Usuario.objects.get(id=request.session["usuario_id"])
    
    except Usuario.DoesNotExist:
        request.session.flush()
        return redirect("login")

    return render(request, "dashboard.html", {"usuario": usuario})


# ------- CRUD RESERVAS ---------

def reserva_create(request):
    if "usuario_id" not in request.session:
        return redirect("login")

    usuario = Usuario.objects.get(id=request.session["usuario_id"])
    reservas = usuario.reservas.all()

    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            Reserva.objects.create(
                usuario=usuario,
                fecha=form.cleaned_data["fecha"],
                hora=form.cleaned_data["hora"],
                actividad=form.cleaned_data["actividad"],
                notas=form.cleaned_data["notas"]
            )
            return redirect("reserva_create")  # Aquí rediriges a la misma página
    else:
        form = ReservaForm()

    return render(request, "reservas/form.html", {
        "form": form,
        "accion": "Crear",
        "reservas": reservas
    })

def reserva_update(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    if "usuario_id" not in request.session or reserva.usuario.id != request.session["usuario_id"]:
        return redirect("login")

    usuario = reserva.usuario
    reservas = usuario.reservas.all()

    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva.fecha = form.cleaned_data["fecha"]
            reserva.hora = form.cleaned_data["hora"]
            reserva.actividad = form.cleaned_data["actividad"]
            reserva.notas = form.cleaned_data["notas"]
            reserva.save()
            return redirect("reserva_create")
    else:
        form = ReservaForm(initial={
            "fecha": reserva.fecha.strftime("%Y-%m-%d"),
            "hora": reserva.hora.strftime("%H:%M"),
            "actividad": reserva.actividad,
            "notas": reserva.notas
        })

    return render(request, "reservas/form.html", {
        "form": form,
        "accion": "Editar",
        "reservas": reservas
    })


def reserva_delete(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    if "usuario_id" not in request.session or reserva.usuario.id != request.session["usuario_id"]:
        return redirect("login")

    if request.method == "POST":
        reserva.delete()
        return redirect("reserva_create")

    return render(request, "reservas/delete.html", {"reserva": reserva})
