from escpos.printer import Serial
from flask import Flask
from flask import request
from flask_cors import CORS
from news import news

app = Flask(__name__)
CORS(app, supports_credentials=True)

printer = Serial(devfile='COM1',
           baudrate=9600,
           bytesize=8,
           parity='N',
           stopbits=1,
           timeout=1.00,
           dsrdtr=True)

last_link=""

@app.route('/printPV', methods=["POST"])
def printpv():
    global last_link

    request_body=request.json

    if request_body["link"]==last_link:
        return "Already Printed"    
    last_link=request_body["link"]

    printer.image("Kassenzettel-Header.png")
    
    printer.text(news)

    printer.qr(request_body["link"],size=11)
    printer.text("\n"+request_body["link"]+"\n")
    printer.text("Dieser Link ist 7 Tage abrufbar.\n\n")

    printer.text("Viel Erfolg bei deinen Klausuren!\n")
    printer.text("Deine fachgruppe-informatik.de\n")

    printer.cut()
    return "ok"


app.run("0.0.0.0",port=6001)



"""
p.text("-----------------------------\n")

p.text("Web: fachgruppe-informatik.de\n")
p.text("Mail: fs@fius.informatik.uni-stuttgart.de\n")
p.text("Tel: 0711 / 685 88367\n")
"""
