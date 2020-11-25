from project import db
from project.com.vo.DatasetVO import DatasetVO
from datetime import datetime


class DatasetDAO:
    def insertDataset(self, datasetVO):
        db.session.add(datasetVO)
        db.session.commit()

    def viewDataset(self):
        print("hello from viewDataset")
        datasetList = DatasetVO.query.all()
        print("datasetList=", datasetList)
        return datasetList

    def deleteDataset(self, datasetVO):
        datasetList = DatasetVO.query.get(datasetVO.datasetId)
        db.session.delete(datasetList)
        db.session.commit()

        return datasetList
