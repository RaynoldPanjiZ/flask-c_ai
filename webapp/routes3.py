from flask import Flask, request, jsonify, render_template
import mariadb
import sys

app = Flask(__name__)


try:
    # connection parameters
    conn_params = {
        'user' : "root",
        'password' : "test123",
        'host' : "127.0.0.1",
        'port' : 3306,
        'database' : "construct_ai"
    }

    # establish a connection
    connection = mariadb.connect(**conn_params)
    cursor = connection.cursor()
    
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

@app.route('/')
def index():
    return "test"


# @app.route('/fetch_all', methods=['GET', 'POST'])
# def get_fetch_all():
#     datas = ref.get()

#     data_res = {'status':'success','data': datas}
#     return jsonify(data_res)


@app.route('/smartphone_info/<action>', methods=['GET', 'POST'])
def get_smartphone_info(action):
    if request.method == 'GET':     # http://localhost:5000/smartphone_info/get
        cursor.execute("SELECT * FROM app_status")
        columns = cursor.description 
        datas = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]


        data_res = {'status':'success','data': datas}
        res = jsonify(data_res)
        res.headers.add("Access-Control-Allow-Origin", "*") 
        return res

    elif request.method == 'POST':      # http://localhost:5000/smartphone_info/edit
        try:
            content = request.json
            id = content['_id']
            username = content['username']
            phone = content['phone']
            site = content['site']
            status = content['status']
            operation = content['operation']
            version = content['version']

            cursor.execute(
                f"UPDATE `construct_ai`.`app_status` SET \
                    `username`='{username}', `phone`='{phone}', `site`='{site}', `status`='{status}', `operation`='{operation}', `version`='{version}' \
                        WHERE `_id`={id};")
            connection.commit()
            
            data_res = {'status':'success','message': 'Data updated!'}
            # print(datas)
            res = jsonify(data_res)
            res.headers.add("Access-Control-Allow-Origin", "*") 
            return res

        except Exception as e:
            data_res = {'status':'Failed','message': f'Error update: {e}'}
            print('fail')
            res = jsonify(data_res)
            res.headers.add("Access-Control-Allow-Origin", "*") 
            return res


@app.route('/system_log/<action>', methods=['GET', 'POST'])
def get_system_log(action):
    if request.method == 'GET':         # http://localhost:5000/system_log/get
        cursor.execute("SELECT * FROM system_log")
        columns = cursor.description 
        datas = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]

        data_res = {'status':'success','data': datas}
        res = jsonify(data_res)
        res.headers.add("Access-Control-Allow-Origin", "*") 
        return res

    
    elif request.method == 'POST':
        if action == "delete":             # http://localhost:5000/system_log/deelete
            try:
                #set data
                content = request.json
                id = content['_id']
                
                query = "DELETE FROM system_log WHERE _id = %s"
                cursor.execute(query, (id,))
                connection.commit()
                
                data_res = {'status':'success','message': 'Data Deleted!'}
                # print(datas)
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res

            except Exception as e:
                data_res = {'status':'Failed','message': f'Error delete: {e}'}
                print('fail')
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res


@app.route('/construction_scope/<action>', methods=['GET', 'POST'])
def get_construction_scope(action):
    if request.method == 'GET':         # http://localhost:5000/construction_scope/get
        cursor.execute("SELECT * FROM construction_site")
        columns = cursor.description 
        datas = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]

        data_res = {'status':'success','data': datas}
        res = jsonify(data_res)
        res.headers.add("Access-Control-Allow-Origin", "*") 
        return res

    elif request.method == 'POST':
        if action == "add":             # http://localhost:5000/construction_scope/deelete
            try:
                # autoincrement data index
                cursor.execute("SELECT _id FROM construction_site ORDER BY _id DESC LIMIT 1;")
                for dat in cursor.fetchall():
                    last_id = dat[0] + 1

                #set data
                content = request.json
                id = last_id
                site = content['site']
                manager_name = content['manager_name']
                phone = content['phone']
                latitude = content['latitude']
                longitude = content['longitude']
                horizontal = content['horizontal']
                vertical = content['vertical']
                
                insert_query = f"INSERT INTO construction_site \
                    (_id, site, manager_name, phone, latitude, longitude, horizontal, vertical) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                data = (id, site, manager_name, phone, latitude, longitude, horizontal, vertical)
                cursor.execute(insert_query, data)
                connection.commit()
                
                data_res = {'status':'success','message': 'Data updated!'}
                # print(datas)
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res

            except Exception as e:
                data_res = {'status':'Failed','message': f'Error update: {e}'}
                print('fail')
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res

            
        elif action == "edit":          # http://localhost:5000/construction_scope/edit
            try:
                content = request.json
                id = content['_id']
                site = content['site']
                manager_name = content['manager_name']
                phone = content['phone']
                latitude = content['latitude']
                longitude = content['longitude']
                horizontal = content['horizontal']
                vertical = content['vertical']

                cursor.execute(
                    f"UPDATE `construct_ai`.`construction_site` SET \
                        `manager_name`='{manager_name}', `phone`='{phone}', `site`='{site}', `latitude`='{latitude}', `longitude`='{longitude}', `horizontal`='{horizontal}', `vertical`='{vertical}' \
                            WHERE `_id`={id};")
                connection.commit()
                
                data_res = {'status':'success','message': 'Data updated!'}
                # print(datas)
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res

            except Exception as e:
                data_res = {'status':'Failed','message': f'Error update: {e}'}
                print('fail')
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res

        
        elif action == "delete":             # http://localhost:5000/construction_scope/deelete
            try:
                #set data
                content = request.json
                id = content['_id']
                
                query = "DELETE FROM construction_scope WHERE _id = %s"
                cursor.execute(query, (id,))
                connection.commit()
                
                data_res = {'status':'success','message': 'Data Deleted!'}
                # print(datas)
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res

            except Exception as e:
                data_res = {'status':'Failed','message': f'Error delete: {e}'}
                print('fail')
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res



@app.route('/notif_setting/<action>', methods=['GET', 'POST'])
def get_notif_setting(action):
    if request.method == 'GET':             # http://localhost:5000/notif_setting/get
        cursor.execute("SELECT * FROM notif_setting")
        columns = cursor.description 
        datas = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]

        data_res = {'status':'success','data': datas}
        res = jsonify(data_res)
        res.headers.add("Access-Control-Allow-Origin", "*") 
        return res

    elif request.method == 'POST':
        if action == "add":                 # http://localhost:5000/notif_setting/add
            try:
                # autoincrement data index
                cursor.execute("SELECT _id FROM notif_setting ORDER BY _id DESC LIMIT 1;")
                for dat in cursor.fetchall():
                    last_id = dat[0] + 1

                #set data
                content = request.json
                id = last_id
                site = content['site']
                title = content['title']
                danger_cat = content['danger_cat']
                type = content['type']
                date = content['date']
                time = content['time']
                
                
                insert_query = f"INSERT INTO notif_setting \
                    (_id, site, title, danger_cat, type, date, time) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data = (id, site, title, danger_cat, type, date, time)
                cursor.execute(insert_query, data)
                connection.commit()
                
                data_res = {'status':'success','message': 'Data updated!'}
                # print(datas)
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res

            except Exception as e:
                data_res = {'status':'Failed','message': f'Error update: {e}'}
                print('fail')
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res

            
        elif action == "edit":              # http://localhost:5000/notif_setting/edit
            try:
                content = request.json
                id = content['_id']
                site = (content['site'])
                title = (content['title'])
                danger_cat = (content['danger_cat'])
                type = (content['type'])
                date = (content['date'])
                time = (content['time'])
                
                cursor.execute(
                    f"UPDATE `construct_ai`.`notif_setting` SET \
                        `site`='{site}', `title`='{title}', `danger_cat`='{danger_cat}', `type`='{type}', `date`='{date}', `time`='{time}' \
                            WHERE `_id`={id};")
                connection.commit()
                
                data_res = {'status':'success','message': 'Data updated!'}
                # print(datas)
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res

            except Exception as e:
                data_res = {'status':'Failed','message': f'Error update: {e}'}
                print('fail')
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res

            
        elif action == "delete":             # http://localhost:5000/construct_ai/deelete
            try:
                #set data
                content = request.json
                id = content['_id']
                
                query = "DELETE FROM construct_ai WHERE _id = %s"
                cursor.execute(query, (id,))
                connection.commit()
                
                data_res = {'status':'success','message': 'Data Deleted!'}
                # print(datas)
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res

            except Exception as e:
                data_res = {'status':'Failed','message': f'Error delete: {e}'}
                print('fail')
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res
