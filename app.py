from flask import Flask,request,jsonify
from flask_mail import Message,Mail
import insert,ast,query

app=Flask(__name__)

app.config.update(
    DEBUG = True,
    MAIL_SERVER='smtp.qq.com',
    MAIL_PROT=25,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = "275959399@qq.com",
    MAIL_PASSWORD = "uzpvggxhqdllbgef",
    MAIL_DEBUG = False
)

mail=Mail(app)

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

#统计每天治疗人数
@app.route('/countTreatmentsPatientNumber',methods=['POST'])
def countTreatmentsPatientNumber():
    device_mac=request.form['device_mac']
    try:
        gender_nums=query.getTreatmentPatientNumber(device_mac)
        return jsonify(gender_nums)
    except:
        return jsonify({'status': 0})


#统计性别人数占比
@app.route('/countGendersProportion',methods=['POST'])
def countGendersProportion():
    device_mac = request.form['device_mac']
    try:
        gender_percent = query.getGenderPatientProportion(device_mac)
        return jsonify(gender_percent)
    except:
        return jsonify({'status': 0})



#统计第一分型人数占比
@app.route('/countTypesProportion',methods=['POST'])
def countTypesProportion():
    device_mac = request.form['device_mac']
    try:
        type_percent = query.getTypePatientProportion(device_mac)
        return jsonify(type_percent)
    except:
        return jsonify({'status': 0})


#统计年龄占比
@app.route('/countAgesProportion',methods=['POST'])
def countAgesProportion():
    device_mac = request.form['device_mac']
    try:
        age_percent = query.getAgePatientProportion(device_mac)
        return jsonify(age_percent)
    except:
        return jsonify({'status': 0})


#统计每位医生的患者数
@app.route('/countPerDoctorPatientNumber',methods=['POST'])
def countPerDoctorPatientNumber():
    device_mac=request.form['device_mac']
    try:
        perdoctor_patient_nums=query.getPerDoctorPatientNumber(device_mac)
        return jsonify(perdoctor_patient_nums)
    except:
        return jsonify({'status': 0})



#统计每种类型音乐数
@app.route('/countPerMusicNumber',methods=['POST'])
def countPerMusicNumber():
    try:
        permusic_nums=query.getPerMusicNumber()
        return jsonify(permusic_nums)
    except:
        return jsonify({'status': 0})


#统计整体疗效
@app.route('/countResultAll',methods=['POST'])
def countResultAll():
    device_mac = request.form['device_mac']
    try:
        result_all=query.getResultAll(device_mac)
        return jsonify(result_all)
    except:
        return jsonify({'status': 0})


# #下载单条数据
# @app.route('/downloadSingleData',methods=['POST'])
# def downloadSingleData():
#     patient_id=request.form['patient_id']

#发送邮件
#@app.route('/sendMail',methods=['POST'])
def downloadSingleData():
    patient_id=request.form['patient_id']
    msg = Message("Hi!This is a test ", sender='275959399@qq.com', recipients=['18019507168@163.com'])
    msg.body = "This is a first email"      # msg.body 邮件正文
    with app.open_resource("C:\\Users\\27595\\Desktop\\test.xlsx") as fp:
        msg.attach("test.xlsx", "text/xlsx", fp.read())                          # msg.attach 邮件附件添加,msg.attach("文件名", "类型", 读取文件）
    mail.send(msg)
    return jsonify({'status':1})


if __name__=='__main__':
    app.run(
        host='192.168.123.189',
        port=5000
    )