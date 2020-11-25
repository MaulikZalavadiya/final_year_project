from flask import request, render_template, redirect, url_for,session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.ProfileDAO import ProfileDAO
# from project.com.dao.AreaDAO import AreaDAO
# from project.com.vo.AreaVO import AreaVO
from project.com.vo.RegisterVO import RegisterVO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.LoginVO import LoginVO

@app.route('/user/loadProfile')
def userLoadProfile():
    try:
        if adminLoginSession() == "user":
            profileDAO = ProfileDAO()
            registerVO = RegisterVO()

            register_LoginId = session['session_loginId']
            registerVO.register_LoginId = register_LoginId

            profileVOList = profileDAO.viewProfile(registerVO)
            print(profileVOList)
            return render_template('user/profile.html',profileVOList=profileVOList)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)



@app.route('/user/editProfile')
def userEditProfile():
    try:
        if adminLoginSession() == "user":
            profileDAO = ProfileDAO()
            registerVO = RegisterVO()

            register_LoginId = session['session_loginId']
            registerVO.register_LoginId = register_LoginId

            profileVOList = profileDAO.viewProfile(registerVO)
            print(profileVOList)

            return render_template('user/editProfile.html',profileVOList=profileVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/updateProfile', methods=['POST'])
def userUpdateProfile():
    try:
        if adminLoginSession() == 'user':
            registerVO = RegisterVO()
            profileDAO = ProfileDAO()

            loginVO = LoginVO()
            loginVO.loginId = session['session_loginId']
            loginVO.loginUsername = request.form['loginUsername']


            registerVO.registerId=request.form['registerId']
            registerVO.registerFirstName = request.form['registerFirstName']
            registerVO.registerLastName = request.form['registerLastName']
            registerVO.registerContact = request.form['registerContact']
            registerVO.registerAddress = request.form['registerAddress']

            profileDAO.userUpdateLoginProfile(loginVO)
            profileDAO.userUpdateRegisterProfile(registerVO)
            return redirect(url_for('userLoadProfile'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/changePassword')
def userChangePassword():
    try:
        if adminLoginSession() == 'user':
            return render_template("user/resetPassword.html")
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertPassword',methods=['POST'])
def userInsertPassword():
    try:
        if adminLoginSession() == 'user':
            profileDAO = ProfileDAO()
            loginVO = LoginVO()

            loginId = request.form['loginId']
            oldLoginPassword = request.form['oldLoginPassword']
            loginPassword = request.form['loginPassword']

            loginVO.loginId = loginId

            profileVOList = profileDAO.viewLoginDetails(loginVO)

            if oldLoginPassword == profileVOList.loginPassword:
                loginVO.loginPassword = loginPassword
                profileDAO.userInsertPassword(loginVO)
                return adminLogoutSession()
            else:
                msg = "your old password are not match !"
                return render_template('user/resetPassword.html', msg=msg)
        else:
            adminLogoutSession()

    except Exception as ex:
        print(ex)






@app.route('/user/loadAboutUs')
def userLoadAboutUs():
    try:
        if adminLoginSession() == "user":
            profileDAO = ProfileDAO()
            registerVO = RegisterVO()

            register_LoginId = session['session_loginId']
            registerVO.register_LoginId = register_LoginId

            profileVOList = profileDAO.viewProfile(registerVO)
            print(profileVOList)
            return render_template('user/aboutus.html',profileVOList=profileVOList)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)



@app.route('/user/loadContactUs')
def userLoadContactUs():
    try:
        if adminLoginSession() == "user":
            profileDAO = ProfileDAO()
            registerVO = RegisterVO()

            register_LoginId = session['session_loginId']
            registerVO.register_LoginId = register_LoginId

            profileVOList = profileDAO.viewProfile(registerVO)
            print(profileVOList)
            return render_template('user/contactus.html',profileVOList=profileVOList)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
