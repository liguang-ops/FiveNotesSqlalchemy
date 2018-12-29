from tables import Doctor,Patient,Treatment,Grade,Device,SessionClass
import ast


#@ brief插入设备信息
#@ param deviceInfo 设备信息（字典）
#@ return device_id 设备id
def insertDevice(deviceInfo):
    session = SessionClass()
    device=session.query(Device).filter(Device.device_mac==deviceInfo['device_mac']).first()
    if device == None:
        device_new = Device()
        device_new.device_mac = deviceInfo['device_mac']
        device_new.device_img = deviceInfo.get('device_img', None)
        device_new.device_name = deviceInfo.get('device_name', None)
        device_new.device_department = deviceInfo.get('device_department', None)
        try:
            session.add(device_new)
            session.flush()
            device_new_id = device_new.device_id
            session.commit()
            session.close()
            return device_new_id
        except:
            session.rollback()
            return None
    else:
        session.close()
        return device.device_id


#@ brief 插入医生信息
#@ param (doctor_name,device_mac) (医生姓名，设备mac) (字典,string)
#@ return doctor_id 医生id
def insertDoctor(doctor_name,device_mac):
    session = SessionClass()
    device = session.query(Device).filter(Device.device_mac == device_mac).first()
    doctor = session.query(Doctor).filter(Doctor.device_id == device.device_id,Doctor.doctor_name==doctor_name).first()
    if doctor==None:
        doctor_new=Doctor()
        doctor_new.doctor_name=doctor_name
        doctor_new.device_id=device.device_id
        try:
            session.add(doctor_new)
            session.flush()
            doctor_new_id=doctor_new.doctor_id
            session.commit()
            session.close()
            #device=session.query(Doctor).filter(Doctor.doctor_id==doctor_new_id).first()
            return doctor_new_id
        except:
            session.rollback()
            return None
    else:
        session.close()
        return doctor.doctor_id


#@ brief 插入患者信息
#@ param (patientInfo,device_mac) (患者信息，设备mac）（dict,list)
#@ return patient_id 患者id
def insertPatient(patientInfo,device_mac):
    session = SessionClass()
    device = session.query(Device).filter(Device.device_mac == device_mac).first()
    patient = session.query(Patient).filter(Patient.patient_age == patientInfo['age'],
                                               Patient.patient_gender == patientInfo['gender'],
                                               Patient.patient_name == patientInfo['name'],
                                               Patient.device_id == device.device_id).first()
    doctor_id = insertDoctor(patientInfo['doctor'], device_mac)
    if doctor_id != None:
        if patient==None:
            patient_new=Patient()
            patient_new.patient_name=patientInfo['name']
            patient_new.patient_gender = patientInfo['gender']
            patient_new.patient_age = patientInfo['age']
            patient_new.patient_self_reported = patientInfo.get('report', None)
            patient_new.patient_medical_history = patientInfo.get('history', None)
            patient_new.patient_examination = patientInfo.get('inspect', None)
            patient_new.patient_device_category = patientInfo['cate']
            #patient_new.patient_doctor_category1 = patientInfo['dcate1']
            patient_new.patient_doctor_category1 = patientInfo['cate']
            patient_new.patient_doctor_category2 = patientInfo.get('dcate2',None)
            patient_new.device_id=device.device_id
            patient_new.doctor_id=doctor_id
            try:
                session.add(patient_new)
                session.flush()
                patient_new_id=patient_new.patient_id
                session.commit()
                session.close()
                return patient_new_id
            except:
                session.rollback()
                return None
        else:
            if 'report' in patientInfo:
                patient.patient_self_reported = patientInfo['report']
            if 'history' in patientInfo:
                patient.patient_medical_history = patientInfo['history']
            if 'inspect' in patientInfo:
                patient.patient_examination = patientInfo['inspect']
            if 'dcate1' in patientInfo:
                patient.patient_examination = patientInfo['dcate1']
            if 'dcate2' in patientInfo:
                patient.patient_examination = patientInfo['dcate2']
            patient_id=patient.patient_id
            session.commit()
            session.close()
            return patient_id
    else:
        session.close()
        return None


#@ brief 插入治疗信息
#@ param (treatmentsInfo,patient_id) (治疗信息,患者编号）（list,int）
#@ return
def insertTreatments(treatments,patient_id):
    session = SessionClass()
    if (treatments != None):
        treatment_count = session.query(Treatment).filter(Treatment.patient_id == patient_id).count()
        if (treatment_count <= 100):
            for treatment in treatments:
                #session.add(Treatment(treatment_time=treatment['ts'],patient_id=patient_id,music_id=treatment['music']))
                session.add(Treatment(treatment_time=treatment['ts'], patient_id=patient_id))
                session.commit()
        session.close()
    return


#@ brief 插入分级信息
#@ param  (gradesInfo,patient_id) (分级信息,患者编号）（list,int）
#@ return
def insertGrades(grades,patient_id):
    session = SessionClass()
    if (grades != None):
        grade_count = session.query(Grade).order_by(Grade.grade_time.desc()).filter(Grade.patient_id == patient_id).count()
        if (grade_count <= 100):
            for grade in grades:
                session.add(Grade(grade_level=grade['grade'], grade_score=grade['score'], grade_time=grade['ts'],
                                     patient_id=patient_id))
            session.commit()
        session.close()
    return


if __name__=='__main__':
    data = "[{'age': 56, 'treats': [{'ts': 1542097122}], 'doctor': '张大伟', 'history': '舌淡红，苔薄白', 'cate': 3, 'inspect': '声阻抗正常，鼓膜正常', 'gender': 1, 'name': '张三', 'report': '右耳耳鸣1年', 'grades': [{'ts': 1542097122, 'score': 12, 'grade': 3}]}, {'age': 42, 'treats': [{'ts': 1542097122}, {'ts': 1542097122}], 'doctor': '王小燕', 'cate': 4, 'gender': 2, 'name': '李四'}, {'age': 42, 'cate': 2, 'gender': 1, 'doctor': '张大伟', 'name': '王五'}, {'age': 36, 'cate': 1, 'gender': 1, 'doctor': '王小燕', 'name': '张全蛋'}]"
    patients = ast.literal_eval(data)
    for patientInfo in patients:
        patientid=insertPatient(patientInfo=patientInfo,device_mac='43:72:DE:A8:5C:20')
        insertTreatments(patientInfo.get('treats',None),patientid)
        insertGrades(patientInfo.get('grades',None),patientid)

