from project import db
from project.com.vo.LoginVO import LoginVO


class VideoVO(db.Model):
    __tablename__ = 'videomaster'
    videoId = db.Column('videoId', db.Integer, primary_key=True, autoincrement=True)
    videoFileName = db.Column('videoFileName', db.VARCHAR(100))
    videoFilePath = db.Column('videoFilePath', db.VARCHAR(100))
    videoUploadDate = db.Column('videoUploadDate', db.VARCHAR(100))
    videoUploadTime = db.Column('videoUploadTime', db.VARCHAR(100))
    videoFrom_LoginId = db.Column('videoFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'videoId': self.videoId,
            'videoFileName': self.videoFileName,
            'videoFilePath': self.videoFilePath,
            'videoUploadDate': self.videoUploadDate,
            'videoUploadTime': self.videoUploadTime,
            'videoFrom_LoginId': self.videoFrom_LoginId
        }


db.create_all()
