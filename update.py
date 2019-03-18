from tables import Doctor,Patient,Treatment,Grade,Device,Music,SessionClass


def updatePerPatient(patient_info, device_mac):
    session = SessionClass()
    device = session.query(Device).filter(Device.device_mac == device_mac).first()
    patient = session.query(Patient).filter(Patient.patient_name==patient_info['patient_name'], Patient.patient_gender==patient_info['patient_gender'],
                                            Patient.patient_age==patient_info['patient_age'], Patient.device_id==device.device_id).first()
    try:
        patient.patient_doctor_category1 = patient_info['patient_doctor_category1']
        patient.patient_doctor_category2 = patient_info['patient_doctor_category2']
        if patient_info['patient_self_reported']=='null':
            patient.patient_self_reported = None
        else:
            patient.patient_self_reported = patient_info['patient_self_reported']
        if patient_info['patient_examination'] == 'null':
            patient.patient_examination = None
        else:
            patient.patient_examination = patient_info['patient_examination']
        if patient_info['patient_medical_history'] == 'null':
            patient.patient_medical_history =None
        else:
            patient.patient_medical_history = patient_info['patient_medical_history']
        session.commit()
        session.close()
        return 1
    except:
        session.close()
        return 0


if __name__=='__main__':
    patient_info={'patient_doctor_category1': 4, 'patient_doctor_category2': 2, 'patient_age': 42, 'patient_examination': 'null', 'patient_self_reported': 'null', 'patient_gender': '2', 'patient_name': '李四', 'patient_medical_history': 'null'}
    device_mac='123456'
    a=updatePerPatient(patient_info,device_mac)
    print(a)

