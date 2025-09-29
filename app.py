<<<<<<< HEAD
=======
import os
#nuevo
from werkzeug.utils import secure_filename
#
>>>>>>> f968ce65124a6f032d20c4e2957637b2da2aae63
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify  # <-- añadí send_file, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from routes.Administrador import Administrador_bp
from routes.Docente import Docente_bp
from routes.Acudiente import Acudiente_bp
from routes.Estudiante import Estudiante_bp
import pymysql

#lo de fredy:
from flask import Flask, jsonify
from sqlalchemy import text 


# Importa el objeto 'db' y los modelos desde tu archivo de modelos
<<<<<<< HEAD
from Controladores.models import db, Usuario, Acudiente, Curso, Matricula, Periodo, Asignatura, Docente_Asignatura, Programacion, Asistencia, Detalle_Asistencia, Cronograma_Actividades, Actividad, Actividad_Estudiante, Observacion
=======
from database.models import db, Usuario
#nuevo
from flask import Flask, jsonify
from flask_login import login_required, current_user
from database.models import Notificacion
>>>>>>> f968ce65124a6f032d20c4e2957637b2da2aae63

# Configuración de la aplicación
app = Flask(__name__)

#nuevo
UPLOAD_FOLDER = os.path.join("static", "uploads", "circulares")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Configuración de la base de datos
DB_URL = 'mysql+pymysql://root:@127.0.0.1:3306/edunotas'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_super_secreta'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}

# Inicializa la instancia de SQLAlchemy con la aplicación
db.init_app(app)

# Inicialización de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Esta función es requerida por Flask-Login para cargar un usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Crea la base de datos y las tablas si no existen
with app.app_context():
    engine = create_engine(DB_URL)
    if not database_exists(engine.url):
        create_database(engine.url)
        print("Base de datos 'edunotas' creada exitosamente.")
    db.create_all()
    print("Tablas de la base de datos creadas exitosamente.")

# ---------------- RUTAS PRINCIPALES ----------------

@app.route('/')
def index():
<<<<<<< HEAD
    return render_template("Login.html")
=======
   return render_template("Login.html")


@app.route('/paginainicio')
def paginainicio():
    return render_template('Administrador/templates/Paginainicio.html')

@app.route('/perfil')
@login_required
def perfil():
    return render_template('Administrador/templates/perfil.html', usuario=current_user)

@app.route('/notas')
def notas():
    return render_template('Administrador/templates/Notas.html')


@app.route('/observador')
def observador():
    return render_template('Administrador/templates/Observador.html')

@app.route('/profesores')
@login_required
def profesores():
    docentes = Usuario.query.filter_by(Rol='Docente').all()
    return render_template('Administrador/templates/Profesores.html', docentes=docentes)

@app.route('/agregar_docente', methods=['POST'])
@login_required
def agregar_docente():
    try:
        nombre = request.form['Nombre']
        apellido = request.form['Apellido']
        correo = request.form['Correo']
        numero_doc = request.form['NumeroDocumento']
        telefono = request.form['Telefono']
        tipo_doc = "C.C."
        profesion = request.form['Profesion']
        ciclo = request.form['Ciclo']

        # Contraseña temporal
        hashed_password = generate_password_hash("123456")

        nuevo_docente = Usuario(
            Nombre=nombre,
            Apellido=apellido,
            Correo=correo,
            Contrasena=hashed_password,
            TipoDocumento=tipo_doc,
            NumeroDocumento=numero_doc,
            Telefono=telefono,
            Rol='Docente',
            Estado='Activo',
            Direccion="",
            Genero="Otro"
        )
        db.session.add(nuevo_docente)
        db.session.commit()
        flash("Docente agregado correctamente", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al agregar docente: {str(e)}", "danger")

    return redirect(url_for('profesores'))


# Actualizar Docente
@app.route('/actualizar_docente/<int:id>', methods=['POST'])
def actualizar_docente(id):
    docente = Usuario.query.get_or_404(id)  # Buscar por ID

    docente.Nombre = request.form['Nombre']
    docente.Apellido = request.form['Apellido']
    docente.TipoDocumento = request.form['TipoDocumento']
    docente.NumeroDocumento = request.form['NumeroDocumento']
    docente.Correo = request.form['Correo']
    docente.Telefono = request.form['Telefono']
    docente.Direccion = request.form['Profesion']
    docente.Calle = request.form['Ciclo']

    try:
        db.session.commit()
        flash("Docente actualizado correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {e}", "danger")

    return redirect(url_for('profesores'))


# Eliminar Docente
@app.route('/eliminar_docente/<int:id>', methods=['POST'])
@login_required
def eliminar_docente(id):
    docente = Usuario.query.get_or_404(id)
    try:
        db.session.delete(docente)
        db.session.commit()
        flash("Docente eliminado correctamente", "danger")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al eliminar docente: {str(e)}", "danger")

    return redirect(url_for('profesores'))


# ---------------- ESTUDIANTES ----------------

@app.route('/estudiantes')
@login_required
def estudiantes():
    estudiantes = Usuario.query.filter_by(Rol='Estudiante').all()
    return render_template('Administrador/templates/Estudiantes.html', estudiantes=estudiantes)


@app.route('/agregar_estudiante', methods=['POST'])
@login_required
def agregar_estudiante():
    try:
        nombre = request.form['Nombre']
        apellido = request.form['Apellido']
        correo = request.form['Correo']
        numero_doc = request.form['NumeroDocumento']
        telefono = request.form['Telefono']
        tipo_doc = request.form['TipoDocumento']
        direccion = request.form['Direccion']
        curso = request.form['Curso']

        hashed_password = generate_password_hash("123456")

        nuevo_estudiante = Usuario(
            Nombre=nombre,
            Apellido=apellido,
            Correo=correo,
            Contrasena=hashed_password,
            TipoDocumento=tipo_doc,
            NumeroDocumento=numero_doc,
            Telefono=telefono,
            Rol='Estudiante',
            Estado='Activo',
            Direccion=direccion,
            Calle=curso,
            Genero="Otro"
        )
        db.session.add(nuevo_estudiante)
        db.session.commit()
        flash("Estudiante agregado correctamente", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al agregar estudiante: {str(e)}", "danger")

    return redirect(url_for('estudiantes'))


@app.route('/actualizar_estudiante/<int:id>', methods=['POST'])
@login_required
def actualizar_estudiante(id):
    estudiante = Usuario.query.get_or_404(id)

    estudiante.Nombre = request.form['Nombre']
    estudiante.Apellido = request.form['Apellido']
    estudiante.TipoDocumento = request.form['TipoDocumento']
    estudiante.NumeroDocumento = request.form['NumeroDocumento']
    estudiante.Correo = request.form['Correo']
    estudiante.Telefono = request.form['Telefono']
    estudiante.Direccion = request.form['Direccion']
    estudiante.Calle = request.form['Curso']

    try:
        db.session.commit()
        flash("Estudiante actualizado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {e}", "danger")

    return redirect(url_for('estudiantes'))


@app.route('/eliminar_estudiante/<int:id>', methods=['POST'])
@login_required
def eliminar_estudiante(id):
    estudiante = Usuario.query.get_or_404(id)
    try:
        db.session.delete(estudiante)
        db.session.commit()
        flash("Estudiante eliminado correctamente", "danger")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al eliminar estudiante: {str(e)}", "danger")

    return redirect(url_for('estudiantes'))


# ---------------- ACUDIENTES ----------------

@app.route('/acudientes')
@login_required
def acudientes():
    acudientes = Usuario.query.filter_by(Rol='Acudiente').all()
    return render_template('Administrador/templates/Acudientes.html', acudientes=acudientes)


@app.route('/agregar_acudiente', methods=['POST'])
@login_required
def agregar_acudiente():
    try:
        nombre = request.form['Nombre']
        apellido = request.form['Apellido']
        correo = request.form['Correo']
        numero_doc = request.form['NumeroDocumento']
        telefono = request.form['Telefono']
        tipo_doc = request.form['TipoDocumento']
        direccion = request.form['Direccion']

        hashed_password = generate_password_hash("123456")

        nuevo_acudiente = Usuario(
            Nombre=nombre,
            Apellido=apellido,
            Correo=correo,
            Contrasena=hashed_password,
            TipoDocumento=tipo_doc,
            NumeroDocumento=numero_doc,
            Telefono=telefono,
            Direccion=direccion,
            Rol='Acudiente',
            Estado='Activo',
            Genero="Otro"
        )
        db.session.add(nuevo_acudiente)
        db.session.commit()
        flash("Acudiente agregado correctamente", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al agregar acudiente: {str(e)}", "danger")

    return redirect(url_for('acudientes'))


@app.route('/actualizar_acudiente/<int:id>', methods=['POST'])
@login_required
def actualizar_acudiente(id):
    acudiente = Usuario.query.get_or_404(id)

    acudiente.Nombre = request.form['Nombre']
    acudiente.Apellido = request.form['Apellido']
    acudiente.TipoDocumento = request.form['TipoDocumento']
    acudiente.NumeroDocumento = request.form['NumeroDocumento']
    acudiente.Correo = request.form['Correo']
    acudiente.Telefono = request.form['Telefono']
    acudiente.Direccion = request.form['Direccion']

    try:
        db.session.commit()
        flash("Acudiente actualizado correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {e}", "danger")

    return redirect(url_for('acudientes'))


@app.route('/eliminar_acudiente/<int:id>', methods=['POST'])
@login_required
def eliminar_acudiente(id):
    acudiente = Usuario.query.get_or_404(id)
    try:
        db.session.delete(acudiente)
        db.session.commit()
        flash("Acudiente eliminado correctamente", "danger")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al eliminar acudiente: {str(e)}", "danger")

    return redirect(url_for('acudientes'))


@app.route('/manual')
def manual():
    return render_template('Administrador/templates/ManualUsuario.html')

@app.route('/resumensemanal')
def resumensemanal():
    return render_template('Administrador/templates/ResumenSemanal.html')

@app.route('/registrotutorias')
def registrotutorias():
    return render_template('Administrador/templates/RegistroTutorías.html')

@app.route('/comunicacion')
def comunicacion():
    return render_template('Administrador/templates/Comunicación.html')

@app.route('/materialapoyo')
def materialapoyo():
    return render_template('Administrador/templates/MaterialApoyo.html')

@app.route('/reunion')
def reunion():
    return render_template('Administrador/templates/Reunion.html')


@app.route('/noticias')
def noticias():
    return render_template('Administrador/templates/Noticias.html')

#nuevo#################################33
@app.route('/circulares')
@login_required
def circulares():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template('Administrador/templates/Circulares.html', files=files)


@app.route('/noticias_vistas')
def noticias_vistas():
    return render_template('Administrador/templates/NoticiasVistas.html')

@app.route('/usuarios')
def usuarios():
    return render_template('Administrador/templates/Usuarios.html')

@app.route('/asignaturas')
def asignaturas():
    return render_template('Administrador/templates/Asignaturas.html')

@app.route('/horarios')
def horarios():
    return render_template('Administrador/templates/Horarios.html')

@app.route('/registro_notas/<int:curso_id>')
def registro_notas(curso_id):
    return render_template('Administrador/templates/RegistroNotas.html', curso_id=curso_id)

#Conexión de los cursos
@app.route('/notas/<int:curso_id>')
def notas_curso(curso_id):
    return render_template("Administrador/templates/notas_curso.html", curso_id=curso_id)


@app.route('/notasr')
def notasr():
    return render_template('Administrador/templates/NotasR.html')
>>>>>>> f968ce65124a6f032d20c4e2957637b2da2aae63

@app.route('/verpromedio')
def verpromedio():
    return render_template('Administrador/templates/VerPromedio.html')

@app.route('/calculopromedio/<int:curso_id>')
def calculopromedio(curso_id):
    return render_template('Administrador/templates/CalculoPromedio.html', curso_id=curso_id)


@app.route('/crear_encuesta')
def crear_encuesta():
    return render_template('Administrador/templates/CrearEncuesta.html')

@app.route('/editar_eliminar_encuesta')
def editar_eliminar_encuesta():
    return render_template('Administrador/templates/EditarEliminarEncuesta.html')

@app.route('/resultados_encuesta')
def resultados_encuesta():
    return render_template('Administrador/templates/ResultadosEncuesta.html')



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('Nombre')
        apellido = request.form.get('Apellido')
        correo = request.form.get('Correo')
        contrasena = request.form.get('Contrasena')
        numero_documento = request.form.get('NumeroDocumento')
        telefono = request.form.get('Telefono')
        direccion = request.form.get('Direccion')
        rol = request.form.get('Rol')

        tipo_documento = request.form.get('TipoDocumento', 'CC')
        estado = request.form.get('Estado', 'Activo')
        genero = request.form.get('Genero', '')

        if not all([nombre, apellido, correo, contrasena, numero_documento, telefono, direccion, rol]):
            flash('Por favor, completa todos los campos requeridos.')
            return render_template('Administrador/templates/Registro.html')

        try:
            existing_user = Usuario.query.filter_by(Correo=correo).first()
            if existing_user:
                flash('El correo ya está registrado.')
                return render_template('Administrador/templates/Registro.html')

            hashed_password = generate_password_hash(contrasena)
            
            new_user = Usuario(
                Nombre=nombre,
                Apellido=apellido,
                Correo=correo,
                Contrasena=hashed_password,
                TipoDocumento=tipo_documento,
                NumeroDocumento=numero_documento,
                Telefono=telefono,
                Direccion=direccion,
                Rol=rol,
                Estado=estado,
                Genero=genero
            )
            
            
            db.session.add(new_user)
            db.session.commit()

            flash('Cuenta creada exitosamente. Inicia sesión.')
            return redirect(url_for('login'))
        
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error al registrar: {str(e)}')
            return render_template('Administrador/templates/Registro.html')

    return render_template('Administrador/templates/Registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['email']
        contrasena = request.form['password']
        
        usuario = Usuario.query.filter_by(Correo=correo).first()

        if usuario and check_password_hash(usuario.Contrasena, contrasena):
            login_user(usuario)

            # Redirigir según rol
            if usuario.Rol == 'Administrador':
                return redirect(url_for('Administrador.paginainicio'))
            elif usuario.Rol == 'Docente':
                return redirect(url_for('Docente.paginainicio'))
            elif usuario.Rol == 'Estudiante':
                return redirect(url_for('Estudiante.paginainicio'))
            elif usuario.Rol == 'Acudiente':
                return redirect(url_for('Acudiente.paginainicio'))
        else:
            flash("Correo o contraseña incorrectos", "danger")

    return render_template('Login.html')




@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.')
    return redirect(url_for('index'))


app.register_blueprint(Administrador_bp)
app.register_blueprint(Docente_bp)
app.register_blueprint(Estudiante_bp)
app.register_blueprint(Acudiente_bp)

#nuevox2
@app.route("/api/notificaciones")
@login_required
def api_notificaciones():
    notificaciones = Notificacion.query.filter_by(ID_Usuario=current_user.ID_Usuario).order_by(Notificacion.Fecha.desc()).all()
    
    data = [
        {
            "id": n.ID_Notificacion,
            "titulo": n.Titulo,
            "mensaje": n.Mensaje,
            "enlace": n.Enlace,
            "estado": n.Estado,
            "fecha": n.Fecha.strftime("%d/%m/%Y %H:%M")
        }
        for n in notificaciones
    ]
    
    return jsonify(data)


#nuevo
@app.route("/subir_circular", methods=["POST"])
@login_required
def subir_circular():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No se envió archivo"})
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Archivo sin nombre"})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)


    return jsonify({"success": True, "filename": filename})







#esto es lo de fredy :D
# --------------------- API REST ---------------------

# ----------- USUARIOS -----------
@app.route('/api/usuarios', methods=['GET'])
def api_get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        "id": u.ID_Usuario,
        "nombre": u.Nombre,
        "apellido": u.Apellido,
        "correo": u.Correo,
        "rol": u.Rol
    } for u in usuarios])

@app.route('/api/usuarios', methods=['POST'])
def api_create_usuario():
    data = request.json
    try:
        nuevo = Usuario(
            Nombre=data['nombre'],
            Apellido=data['apellido'],
            Correo=data['correo'],
            Contrasena=generate_password_hash(data.get('contrasena', "123456")),
            TipoDocumento=data.get("TipoDocumento", "CC"),
            NumeroDocumento=data.get("NumeroDocumento", ""),
            Telefono=data.get("Telefono", ""),
            Rol=data.get("rol", "Estudiante"),
            Estado="Activo",
            Direccion=data.get("Direccion", ""),
            Genero=data.get("Genero", "Otro")
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"mensaje": "Usuario creado", "id": nuevo.ID_Usuario}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/usuarios/<int:id>', methods=['PUT'])
def api_update_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = request.json
    usuario.Nombre = data.get("nombre", usuario.Nombre)
    usuario.Apellido = data.get("apellido", usuario.Apellido)
    usuario.Correo = data.get("correo", usuario.Correo)
    usuario.Telefono = data.get("telefono", usuario.Telefono)
    db.session.commit()
    return jsonify({"mensaje": "Usuario actualizado"})

@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
def api_delete_usuario(id):
    try:
        db.session.execute(text("DELETE FROM Usuario WHERE ID_Usuario = :id"), {"id": id})
        db.session.commit()
        return jsonify({"mensaje": "Usuario eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ----------- DOCENTES -----------
@app.route('/api/docentes', methods=['GET'])
def api_get_docentes():
    docentes = Usuario.query.filter_by(Rol='Docente').all()
    return jsonify([{
        "id": d.ID_Usuario,
        "nombre": d.Nombre,
        "apellido": d.Apellido,
        "correo": d.Correo
    } for d in docentes])

@app.route('/api/docentes', methods=['POST'])
def api_create_docente():
    data = request.json
    try:
        nuevo = Usuario(
            Nombre=data['nombre'],
            Apellido=data['apellido'],
            Correo=data['correo'],
            Contrasena=generate_password_hash("123456"),
            TipoDocumento="CC",
            NumeroDocumento=data.get("numero_doc", ""),
            Telefono=data.get("telefono", ""),
            Rol="Docente",
            Estado="Activo",
            Direccion="",
            Genero="Otro"
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"mensaje": "Docente creado", "id": nuevo.ID_Usuario}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/docentes/<int:id>', methods=['PUT'])
def api_update_docente(id):
    docente = Usuario.query.get_or_404(id)
    data = request.json
    docente.Nombre = data.get("nombre", docente.Nombre)
    docente.Apellido = data.get("apellido", docente.Apellido)
    docente.Correo = data.get("correo", docente.Correo)
    db.session.commit()
    return jsonify({"mensaje": "Docente actualizado"})

@app.route('/api/docentes/<int:id>', methods=['DELETE'])
def api_delete_docente(id):
    try:
        db.session.execute(text("DELETE FROM Usuario WHERE ID_Usuario = :id AND Rol='Docente'"), {"id": id})
        db.session.commit()
        return jsonify({"mensaje": "Docente eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ----------- ESTUDIANTES -----------
@app.route('/api/estudiantes', methods=['GET'])
def api_get_estudiantes():
    estudiantes = Usuario.query.filter_by(Rol='Estudiante').all()
    return jsonify([{
        "id": e.ID_Usuario,
        "nombre": e.Nombre,
        "apellido": e.Apellido,
        "correo": e.Correo
    } for e in estudiantes])

@app.route('/api/estudiantes', methods=['POST'])
def api_create_estudiante():
    data = request.json
    try:
        nuevo = Usuario(
            Nombre=data['nombre'],
            Apellido=data['apellido'],
            Correo=data['correo'],
            Contrasena=generate_password_hash("123456"),
            TipoDocumento="CC",
            NumeroDocumento=data.get("numero_doc", ""),
            Telefono=data.get("telefono", ""),
            Rol="Estudiante",
            Estado="Activo",
            Direccion="",
            Genero="Otro"
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"mensaje": "Estudiante creado", "id": nuevo.ID_Usuario}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/estudiantes/<int:id>', methods=['PUT'])
def api_update_estudiante(id):
    estudiante = Usuario.query.get_or_404(id)
    data = request.json
    estudiante.Nombre = data.get("nombre", estudiante.Nombre)
    estudiante.Apellido = data.get("apellido", estudiante.Apellido)
    estudiante.Correo = data.get("correo", estudiante.Correo)
    db.session.commit()
    return jsonify({"mensaje": "Estudiante actualizado"})

@app.route('/api/estudiantes/<int:id>', methods=['DELETE'])
def api_delete_estudiante(id):
    try:
        db.session.execute(text("DELETE FROM Usuario WHERE ID_Usuario = :id AND Rol='Estudiante'"), {"id": id})
        db.session.commit()
        return jsonify({"mensaje": "Estudiante eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ----------- ACUDIENTES -----------
@app.route('/api/acudientes', methods=['GET'])
def api_get_acudientes():
    acudientes = Usuario.query.filter_by(Rol='Acudiente').all()
    return jsonify([{
        "id": a.ID_Usuario,
        "nombre": a.Nombre,
        "apellido": a.Apellido,
        "correo": a.Correo
    } for a in acudientes])

@app.route('/api/acudientes', methods=['POST'])
def api_create_acudiente():
    data = request.json
    try:
        nuevo = Usuario(
            Nombre=data['nombre'],
            Apellido=data['apellido'],
            Correo=data['correo'],
            Contrasena=generate_password_hash("123456"),
            TipoDocumento="CC",
            NumeroDocumento=data.get("numero_doc", ""),
            Telefono=data.get("telefono", ""),
            Rol="Acudiente",
            Estado="Activo",
            Direccion=data.get("direccion", ""),
            Genero="Otro"
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"mensaje": "Acudiente creado", "id": nuevo.ID_Usuario}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/acudientes/<int:id>', methods=['PUT'])
def api_update_acudiente(id):
    acudiente = Usuario.query.get_or_404(id)
    data = request.json
    acudiente.Nombre = data.get("nombre", acudiente.Nombre)
    acudiente.Apellido = data.get("apellido", acudiente.Apellido)
    acudiente.Correo = data.get("correo", acudiente.Correo)
    db.session.commit()
    return jsonify({"mensaje": "Acudiente actualizado"})

@app.route('/api/acudientes/<int:id>', methods=['DELETE'])
def api_delete_acudiente(id):
    try:
        db.session.execute(text("DELETE FROM Usuario WHERE ID_Usuario = :id AND Rol='Acudiente'"), {"id": id})
        db.session.commit()
        return jsonify({"mensaje": "Acudiente eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
