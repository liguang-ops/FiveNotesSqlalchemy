from flask import Flask,request,jsonify
import insert,ast,query

app=Flask(__name__)

#插入设备信息
@app.route('/addDevice',methods=['POST'])
def addDevice():
    device_mac = request.form['device_mac']
    device_id=insert.insertDevice({'device_mac':device_mac})
    if device_id !=None:
        return jsonify({'status':1})
    else:
        return jsonify({'status':0})



#同步设备端所有病人信息至云端
@app.route('/syncAllPatientsInfo',methods=['POST'])
def syncAllPatientsInfo():
    data = request.form['patients']
    device_mac = request.form['device_mac']
    if data!='':
        patients=ast.literal_eval(data)
        try:
            for patient in patients:
                doctor_id=insert.insertDoctor(patient['doctor'],device_mac)
                if doctor_id != None:
                    patient_id=insert.insertPatient(patient,device_mac)
                    if patient_id !=None:
                        insert.insertTreatments(patient.get('treats',None),patient_id)
                        insert.insertGrades(patient.get('grades',None),patient_id)
            return jsonify({'status':1})
        except:
            return jsonify({'status':0})
    else:
        return jsonify({'status':2})


#获取所有患者信息
@app.route('/queryConsultationList',methods=['POST'])
def queryConsultationList():
    device_mac = request.form['device_mac']
    try:
        patients_info = query.getAllPatientsInfo(device_mac)
        return jsonify(patients_info)
    except:
        return jsonify({'status':0})

#统计每天就诊人数
@app.route('/countTreatmentsPatientNumber',methods=['POST'])
def countTreatmentsPatientNumber():
    device_mac=request.form['device_mac']
    try:
        date_result=query.getTreatmentPatientNumber(device_mac)
        return jsonify(date_result)
    except:
        return jsonify({'status': 0})

if __name__=='__main__':
    app.run(
        host='192.168.123.189',
        port=5000
    )