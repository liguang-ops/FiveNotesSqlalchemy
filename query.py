from tables import Doctor,Patient,Treatment,Grade,Device,SessionClass
from tools import timeStampToYMD

def getPatientIDDeduplicate(device_mac):
    session = SessionClass()
    device=session.query(Device).filter(Device.device_mac==device_mac).first()
    patient_id_value=session.query(Patient).filter(Patient.device_id==device.device_id).with_entities(Patient.patient_id).all()
    value_list=[]
    for index in range(len(patient_id_value)):
        value_list.append(patient_id_value[index][0])
    session.close()
    return value_list


def getSinglePatientInfo(patient_id):
    session=SessionClass()
    patient=session.query(Patient).filter(Patient.patient_id==patient_id).first()
    treatment_count=session.query(Treatment).filter(Treatment.patient_id==patient_id).count()
    grade=session.query(Grade).order_by(Grade.grade_time.desc()).filter(Grade.patient_id==patient_id).first()
    # 处理None情况
    if (grade == None):
        grade_level = ''
        grade_score=''
        grade_time=0
    else:
        grade_level = grade.grade_level
        grade_score=grade.grade_score
        grade_time=grade.grade_time
    #处理None情况结束
    per_patient={
        'patient_id':patient.patient_id,
        'patient_name':patient.patient_name,
        'patient_gender':patient.patient_gender,
        'patient_age':patient.patient_age,
        'patient_self_reproted': patient.patient_self_reported,
        'patient_medical_history':patient.patient_medical_history,
        'patient_examination':patient.patient_examination,
        'patient_doctor_category1':patient.patient_doctor_category1,
        'patient_doctor_category2':patient.patient_doctor_category2,
        'doctor':patient.doctor.doctor_name,
        'treatment_count':treatment_count,
        'grade_level':grade_level,
        'grade_score':grade_score,
        'grade_time':grade_time,
        'device_id':patient.device_id
    }
    session.close()
    return per_patient

#获取所有病人信息
def getAllPatientsInfo(device_mac):
    patients_id=getPatientIDDeduplicate(device_mac)
    patients_info=[]
    for id in patients_id:
        patients_info.append(getSinglePatientInfo(id))
    patients_info.sort(key=lambda patient: -patient['grade_time'])
    return {'patients_info':patients_info}

#获取每天治疗人数
def getTreatmentPatientNumber(device_mac):
    session=SessionClass()
    patients_id=getPatientIDDeduplicate(device_mac)
    timestamps_string=[]
    date_result=[]
    for patient_id in patients_id:
        treatments=session.query(Treatment).filter(Treatment.patient_id==patient_id).all()
        for treatment in treatments:
            timestamps_string.append(timeStampToYMD(treatment.treatment_time))
    for i in set(timestamps_string):
        counts={}
        counts['date']=i
        counts['steps']=timestamps_string.count(i)
        date_result.append(counts)
    session.close()
    return date_result


    # for key in timestamps.sort():
    #     date_result[key]=date_result.get(key,0)+1
    # return date_result





if __name__=='__main__':
    # patients_info=getAllPatientsInfo('63:8D:56:86:A1:6B')
    # print(patients_info)
    # for a in patients_info['patients_info']:
    #     print(a['grade_time'])
    # timestamps=getTreatmentPatientNumber('5A:D7:5E:52:2F:6E')
    # print(timestamps)
    result=getTreatmentPatientNumber('5A:D7:5E:52:2F:6E')
    print(result)