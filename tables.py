from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Text,LargeBinary,ForeignKey,UniqueConstraint,Index,create_engine
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.pool import NullPool

#创建数据库连接
engine = create_engine('mysql+pymysql://root:308YiXin++@sh-cynosdbmysql-grp-5iw5n41g.sql.tencentcdb.com:27048/fivenotes',poolclass=NullPool) #echo=True,
SessionClass=sessionmaker(bind=engine)

Base=declarative_base()


# 定义doctor表
class Doctor(Base):
    __tablename__ = 'doctor'
    doctor_id = Column(Integer, primary_key=True)
    doctor_name = Column(String(10), nullable=False)
    device_id = Column(Integer, ForeignKey('device.device_id'), nullable=False)
    patient = relationship('Patient', backref='doctor')
    __table_args__ = (
        UniqueConstraint('doctor_name', 'device_id', name='ui_name_id'),
    )


# 定义patient表
class Patient(Base):
    __tablename__ = 'patient'
    patient_id = Column(Integer, primary_key=True)
    patient_name = Column(String(10), nullable=False)
    patient_gender = Column(Integer, nullable=False)
    patient_age = Column(Integer, nullable=False)
    device_id = Column(Integer, ForeignKey('device.device_id'), nullable=False)
    patient_self_reported = Column(Text, nullable=True)
    patient_medical_history = Column(Text, nullable=True)
    patient_examination = Column(Text, nullable=True)
    patient_device_category = Column(Integer, nullable=False)
    patient_doctor_category1 = Column(Integer, nullable=False)
    patient_doctor_category2 = Column(Integer, nullable=True)
    doctor_id = Column(Integer, ForeignKey('doctor.doctor_id'), nullable=False)

    treatment = relationship('Treatment', backref='patient')
    grade = relationship('Grade', backref='patient')
    __table_args__ = (
        UniqueConstraint('patient_name', 'patient_gender', 'patient_age', 'device_id', name='ui_name_gender_age_device'),
        Index('index_name_gender_age_device', 'patient_name', 'patient_gender', 'patient_age', 'device_id')
    )



# 定义treatment表
class Treatment(Base):
    __tablename__ = 'treatment'
    treatment_id = Column(Integer, primary_key=True)
    treatment_time = Column(Integer, nullable=False)
    patient_id = Column(Integer, ForeignKey('patient.patient_id'), nullable=False)
    music_id=Column(Integer,ForeignKey('music.music_id'),nullable=False)


# 定义grade表
class Grade(Base):
    __tablename__ = 'grade'
    grade_id = Column(Integer, primary_key=True)
    grade_level = Column(Integer, nullable=True)
    grade_score = Column(Integer, nullable=True)
    grade_time = Column(Integer, nullable=True)
    patient_id = Column(Integer, ForeignKey('patient.patient_id'), nullable=False)


# 定义device表
class Device(Base):
    __tablename__ = 'device'
    device_id = Column(Integer, primary_key=True)
    device_mac = Column(String(17), nullable=False, unique=True, index=True)
    device_img = Column(LargeBinary, nullable=True)
    device_name = Column(String(20), nullable=True)
    device_department = Column(String(20), nullable=True)
    patient = relationship('Patient', backref='device')
    doctor = relationship('Doctor', backref='device')

#定义music表
class Music(Base):
    __tablename__ = 'music'
    music_id = Column(Integer, primary_key=True)
    music_human_no=Column(String(3),nullable=False)
    #music_human_no = Column(Integer, nullable=False, unique=True, index=True)
    music_name=Column(String(50),nullable=False)
    music_singer = Column(String(20), nullable=True)
    music_characteristic = Column(String(20), nullable=True)
    music_score = Column(Integer, nullable=True)
    music_group=Column(String(1),nullable=False)
    music_human_no_and_group=Column(String(4),nullable=False)
    music_insert_time = Column(Integer, nullable=True)
    treatment = relationship('Treatment', backref='music')

if __name__=='__main__':
#    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session=SessionClass()
    session.add(Music(music_human_no='000', music_name='森林', music_group='1', music_insert_time=1552527627, music_human_no_and_group='1000'))
    session.add(Music(music_human_no='000', music_name='峡谷', music_group='2', music_insert_time=1552527627, music_human_no_and_group='2000'))
    session.add(Music(music_human_no='000', music_name='田野', music_group='3', music_insert_time=1552527627, music_human_no_and_group='3000'))
    session.add(Music(music_human_no='000', music_name='荒岛', music_group='4', music_insert_time=1552527627, music_human_no_and_group='4000'))
    session.add(Music(music_human_no='000', music_name='星空', music_group='5', music_insert_time=1552527627, music_human_no_and_group='5000'))
    session.add(Music(music_human_no='001', music_name='春江花月夜', music_group='1', music_insert_time=1552527627, music_human_no_and_group='1001'))
    session.add(Music(music_human_no='001', music_name='阳春白雪', music_group='2', music_insert_time=1552527627, music_human_no_and_group='2001'))
    session.add(Music(music_human_no='001', music_name='胡笳十八拍', music_group='3', music_insert_time=1552527627, music_human_no_and_group='3001'))
    session.add(Music(music_human_no='001', music_name='紫竹调', music_group='4', music_insert_time=1552527627, music_human_no_and_group='4001'))
    session.add(Music(music_human_no='001', music_name='梅花三弄', music_group='5', music_insert_time=1552527627, music_human_no_and_group='5001'))
    session.add(Music(music_human_no='000', music_name='青花瓷', music_group='6', music_insert_time=1552527627,music_human_no_and_group='6000'))
    session.commit()
    session.close()

