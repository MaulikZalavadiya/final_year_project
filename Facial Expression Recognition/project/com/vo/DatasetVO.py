from project import db
from datetime import datetime


class DatasetVO(db.Model):
    __tablename__ = 'datasetmaster'
    datasetId = db.Column('datasetId', db.INTEGER, primary_key=True, autoincrement=True)
    datasetFileName = db.Column('datasetFileName', db.String(30), nullable=False)
    datasetFilePath = db.Column('datasetFilePath', db.String(60), nullable=False)
    datasetDate = db.Column('datasetDate', db.Date())
    datasetTime = db.Column('datasetTime', db.Time())

    def as_dict(self):
        return {
            'datasetId': self.datasetId,
            'datasetFileName': self.datasetFileName,
            'datasetFilePath': self.datasetFilePath,
            'datasetDate': self.datasetDate,
            'datasetTime': self.datasetTime
        }


db.create_all()
