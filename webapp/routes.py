from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, db
import threading

app = Flask(__name__)


cred = credentials.Certificate("webapp/firebase-credential.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://construction-ai-64c04-default-rtdb.firebaseio.com'  # Ganti dengan URL Realtime Database Anda
})

ref = db.reference("/") 


# print(ref.get()["construction_site"])

@app.route('/')
def index():
    return "test"


@app.route('/fetch_all', methods=['GET', 'POST'])
def get_fetch_all():     # http://localhost:5000/fetch_all
    datas = ref.get()

    data_res = {'status':'success','data': datas}
    
    res = jsonify(data_res)
    res.headers.add("Access-Control-Allow-Origin", "*") 
    return res


@app.route('/smartphone_info/<action>', methods=['GET', 'POST'])
def get_smartphone_info(action):
    if request.method == 'GET':     # http://localhost:5000/smartphone_info/get
        datas = ref.get()["app_status"]

        data_res = {'status':'success','data': datas}
        res = jsonify(data_res)
        res.headers.add("Access-Control-Allow-Origin", "*") 
        return res
    elif request.method == 'POST':     # http://localhost:5000/smartphone_info/edit
        try:
            content = request.json
            id = content['id']
            username = content['username']
            phone = content['phone']
            site = content['site']
            status = content['status']
            operation = content['operation']
            version = content['version']

            datas = {
                'username': username,
                'phone': phone,
                'site': site,
                'status': status,
                'operation': operation,
                'version': version
            }

            ref_update = db.reference(f"/app_status/{id}")
            ref_update.update(datas)
            
            data_res = {'status':'success','message': 'Data updated!'}
            print(datas)
            
            res = jsonify(data_res)
            res.headers.add("Access-Control-Allow-Origin", "*") 
            return res
        except Exception as e:
            print('fail:', e)
            data_res = {'status':'Failed','message': f'Error update: {e}'}
            res = jsonify(data_res)
            res.headers.add("Access-Control-Allow-Origin", "*") 
            return res

@app.route('/system_log/<action>', methods=['GET', 'POST'])
def get_system_log(action):        # http://localhost:5000/system_log/get
    if request.method == 'GET':
        datas = ref.get()["system_log"]

        data_res = {'status':'success','data': datas}

        res = jsonify(data_res)
        res.headers.add("Access-Control-Allow-Origin", "*") 
        return res


@app.route('/construction_scope/<action>', methods=['GET', 'POST'])
def get_construction_scope(action):
    if request.method == 'GET':       # http://localhost:5000/construction_scope/get
        datas = ref.get()["construction_site"]
        # print(datas)
        data_res = {'status':'success','data': datas}
        res = jsonify(data_res)
        res.headers.add("Access-Control-Allow-Origin", "*") 
        return res
    elif request.method == 'POST':
        if action == "add":             # http://localhost:5000/construction_scope/add
            try:
                # autoincrement data index
                with threading.Lock():
                    counter_ref = db.reference('/construction_site')
                    get_datas = counter_ref.get()
                    current_counter = len(get_datas)
                    if get_datas is None:
                        current_counter = 0

                #set data
                content = request.json
                site = content['site']
                manager_name = content['manager_name']
                phone = content['phone']
                latitude = content['latitude']
                longitude = content['longitude']
                horizontal = content['horizontal']
                vertical = content['vertical']
                
                datas = {
                    current_counter : {
                        'manager_name': manager_name,
                        'phone': phone,
                        'site': site,
                        'latitude': latitude,
                        'longitude': longitude,
                        'horizontal': horizontal,
                        'vertical': vertical
                    }
                }

                ref_update = db.reference(f"/construction_site")
                ref_update.update(datas)
                
                print(datas)
                data_res = {'status':'success','message': 'Data updated!'}
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res
            except Exception as e:
                print('fail:', e)
                data_res = {'status':'Failed','message': f'Error update: {e}'}
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res
            
        elif action == "edit":          # http://localhost:5000/construction_scope/edit
            try:
                content = request.json
                id = content['id']
                site = content['site']
                manager_name = content['manager_name']
                phone = content['phone']
                latitude = content['latitude']
                longitude = content['longitude']
                horizontal = content['horizontal']
                vertical = content['vertical']

                datas = {
                    'manager_name': manager_name,
                    'phone': phone,
                    'site': site,
                    'latitude': latitude,
                    'longitude': longitude,
                    'horizontal': horizontal,
                    'vertical': vertical
                }

                ref_update = db.reference(f"/construction_site/{id}")
                ref_update.update(datas)
                
                print(datas)
                data_res = {'status':'success','message': 'Data updated!'}
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res
            except Exception as e:
                print('fail:', e)
                data_res = {'status':'Failed','message': f'Error update: {e}'}
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res



@app.route('/notif_setting/<action>', methods=['GET', 'POST'])
def get_notif_setting(action):
    if request.method == 'GET':             # http://localhost:5000/notif_setting/get
        datas = ref.get()["notif_setting"]
        # print(datas)
        data_res = {'status':'success','data': datas}
        res = jsonify(data_res)
        res.headers.add("Access-Control-Allow-Origin", "*") 
        return res
    elif request.method == 'POST':
        if action == "add":                 # http://localhost:5000/notif_setting/add
            try:
                # autoincrement data index
                with threading.Lock():
                    counter_ref = db.reference('/notif_setting')
                    get_datas = counter_ref.get()
                    current_counter = len(get_datas)
                    if get_datas is None:
                        current_counter = 0
                    # counter_ref.set(current_counter)
                    # print('total:',len(current_counter))


                #set data
                content = request.json
                site = content['site']
                title = content['title']
                danger_cat = content['danger_cat']
                type = content['type']
                date = content['date']
                time = content['time']
                
                datas = {
                    current_counter : {
                        'site': site,
                        'title': title,
                        'danger_cat': danger_cat,
                        'type': type,
                        'date': date,
                        'time': time
                    }
                }

                ref_update = db.reference(f"/notif_setting")
                ref_update.update(datas)
                
                print(datas)
                data_res = {'status':'success','message': 'Data updated!'}
                
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res
            except Exception as e:
                print('fail:', e)
                data_res = {'status':'Failed','message': f'Error update: {e}'}
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res
            
        elif action == "edit":              # http://localhost:5000/notif_setting/edit
            try:
                content = request.json
                id = content['id']
                site = content['site']
                title = content['title']
                danger_cat = content['danger_cat']
                type = content['type']
                date = content['date']
                time = content['time']
                
                datas = {
                    'site': site,
                    'title': title,
                    'danger_cat': danger_cat,
                    'type': type,
                    'date': date,
                    'time': time
                }

                ref_update = db.reference(f"/notif_setting/{id}")
                ref_update.update(datas)
                
                print(datas)
                data_res = {'status':'success','message': 'Data updated!'}
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res
            except Exception as e:
                print('fail:', e)
                data_res = {'status':'Failed','message': f'Error update: {e}'}
                res = jsonify(data_res)
                res.headers.add("Access-Control-Allow-Origin", "*") 
                return res