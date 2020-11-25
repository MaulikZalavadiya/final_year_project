from project import db
from project.com.vo.LoginVO import LoginVO


class DetectionVO(db.Model):
    __tablename__ = 'detectionmaster'
    detectionId = db.Column('detectionId', db.INTEGER, autoincrement=True, primary_key=True)
    detectionFileName = db.Column('detectionFileName', db.VARCHAR(100), nullable=False)
    detectionFilePath = db.Column('detectionFilePath', db.VARCHAR(200), nullable=False)
    detectionUploadDate = db.Column('detectionUploadDate', db.VARCHAR(100), nullable=False)
    detectionUploadTime = db.Column('detectionUploadTime', db.VARCHAR(100), nullable=False)
    detectionFrom_LoginId = db.Column('detectionFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'detectionId': self.detectionId,
            'detectionFileName': self.detectionFileName,
            'detectionFilePath': self.detectionFilePath,
            'detectionUploadDate': self.detectionUploadDate,
            'detectionUploadTime': self.detectionUploadTime,
            'detectionFrom_LoginId': self.detectionFrom_LoginId

        }


db.create_all()
