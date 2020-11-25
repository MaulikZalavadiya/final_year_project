import os
from datetime import datetime

from flask import render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.VideoDAO import VideoDAO
from project.com.vo.VideoVO import VideoVO

##############





###############################USER##############################

@app.route('/user/loadVideo', methods=['GET'])
def userLoadVideo():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addVideo.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/uploadVideo', methods=['POST'])
def userUploadVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()
            videoDAO = VideoDAO()

            UPLOAD_FOLDER = 'project/static/adminResources/videos/'

            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']

            videoFileName = secure_filename(file.filename)
            print("video file name=",videoFileName)
            videoFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print("video file path=", videoFilePath)

            file.save(os.path.join(videoFilePath, videoFileName))



            videoUploadDate = datetime.today().strftime("%d/%m/%Y")
            videoUploadTime = datetime.now().strftime("%H:%M:%S")

            videoFrom_LoginId = session['session_loginId']

            videoVO.videoFileName = videoFileName
            videoVO.videoFilePath = videoFilePath.replace("project", "..")
            videoVO.videoUploadDate = videoUploadDate
            videoVO.videoUploadTime = videoUploadTime
            videoVO.videoFrom_LoginId = videoFrom_LoginId

            #session['videoFilePath'] = videoFilePath

            videoDAO.userInsertVideo(videoVO)

            return redirect(url_for('userViewVideo'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)






@app.route('/user/viewVideo', methods=['GET'])
def userViewVideo():
    try:
        if adminLoginSession() == 'user':

            videoDAO = VideoDAO()
            videoVO = VideoVO()

            videoVO.videoFrom_LoginId = session['session_loginId']

            videoVOList = videoDAO.userViewVideo(videoVO)

            return render_template('user/viewVideo.html', videoVOList=videoVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteVideo', methods=['GET'])
def userDeleteVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()
            videoDAO = VideoDAO()

            videoId = request.args.get('videoId')

            videoVO.videoId = videoId

            videoList = videoDAO.userDeleteVideo(videoVO)

            path = videoList.videoFilePath.replace("..", "project") + videoList.videoFileName
            os.remove(path)

            return redirect(url_for('userViewVideo'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


#######################ADMIN###############################

@app.route('/admin/viewVideo', methods=['GET'])
def adminViewVideo():
    try:
        if adminLoginSession() == 'admin':
            videoDAO = VideoDAO()
            videoVOList = videoDAO.adminViewVideo()

            return render_template('admin/viewVideo.html', videoVOList=videoVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
