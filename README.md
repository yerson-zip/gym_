#  Proyecto Gym – Usuarios y Reservas

Proyecto Django sencillo que permite gestionar **usuarios** y **reservas** para un gimnasio.  
Incluye registro, inicio de sesión básico y CRUD de reservas.  
Base de datos: **PostgreSQL**.

---

##  Requisitos

- Python 3.x  
- Django  
- PostgreSQL  
- pip / virtualenv (opcional pero recomendado)

---

##  Instalación

### 1. Clonar el proyecto
```bash
git clone https://github.com/yerson-zip/gym_
cd gym_
```

### 2. Crear un entorno virtual (opcional)
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

##  Configurar Base de Datos (PostgreSQL)

Crea una base de datos:

```sql
CREATE DATABASE gym_db;
```

Luego edita tu `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gym_db',
        'USER': 'postgres',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Ejecutar el servidor

```bash
python manage.py runserver
```

---

## Modelo de Usuario

El proyecto usa un modelo personalizado:

```python
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
```

---

## Modelo de Reservas

Relación **uno a muchos** (un usuario puede tener varias reservas):

```python
class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
```

---

##  Funcionalidades

- Registro de usuarios  
- Login y logout  
- Crear, editar y eliminar reservas  
- Relación usuario → muchas reservas  
- Validaciones básicas  

---

##  Usuario de prueba (opcional)

```sql
INSERT INTO app_usuario (nombre, correo, telefono, password)
VALUES ('Juan Perez', 'juan@example.com', '3001234567', '1234');
```

---

## Notas

- El login es básico, sin el sistema de auth de Django.  
- La contraseña no está hasheada (solo demostrativo).  
- Puedes extender los modelos según lo necesites.
