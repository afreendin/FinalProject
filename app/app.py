from typing import List, Dict
import mysql.connector
import simplejson as json
# import str as str
from flask import Flask, Response, request, redirect
from flask import render_template

app = Flask(__name__ , template_folder='templates')

from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_USER'] = 'afu2'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'citiesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Cities Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cities=result)


@app.route('/view/<string:city_id>', methods=['GET'])
def view(city_id):
    cursor = mysql.get_db().cursor()
    # id = city_id.id
    # id = request.args.get('city_id')
    # id = request.form('city_id')
    cursor.execute('SELECT * FROM tblCitiesImport WHERE fldName= %s', city_id)
    result = cursor.fetchall()
    # return render_template('view.html', title='View Form', city=result[0], id= city_id)  # main
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<string:fldName>', methods=['GET'])
def form_edit_get(fldName):
    # return render_template('edit1.html', title='Edit Form', city= city_id)
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE fldName= %s', fldName)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<string:fldName>', methods=['POST'])
def form_update_post(fldName):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldLat'), request.form.get('fldLong'),
                 request.form.get('fldCountry'), request.form.get('fldAbreviation'),
                 request.form.get('fldCapitalStatus'), request.form.get('fldPopulation'), fldName)
    sql_update_query = """UPDATE tblCitiesImport t SET t.fldName = %s, t.fldLat = %s, t.fldLong = %s, t.fldCountry =
    %s, t.fldAbreviation = %s, t.fldCapitalStatus = %s, t.fldPopulation = %s WHERE t.fldName = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    cursor.close()
    return redirect("/", code=302)


@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New City Form')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldLat'), request.form.get('fldLong'),
                 request.form.get('fldCountry'), request.form.get('fldAbreviation'),
                 request.form.get('fldCapitalStatus'), request.form.get('fldPopulation'))
    sql_insert_query = """INSERT INTO tblCitiesImport (fldName,fldLat,fldLong,fldCountry,fldAbreviation,fldCapitalStatus,fldPopulation) VALUES (%s, %s,%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<string:fldName>', methods=['POST'])
def form_delete_post(fldName):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblCitiesImport WHERE fldName = %s """
    cursor.execute(sql_delete_query, fldName)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['GET'])
def api_retrieve(city_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE fldName=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['PUT'])
def api_edit(city_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/cities/<int:city_id>', methods=['DELETE'])
def api_delete(city_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp



if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(host='0.0.0.0', port=5070)
