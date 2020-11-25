import os
from datetime import datetime

from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO


@app.route('/user/loadComplain', methods=['GET'])
def userLoadComplain():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainFrom_LoginId = session['session_loginId']

            complainList = complainDAO.viewComplain(complainVO)

            print("__________________", complainList)

            return render_template('user/addComplain.html', complainList=complainList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST'])
def userInsertComplain():
    try:
        if adminLoginSession() == 'user':
            UPLOAD_FOLDER = 'project/static/adminResources/complain/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']

            now = datetime.now()
            complainDate = now.strftime("%y/%m/%d")
            complainTime = now.strftime("%H:%M:%S")

            complainFile = request.files['file']
            complainFileName = secure_filename(complainFile.filename)
            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            complainFile.save(os.path.join(complainFilePath, complainFileName))

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainStatus = "pending"
            complainVO.complainFileName = complainFileName
            complainVO.complainFilePath = complainFilePath.replace("project", "..")
            complainVO.complainFrom_LoginId = session['session_loginId']

            complainDAO.insertComplain(complainVO)

            return redirect(url_for('userLoadComplain'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')

            complainVO.complainId = complainId

            complainList = complainDAO.deleteComplain(complainVO)

            path_lender = complainList.complainFilePath.replace("..", "project") + complainList.complainFileName
            os.remove(path_lender)

            if complainList.complainStatus == 'replied':
                path_admin = complainList.replyFilePath.replace("..", "project") + complainList.replyFileName
                os.remove(path_admin)

            return redirect(url_for('userLoadComplain'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route("/user/loadComplainReply")
def userViewComplainReply():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.args.get("complainId")

            complainVO.complainId = complainId

            complainReplyList = complainDAO.viewComplainReply(complainVO)

            return render_template("user/viewComplainReply.html", complainReplyList=complainReplyList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


# --------------------------------- admin side ---------------------------------------------------------------

@app.route('/admin/viewComplain', methods=['GET'])
def adminViewComplain():
    try:
        if adminLoginSession() == 'admin':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainStatus = "pending"
            print("hello complain admin")

            complainVOList = complainDAO.adminViewComplain(complainVO)
            totalComplainReply = len(complainVOList)

            print("__________________", complainVOList)

            return render_template('admin/viewComplain.html', complainVOList=complainVOList, totalComplainReply=totalComplainReply)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply', methods=['GET'])
def adminLoadComplainReply():
    try:
        if adminLoginSession() == 'admin':
            complainId = request.args.get("complainId")
            return render_template('admin/addComplainReply.html', complainId=complainId)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST'])
def adminInsertComplainReplay():
    try:
        if adminLoginSession() == 'admin':
            UPLOAD_FOLDER = 'project/static/adminResources/reply/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']

            now = datetime.now()

            replyDate = now.strftime("%y/%m/%d")
            replyTime = now.strftime("%H:%M:%S")

            replyFile = request.files['replyFile']
            replyFileName = secure_filename(replyFile.filename)
            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER'])

            # if replyFileName

            replyFile.save(os.path.join(replyFilePath, replyFileName))

            complainVO.complainId = complainId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace("project", "..")
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainTo_LoginId = session['session_loginId']
            complainVO.complainStatus = 'replied'

            complainDAO.adminInsertReply(complainVO)

            return redirect(url_for('adminViewComplain'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
