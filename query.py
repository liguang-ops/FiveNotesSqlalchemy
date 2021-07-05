from tables import Doctor,Patient,Treatment,Grade,Device,Music,SessionClass
from tools import timeStampToYMD, patientInfo2List, treatmentInfo2List, gradeInfo2List,writeRowExcel
import time, xlsxwriter

def getPatientIDDeduplicate(device_mac,*args):
    session = SessionClass()
    device=session.query(Device).filter(Device.device_mac==device_mac).first()
    if len(args)==0:
        patient_id_value=session.query(Patient).filter(Patient.device_id==device.device_id).with_entities(Patient.patient_id).all()
    else:
        patient_id_value = session.query(Patient).filter(Patient.device_id == device.device_id, Patient.patient_name==args[0]).with_entities(Patient.patient_id).all()
    value_list=[]
    for index in range(len(patient_id_value)):
        value_list.append(patient_id_value[index][0])
    session.close()
    return value_list


def getDoctorIDDedulicate(device_mac):
    session = SessionClass()
    device = session.query(Device).filter(Device.device_mac == device_mac).first()
    doctor_id_value = session.query(Doctor).filter(Doctor.device_id == device.device_id).with_entities(Doctor.doctor_id).all()
    value_list = []
    for index in range(len(doctor_id_value)):
        value_list.append(doctor_id_value[index][0])
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

#单个病人疗效评估
def getSinglePatirntGradeLevelChange(patient_id):
    session = SessionClass()
    grade_latest = session.query(Grade).order_by(Grade.grade_time.desc()).filter(Grade.patient_id == patient_id).first()
    grade_oldest = session.query(Grade).order_by(Grade.grade_time).filter(Grade.patient_id == patient_id).first()
    if grade_latest !=None:
        difference = grade_oldest.grade_level-grade_latest.grade_level
        session.close()
        if grade_latest.grade_score==0:     # 痊愈
            return 0
        elif difference >= 2:               # 显效
            return 1
        elif difference == 1:               # 有效
            return 2
        else:
            return 3                   # 无效

#获取所有病人信息
def getAllPatientsInfo(device_mac):
    patients_id=getPatientIDDeduplicate(device_mac)
    patients_info=[]
    for id in patients_id:
        patients_info.append(getSinglePatientInfo(id))
    patients_info.sort(key=lambda patient: -patient['grade_time'])
    return patients_info

#获取每天治疗人数
def getTreatmentPatientNumber(device_mac):
    session=SessionClass()
    patients_id=getPatientIDDeduplicate(device_mac)
    timestamps_string=[]
    date_nums=[]
    for patient_id in patients_id:
        treatments=session.query(Treatment).filter(Treatment.patient_id==patient_id).all()
        for treatment in treatments:
            timestamps_string.append(timeStampToYMD(treatment.treatment_time))
    for i in set(timestamps_string):
        counts={}
        counts['date']=i
        counts['nums']=timestamps_string.count(i)
        date_nums.append(counts)
    session.close()
    return date_nums

#获取性别占比
def getGenderPatientProportion(device_mac):
    session = SessionClass()
    patients_id = getPatientIDDeduplicate(device_mac)
    gender_num = [0, 0]
    gender_name = ['男', '女']
    type_percent = []
    for patient_id in patients_id:
        patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
        if patient.patient_gender == 1:    #1为男，2为女
            gender_num[0] += 1
        elif patient.patient_gender == 2:
            gender_num[1] += 1
    all_nums = sum(gender_num)
    for i in range(len(gender_num)):
        counts = {}
        counts['name'] = gender_name[i]
        counts['percent'] = round((gender_num[i] / all_nums), 2)
        counts['a'] = '1'
        type_percent.append(counts)
    session.close()
    return type_percent

#获取每种分型占比
def getTypePatientProportion(device_mac):
    session = SessionClass()
    patients_id = getPatientIDDeduplicate(device_mac)
    types_num = [0,0,0,0,0]
    types_name = ['风热侵袭','肝火上扰','痰火郁结','肾精亏损','脾胃虚弱']
    type_percent = []
    for patient_id in patients_id:
        patient = session.query(Patient).filter(Patient.patient_id==patient_id).first()
        if patient.patient_doctor_category1 == 1:
            types_num[0] += 1
        elif patient.patient_doctor_category1==2:
            types_num[1] += 1
        elif patient.patient_doctor_category1==3:
            types_num[2] += 1
        elif patient.patient_doctor_category1==4:
            types_num[3] += 1
        elif patient.patient_doctor_category1==5:
            types_num[4] += 1
    all_nums=sum(types_num)
    for i in range(len(types_num)):
        counts = {}
        counts['name'] = types_name[i]
        counts['percent'] = round((types_num[i]/all_nums),2)
        counts['a']='1'
        type_percent.append(counts)
    session.close()
    return type_percent


#获取每个年龄段人数 小于等于18、大于18小于等于44、大于44小于等于60、大于60
def getAgePatientProportion(device_mac):
    session = SessionClass()
    patients_id = getPatientIDDeduplicate(device_mac)
    age_stages = [0,0,0,0]
    age_stages_name=['18岁以下','18岁-44岁','44岁-60岁','60岁以上']
    age_nums=[]
    for patient_id in patients_id:
        patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
        if patient.patient_age <= 18:
            age_stages[0] += 1
        elif (patient.patient_age > 18) and (patient.patient_age<=44):
            age_stages[1]+=1
        elif (patient.patient_age > 44) and (patient.patient_age <= 60):
            age_stages[2] += 1
        elif patient.patient_age > 60:
            age_stages[3] += 1
    for i in range(len(age_stages)):
        per_count = {}
        per_count['name'] = age_stages_name[i]
        per_count['percent'] = round((age_stages[i]/sum(age_stages)),2)
        per_count['a']='1'
        age_nums.append(per_count)
    return age_nums


#获取每个医生的患者数目
def getPerDoctorPatientNumber(device_mac):
    session=SessionClass()
    doctors_id=getDoctorIDDedulicate(device_mac)
    perdoctor_nums=[]
    for doctor_id in doctors_id:
        counts={}
        doctor=session.query(Doctor).filter(Doctor.doctor_id==doctor_id).first()
        patient_count=session.query(Patient).filter(Patient.doctor_id==doctor_id).count()
        counts['name']=doctor.doctor_name
        counts['num']=patient_count
        perdoctor_nums.append(counts)
    session.close()
    return perdoctor_nums


#获取每种音乐类型数目
def getPerMusicNumber():
    session=SessionClass()
    permusic_nums=[]
    music_types_name=['宫','商','角', '徵','羽','阿是乐']
    for i in range(6):
        count={}
        count['name']=music_types_name[i]
        count['num']=session.query(Music).filter(Music.music_group==str(i+1)).count()
        permusic_nums.append(count)
    session.close()
    return permusic_nums


#获取整体疗效（痊愈——无耳鸣、显效——降低2个等级及以上，有效——降低1个等级，无效——等级不变化，甚至更糟）
def getResultAll(device_mac):
    nums=[0,0,0,0]
    patients_id = getPatientIDDeduplicate(device_mac)
    result_name=['痊愈','显效','有效','无效']
    result_nums=[]
    for patient_id in patients_id:
        result=getSinglePatirntGradeLevelChange(patient_id)
        if result == 0:
            nums[0]+=1
        elif result == 1:
            nums[1] +=1
        elif result == 2:
            nums[2] += 1
        elif result == 3:
            nums[3] += 1
    for i in range(4):
        count={}
        count['name']=result_name[i]
        count['nums']=nums[i]
        result_nums.append(count)
    return result_nums


#单个病人信息转换成excel
def singlePatientToExcel(patient_id):
    session=SessionClass()

    patient_col_name = ['编号','姓名','性别','年龄','主诉','既往史','检查','设备分型','医生第一分型','医生第二分型','医生姓名']
    treatment_col_name = ['编号','治疗时间','患者编号']
    grade_col_name =['编号','等级','分数','评分时间','患者编号']

    now_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    filename = 'singlePatient_'+ now_time + '.xlsx'
    workbook_filepath = 'emailData/' + filename

    with xlsxwriter.Workbook(workbook_filepath) as workbook:
        worksheet_patient = workbook.add_worksheet('患者信息')
        writeRowExcel(0, patient_col_name, worksheet_patient)
        worksheet_treatment=workbook.add_worksheet('治疗信息')
        writeRowExcel(0, treatment_col_name, worksheet_treatment)
        worksheet_grade=workbook.add_worksheet('评分信息')
        writeRowExcel(0, grade_col_name, worksheet_grade)

        patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
        doctor = session.query(Doctor).filter(Doctor.doctor_id == patient.doctor_id).first()
        treatments = session.query(Treatment).filter(Treatment.patient_id == patient_id).all()
        grades = session.query(Grade).filter(Grade.patient_id == patient_id).all()

        #患者信息sheet表
        patient_info = patientInfo2List(patient, doctor)
        writeRowExcel(1, patient_info, worksheet_patient)

        #治疗信息sheet表
        for i in range(len(treatments)):
            treatment_info=treatmentInfo2List(treatments[i])
            writeRowExcel(i+1,treatment_info,worksheet_treatment)

        # 评分信息sheet表
        for i in range(len(grades)):
            grade_info=gradeInfo2List(grades[i])
            writeRowExcel(i+1,grade_info,worksheet_grade)
        session.close()
    return filename, workbook_filepath

#多个病人信息转换成excel,传入为patient_id list
def allPatientToExcel(device_mac):
    patients_id=getPatientIDDeduplicate(device_mac)
    session = SessionClass()
    patient_col_name = ['编号', '姓名', '性别', '年龄', '主诉', '既往史', '检查', '设备分型', '医生第一分型', '医生第二分型', '医生姓名']
    treatment_col_name = ['编号', '治疗时间','患者编号','音乐编号']
    grade_col_name = ['编号', '等级', '分数', '评分时间','患者编号']

    now_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    filename = 'allPatients_' + now_time + '.xlsx'
    workbook_filepath ='./emailData/' + filename

    with xlsxwriter.Workbook(workbook_filepath) as workbook:
        worksheet_patient = workbook.add_worksheet('患者信息')          # 创建患者信息sheet表
        worksheet_treatment = workbook.add_worksheet('治疗信息')        # 创建治疗信息sheet表
        worksheet_grade = workbook.add_worksheet('评分信息')            # 创建评分信息sheet表
        writeRowExcel(0, patient_col_name, worksheet_patient)
        writeRowExcel(0, treatment_col_name, worksheet_treatment)
        writeRowExcel(0, grade_col_name, worksheet_grade)
        len_treatment = 0
        len_grade = 0
        for index in range(len(patients_id)):
            #从数据库获取单个患者数据
            patient = session.query(Patient).filter(Patient.patient_id == patients_id[index]).first()
            doctor = session.query(Doctor).filter(Doctor.doctor_id == patient.doctor_id).first()
            treatments = session.query(Treatment).filter(Treatment.patient_id == patients_id[index]).all()
            grades = session.query(Grade).filter(Grade.patient_id == patients_id[index]).all()

            #填充患者信息表
            patient_info = patientInfo2List(patient, doctor)
            writeRowExcel(index + 1, patient_info, worksheet_patient)

            # 填充治疗信息表
            for i in range(len(treatments)):
                treatment_info = treatmentInfo2List(treatments[i])
                writeRowExcel(len_treatment + i + 1, treatment_info, worksheet_treatment)
            len_treatment += len(treatments)

            # 填充评分信息表
            for i in range(len(grades)):
                grade_info = gradeInfo2List(grades[i])
                writeRowExcel(len_grade + i + 1, grade_info, worksheet_grade)
            len_grade += len(grades)
        session.close()
    return filename,workbook_filepath


#根据患者姓名和设备mac查询
def getPatientInfoDependName(device_mac,patient_name):
    patients_id = getPatientIDDeduplicate(device_mac,patient_name)
    patients_info = []
    for id in patients_id:
        patients_info.append(getSinglePatientInfo(id))
    patients_info.sort(key=lambda patient: -patient['grade_time'])
    return patients_info

#根据device_mac查询设备是否存在
def getDevice(device_mac):
    session = SessionClass()
    device = session.query(Device).filter(Device.device_mac == device_mac).first()
    session.close()
    if device == None:
        return None
    else:
        return device


#查询所有音乐信息，返回字段音乐名，编号和时间戳
def getAllMusicInfo():
    session = SessionClass()
    musics_info = []
    musics = session.query(Music).all()
    for music in musics:
        per_music_info ={}
        per_music_info['musicName'] = music.music_name
        per_music_info['musicId'] = music.music_human_no_and_group
        per_music_info['musicType'] = music.music_group
        #per_music_info['timestamp'] = music.music_insert_time
        musics_info.append(per_music_info)
    session.close()
    return musics_info


#查询所有音乐music_human_no_and_group
def getCertainMusic():
    session = SessionClass()
    musics = session.query(Music).filter(Music.music_insert_time != 0).all()
    #musics = session.query(Music).all()
    a = []
    for music in musics:
        a.append(music.music_human_no_and_group + '.' +'mp3')
    return a

if __name__=='__main__':
    # patients_info=getAllPatientsInfo('63:8D:56:86:A1:6B')
    # print(patients_info)
    # for a in patients_info['patients_info']:
    #     print(a['grade_time'])
    # timestamps=getTreatmentPatientNumber('5A:D7:5E:52:2F:6E')
    # print(timestamps)
    # a = getAllMusicInfo()
    # print(a)
    a = getCertainMusic()
    print(a)
    print(len(a))


