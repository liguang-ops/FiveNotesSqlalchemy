import time
import zipfile
import os
import xlsxwriter
from tables import Doctor,Patient,Treatment,Grade,Music,SessionClass


#@ brief 将时间戳转换成年月日字符串
#@ param deviceInfo 设备信息（字典）
#@ return device_id 设备id
def timeStampToYMD(timeStamp):
    timeArray=time.localtime(timeStamp)
    stringYMD=time.strftime('%Y-%m-%d',timeArray)
    return stringYMD

#@ brief 获取当前时间时间戳
#@ param 无
#@ return 时间戳（int）
def getTimeStamp():
    timestamp = time.time()
    return int(timestamp)



#@ brief 将数字映射成性别
#@ param gender 数字（代表性别）
#@ return
def mapGender(gender):
    if gender==1:
        gender_map='男'
    elif gender==2:
        gender_map='女'
    return gender_map

#@ brief 将数字映射成分型
#@ param gender 数字（代表分型）
#@ return
def mapType(type):
    if type==1:
        type_map='风热侵袭'
    elif type==2:
        type_map='肝火上扰'
    elif type==3:
        type_map='痰火郁结'
    elif type==4:
        type_map='肾精亏损'
    elif type==5:
        type_map='脾胃虚弱'
    return type_map


#@ brief 将一行患者表内容转化成list
#@ param 一行患者表对象
#@ return 列名(list) 数据(list)
def patientInfo2List(patient,doctor):
    patient_info = []
    patient_info.append(patient.patient_id)
    patient_info.append(patient.patient_name)
    patient_info.append(mapGender(patient.patient_gender))
    patient_info.append(patient.patient_age)
    if patient.patient_self_reported ==None:
        patient_info.append('None')
    else:
        patient_info.append(patient.patient_self_reported)
    if patient.patient_medical_history==None:
        patient_info.append('None')
    else:
        patient_info.append(patient.patient_medical_history)
    if patient.patient_examination == None:
        patient_info.append('None')
    else:
        patient_info.append(patient.patient_examination)
    patient_info.append(mapType(patient.patient_device_category))
    patient_info.append(mapType(patient.patient_doctor_category1))
    if patient.patient_doctor_category2 == None:
        patient_info.append('None')
    else:
        patient_info.append(mapType(patient.patient_doctor_category2))
    patient_info.append(doctor.doctor_name)
    return  patient_info


#@ brief 将一行治疗表内容转化成list
#@ param 一行治疗表对象
#@ return 列名(list) 数据(list)
def treatmentInfo2List(treatment):
    session = SessionClass()
    music = session.query(Music).filter(Music.music_id == treatment.music_id).first()
    treatment_info=[]
    treatment_info.append(treatment.treatment_id)
    treatment_info.append(timeStampToYMD(treatment.treatment_time))
    treatment_info.append(treatment.patient_id)
    treatment_info.append(music.music_human_no_and_group)
    return treatment_info



#@ brief 将一行评分表内容转化成list
#@ param 一行评分表对象
#@ return 列名(list) 数据(list)
def gradeInfo2List(grade):
    grade_info=[]
    grade_info.append(grade.grade_id)
    grade_info.append(grade.grade_level)
    grade_info.append(grade.grade_score)
    grade_info.append(timeStampToYMD(grade.grade_time))
    grade_info.append(grade.patient_id)
    return grade_info


#@ brief 向worksheet中写入一行数据
#@ param row 行序列；data 行数据；worksheet 指定sheet表
#@ return device_id 设备id
def writeRowExcel(row,data,worksheet):
    for col in range(len(data)):
        worksheet.write(row,col,data[col])


def getZipfile(source_file_names, source_filepath='E:\\NewMyGitProjects\\FiveNotesSqlalchemy\\mp3Files', target_filepath='E:\\NewMyGitProjects\\FiveNotesSqlalchemy\\mp3ZipFiles',):
    now_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    file_name = now_time + '.zip'
    new_target_filepath = os.path.join(target_filepath, file_name)
    new_zip = zipfile.ZipFile(new_target_filepath, 'w')
    for name in source_file_names:
        path = source_filepath
        path_res = os.path.join(path, name)
        new_zip.write(path_res, compress_type=zipfile.ZIP_DEFLATED)
    new_zip.close()
    return target_filepath,file_name




if __name__=='__main__':
    #print(mapGender(1))
    # now_time=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    # workbook_filename='E:/NewMyGitProjects/FiveNotesSqlalchemy/emailData/' +now_time+'.xlsx'
    # with xlsxwriter.Workbook(workbook_filename) as workbook:
    #     worksheet_patient=workbook.add_worksheet('患者信息')
    #     data=['患者编号','患者姓名','患者性别']
    #     writeRowExcel(0,data,worksheet_patient)
    file_names = ['0021.mp3', '0031.mp3', '0041.mp3']
    getZipfile(file_names)



