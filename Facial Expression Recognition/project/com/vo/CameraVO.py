from project import db


class CameraVO(db.Model):
    __tablename__ = 'cameramaster'
    cameraId = db.Column('cameraId', db.Integer, primary_key=True, autoincrement=True)
    cameraType = db.Column('cameraType', db.String(100))
    cameraCode = db.Column('cameraCode', db.String(100))

    def as_dict(self):
        return {
            'cameraId': self.cameraId,
            'cametaType': self.cameraType,
            'cameraCode': self.cameraCode
        }


db.create_all()
