from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)

#Configuraciond e la base d edatos SQLITE
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///metapyhon.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Modelo de la tabla log
class Log(db.Model):
    format = '%a %d %b %Y, %I:%M%p'
    
    date = datetime.now().strftime(format)
    
    id = db.Column(db.Integer,primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, default=datetime.strptime(date, format))
    texto = db.Column(db.TEXT)

#Funcion para ordenar los registros por fecha y hora
def ordenar_por_fecha_y_hora(registros):
    return sorted(registros, key=lambda x: x.fecha_y_hora,reverse=True)

#Crear tabla si no existe
with app.app_context():
    #db.drop_all()
    db.create_all()


@app.route('/')




def index():
    # Obtener todos los registros de la base de datos
    registros = Log.query.all()
    registros_ordenados = ordenar_por_fecha_y_hora(registros)
    return render_template('index.html', registros=registros_ordenados)


mensajes_log = []
# Funcion para agregar mensajes y guardar en la base de datos
def agregar_mensajes_log(texto):
    mensajes_log.append(texto)

    # Guardar el mensaje en la base de datos
    nuevo_registro = Log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit()

#agregar_mensajes_log("Test 111")

if __name__=='__main__':
    app.run(host='0.0.0.0',port=80,debug=True)