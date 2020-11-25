from flask import request, render_template, redirect, url_for
from project import app
from datetime import datetime
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.DatasetDAO import DatasetDAO
from project.com.vo.DatasetVO import DatasetVO

from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'project/static/adminResources/dataset/'  # location(path) for uploaded dataset from addDataset.html

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/admin/loadDataset', methods=['GET'])
def adminLoadDataset():
    try:
        if adminLoginSession() == 'admin':
            print('Load Dataset')
            return render_template('admin/addDataset.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertDataset', methods=['POST'])
def adminInsertDataset():
    try:
        if adminLoginSession() == 'admin':
            print("InsertDataset")

            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()

            # to get file from html page
            file = request.files['file']
            print(file)

            # secure_filename is method which gives filename
            datasetFileName = secure_filename(file.filename)
            print("Dataset File name-", datasetFileName)

            now = datetime.now()
            print("now = ", now)

            datasetDate = now.strftime("%y/%m/%d")
            print("date =", datasetDate)

            datasetTime = now.strftime("%H:%M:%S")
            print("time = ", datetime)
            # os.path.join method gives uploaded file path in PC
            datasetFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print("datasetFilepath-", datasetFilePath)

            # save method to save file on given path
            file.save(os.path.join(datasetFilePath, datasetFileName))

            # store fileName & filePath in datasetVO object
            datasetVO.datasetFileName = datasetFileName
            datasetVO.datasetTime = datasetTime
            datasetVO.datasetDate = datasetDate
            datasetVO.datasetFilePath = datasetFilePath.replace("project", "..")
            print("++++++++++++++++++++++++++++")

            datasetDAO.insertDataset(datasetVO)
            print("ddddddddddddddddd")

            return redirect(url_for('adminViewDataset'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewDataset', methods=['GET'])
def adminViewDataset():
    try:
        if adminLoginSession() == 'admin':
            print("ViewDataset")
            datasetDAO = DatasetDAO()
            datasetVOList = datasetDAO.viewDataset()
            print("DatasetVOList-", datasetVOList)
            return render_template('admin/viewDataset.html', datasetVOList=datasetVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteDataset', methods=['GET'])
def adminDeleteDataset():
    try:
        if adminLoginSession() == 'admin':
            print("hello")
            datasetVO = DatasetVO()
            # object created forDatasetDAO &DatasetVO class
            datasetDAO = DatasetDAO()

            datasetId = request.args.get('datasetId')
            print(datasetId)

            datasetVO.datasetId = datasetId  # datasetNo save in DB by datasetVO object ofDatasetVO class

            datasetList = datasetDAO.deleteDataset(datasetVO)  # deletedataset method ofDatasetDAO class

            path = datasetList.datasetFilePath.replace("..", "project") + datasetList.datasetFileName

            os.remove(path)

            return redirect(url_for('adminViewDataset'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
