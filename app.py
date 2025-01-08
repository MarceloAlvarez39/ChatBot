from flask import Flask, render_template, request, jsonify
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

TOKEN_CHATBOT = "CRYOB"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        challenge = verificar_token(request)
        return challenge
    elif request.method == 'POST':
        response = recibir_mensajes(request)
        return response

def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if challenge and token == TOKEN_CHATBOT:
        return challenge
    else:
        return jsonify({'error':'Token Invalido'}), 401

def recibir_mensajes(req):
    try:
        req = request.get_json()
        entry = req['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        objeto_mensaje = value['messages']
        # Si quisiera obtener el nombre del usuario, entraría en value["contacts"][0][profile][name]

        if objeto_mensaje:
            messages = objeto_mensaje[0]
            if "type" in messages:
                tipo = messages["type"]
                if tipo == "interactive":
                    return 0
                if "text" in messages:
                    text = messages["text"]["body"]
                    numero = messages["from"]


        agregar_mensajes_log(json.dups(text))
        agregar_mensajes_log(json.dups(numero))

        return jsonify({'messaje':'EVENT_RECEIVED'})
    except Exception as e:
        return jsonify({'messaje':'EVENT_RECEIVED'})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=80,debug=True)