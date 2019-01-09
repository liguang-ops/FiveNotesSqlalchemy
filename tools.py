import time



#@ brief 将时间戳转换成年月日字符串
#@ param deviceInfo 设备信息（字典）
#@ return device_id 设备id
def timeStampToYMD(timeStamp):
    timeArray=time.localtime(timeStamp)
    stringYMD=time.strftime('%Y-%m-%d',timeArray)
    return stringYMD

def singlePatientToExcel(patient_id):
    return 



if __name__=='__main__':
    print(timeStampToYMD(1514856271))