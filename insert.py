from tables import Doctor,Patient,Treatment,Grade,Device,SessionClass, Music
from tools import getTimeStamp
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
        if (treatment_count <= 1000):
            for treatment in treatments:
                music = session.query(Music).filter(Music.music_human_no_and_group == treatment['musicNum']).first()
                session.add(Treatment(treatment_time=treatment['ts'],patient_id=patient_id,music_id=music.music_id))
                #session.add(Treatment(treatment_time=treatment['ts'], patient_id=patient_id))
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
        if (grade_count <= 1000):
            for grade in grades:
                session.add(Grade(grade_level=grade['grade'], grade_score=grade['score'], grade_time=grade['ts'],
                                     patient_id=patient_id))
            session.commit()
        session.close()
    return


#@ brief 插入音乐信息
#@ param  (filename,file_type) (文件名,音乐类型）（string,string）
#@ return  类型+编号（四位string)(表内字段）
def insertAndUpdateMusic(filename, file_type):
    session = SessionClass()
    music = session.query(Music).filter(Music.music_name == filename).first()
    if music == None:
        cur_max_human_no_music = session.query(Music).filter(Music.music_group == file_type).order_by(Music.music_human_no.desc()).first()
        music_human_no = str(int(cur_max_human_no_music.music_human_no) + 1).zfill(3)

        music_new = Music()
        music_new.music_name = filename
        music_new.music_human_no = music_human_no
        music_new.music_group = file_type
        music_new.music_human_no_and_group = music_human_no + file_type
        music_new.music_insert_time = getTimeStamp()
        try:
            session.add(music_new)
            session.flush()
            music_human_no_and_group = music_new.music_human_no_and_group
            session.commit()
            session.close()
            return music_human_no_and_group
        except:
            session.rollback()
            return None
    else:

        music_human_no_and_group = music.music_human_no_and_group
        session.commit()
        session.close()
        return music_human_no_and_group



if __name__=='__main__':
    insertDevice({'device_mac': '123456'})
    #data = "[{'age': 56, 'treats': [{'ts': 1542097122}], 'doctor': '张大伟', 'history': '舌淡红，苔薄白', 'cate': 3, 'inspect': '声阻抗正常，鼓膜正常', 'gender': 1, 'name': '张三', 'report': '右耳耳鸣1年', 'grades': [{'ts': 1542097122, 'score': 12, 'grade': 3}]}, {'age': 42, 'treats': [{'ts': 1542097122}, {'ts': 1542097122}], 'doctor': '王小燕', 'cate': 4, 'gender': 2, 'name': '李四'}, {'age': 42, 'cate': 2, 'gender': 1, 'doctor': '张大伟', 'name': '王五'}, {'age': 36, 'cate': 1, 'gender': 1, 'doctor': '王小燕', 'name': '张全蛋'}]"
    data = "[{'cate': 3, 'grade': [{'grade': 3, 'score': 12, 'ts': 1551948932}], 'history': '舌淡红，苔薄白', 'treat': [{'ts': 1551948932, 'musicNum': '3000'}], 'gender': 1, 'name': '张三', 'inspect': '声阻抗正常，鼓膜正常', 'age': 56, 'report': '右耳耳鸣1年', 'doctor': '张大伟'}, " \
           "{'cate': 4, 'treat': [{'ts': 1551948932, 'musicNum': '4000'}, {'ts': 1551948932, 'musicNum': '4000'}], 'gender': 2, 'name': '李四', 'age': 42, 'doctor': '王小燕'}, " \
           "{'cate': 2, 'doctor': '张大伟', 'name': '王五', 'gender': 1, 'age': 42}, " \
           "{'cate': 1, 'doctor': '王小燕', 'name': '张全蛋', 'gender': 1, 'age': 36}]"
    patients = ast.literal_eval(data)
    for patientInfo in patients:
        patientid=insertPatient(patientInfo=patientInfo,device_mac='123456')
        insertTreatments(patientInfo.get('treat',None),patientid)
        insertGrades(patientInfo.get('grade',None),patientid)


