from flask import request, render_template, redirect, url_for, session
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.CameraDAO import CameraDAO
from project.com.vo.CameraVO import CameraVO


@app.route('/admin/loadCamera', methods=['GET'])
def adminLoadCamera():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addCamera.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/insertCamera', methods=['POST'])
def adminInsertCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraType = request.form['cameraType']
            print(cameraType)
            cameraCode = request.form['cameraCode']
            print(cameraCode)

            cameraVO = CameraVO()
            cameraDAO = CameraDAO()

            cameraVO.cameraType = cameraType
            cameraVO.cameraCode = cameraCode

            cameraDAO.insertCamera(cameraVO)

            return redirect(url_for('adminViewCamera'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewCamera', methods=['GET'])
def adminViewCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraDAO = CameraDAO()
            cameraVOList = cameraDAO.viewCamera()
            print("__________________", cameraVOList)
            return render_template("admin/viewCamera.html", cameraVOList=cameraVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/deleteCamera', methods=['GET'])
def adminDeleteCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraVO = CameraVO()

            cameraDAO = CameraDAO()

            cameraId = request.args.get('cameraId')

            cameraVO.cameraId = cameraId

            cameraDAO.deleteCamera(cameraVO)

            return redirect(url_for('adminViewCamera'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/editCamera', methods=['GET'])
def adminEditCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraVO = CameraVO()

            cameraDAO = CameraDAO()

            cameraId = request.args.get('cameraId')

            cameraVO.cameraId = cameraId

            cameraVOList = cameraDAO.editCamera(cameraVO)

            print("=======cameraVOList=======", cameraVOList)

            print("=======type of cameraVOList=======", type(cameraVOList))

            return render_template('admin/editCamera.html', cameraVOList=cameraVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/updateCamera', methods=['POST'])
def adminUpdateCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraId = request.form['cameraId']
            cameraCode = request.form['cameraCode']
            cameraType = request.form['cameraType']

            print("=========================done==========================")

            cameraVO = CameraVO()
            cameraDAO = CameraDAO()

            cameraVO.cameraId = cameraId
            cameraVO.cameraType = cameraType
            cameraVO.cameraCode = cameraCode

            cameraDAO.updateCamera(cameraVO)

            return redirect(url_for('adminViewCamera'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
