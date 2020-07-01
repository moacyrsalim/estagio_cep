import json
import sqlite3
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os

def home(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    cur = conn.cursor()
    cur.execute("SELECT * FROM tb_ceps;")
    zipcode_data = cur.fetchall()
    return render(request, 'home/index.html', {'zipcode_data': zipcode_data})

def api(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    cur = conn.cursor()


    zipcode = request.POST['zipcode'].replace("-", "")

    #Checa se existe no banco
    cur.execute("SELECT * FROM tb_ceps WHERE zipcode = '" + zipcode + "';")
    handle = cur.fetchall()

    if len(handle) > 0:
        z = handle[0]
        data = {
            "cep": z[1],
            "logradouro": z[2],
            "numero": z[3],
            "complemento": z[4],
            "bairro": z[5],
            "localidade": z[6],
            "uf": z[7]
        }
        data = json.dumps(data)
    else:
        url = "https://viacep.com.br/ws/" + zipcode + "/json/"
        f = requests.get(url)
        data = f.text

    return HttpResponse(data)

def register_zipcode(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    cur = conn.cursor()

    zipcode = request.POST['zipcode'].replace("-", "")
    address = request.POST['address']
    number = request.POST['number']
    complement = request.POST['complement']
    neighborhood = request.POST['neighborhood']
    city = request.POST['city']
    state = request.POST['state']

    # Checa se existe no banco
    cur.execute("SELECT * FROM tb_ceps WHERE zipcode = '" + zipcode + "';")
    handle = cur.fetchall()

    if len(handle) > 0:
        sql = "UPDATE tb_ceps SET address = ?, number = ?, complement = ?, neighborhood = ?, city = ?, state = ? WHERE zipcode = ?"
        cur.execute(sql, (address, number, complement, neighborhood, city, state, zipcode))
        conn.commit()
    else:
        sql = "INSERT INTO tb_ceps (zipcode, address, number, complement, neighborhood, city, state) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cur.execute(sql, (zipcode, address, number, complement, neighborhood, city, state))
        conn.commit()

    return JsonResponse({"response": True})
