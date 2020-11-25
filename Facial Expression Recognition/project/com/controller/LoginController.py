import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template, redirect, url_for, session
from project import app
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.dao.DetectionDAO import DetectionDAO
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.ComplainVO import ComplainVO
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/', methods=['GET'])
def adminLoadLogin():
    try:
        print("in login")
        session.clear()
        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route("/admin/validateLogin", methods=['POST'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]  # to convert loginVOList into dictionary inside the list

        print(loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = 'Username Or Password is Incorrect !'

            return render_template('admin/login.html', error=msg)

        elif loginDictList[0]['loginStatus'] == "inactive":

            error_block = 'User is temporary blocked by Website Admin !'

            return render_template('admin/login.html', error_block=error_block)

        else:

            for row1 in loginDictList:

                loginId = row1['loginId']
                loginUsername = row1['loginUsername']
                loginRole = row1['loginRole']

                session['session_loginId'] = loginId
                print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ session store')
                session['session_loginUsername'] = loginUsername
                session['session_loginRole'] = loginRole

                session.permanent = False  # True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))

                elif loginRole == 'user':
                    return redirect(url_for('userLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard', methods=['GET'])
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            registerVOList = registerDAO.adminViewUser()
            totalUsers = len(registerVOList)

            feedbackDAO = FeedbackDAO()
            feedbackList = feedbackDAO.adminViewFeedback()
            totalFeedbackCount = len(feedbackList)

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            complainVO.complainStatus = "pending"
            pendingComlpainList = complainDAO.adminViewComplain(complainVO)
            pendingComplainCount = len(pendingComlpainList)

            detectionDAO = DetectionDAO()
            userVOList = detectionDAO.getUsers()
            return render_template('admin/index.html', totalUsers=totalUsers,
                                   totalFeedbackCount=totalFeedbackCount, userVOList=userVOList,
                                   pendingComplainCount=pendingComplainCount)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


        # ------user side---


@app.route('/user/loadDashboard', methods=['GET'])
def userLoadDashboard():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/index.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:

            if session['session_loginRole'] == 'admin':
                return 'admin'

            elif session['session_loginRole'] == 'user':
                return 'user'

            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")

        else:

            print("<<<<<<<<<<<<<<<<False>>>>>>>>>>>>>>>>>>>>")

            return False
    except Exception as ex:
        print(ex)


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    try:
        session.clear()
        return redirect(url_for('adminLoadLogin'))

    except Exception as ex:
        print(ex)


@app.route('/admin/blockUser', methods=['GET'])
def adminBlockUser():
    try:
        if adminLoginSession() == 'admin':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginId = request.args.get('loginId')

            loginVO.loginId = loginId
            loginVO.loginStatus = "inactive"
            loginDAO.updateLogin(loginVO)

            return redirect(url_for('adminViewUser'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/unblockUser', methods=['GET'])
def adminUnblockUser():
    try:
        if adminLoginSession() == 'admin':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginId = request.args.get('loginId')

            loginVO.loginId = loginId
            loginVO.loginStatus = "active"
            loginDAO.updateLogin(loginVO)

            return redirect(url_for('adminViewUser'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


##############  Forgot Password ###############

@app.route("/admin/forgotPassword", methods=['GET'])
def adminForgotPassword():
    try:
        # if adminLoginSession() == 'user':
        return render_template('user/forgotPassword.html')
        # else:
        #     return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route("/admin/insertUsername", methods=['POST'])
def adminInsertUsername():
    try:
        loginDAO = LoginDAO()
        loginVO = LoginVO()

        loginUsername = request.form['loginUsername']
        loginVO.loginUsername = loginUsername

        loginVOList = loginDAO.validateLoginUsername(loginVO)
        print("loginVO=", loginVO, "\nloginVOList=", loginVOList)
        loginDictList = [i.as_dict() for i in loginVOList]
        print("loginDictList=", loginDictList)
        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:
            msg = "User is not exist !"
            return render_template("user/forgotPassword.html", error=msg)
        else:
            for row in loginDictList:
                loginId = row['loginId']
                loginUsername = row['loginUsername']
                loginPassword = row['loginPassword']
                print("id Username", loginId, "\t", loginUsername, "\t", loginPassword)

                session['session_loginId'] = loginId
                session['session_loginUsername'] = loginUsername

            otp = ''.join((random.choice(string.digits)) for x in range(6))

            sender = "mdhfec2020@gmail.com"
            receiver = loginUsername
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "Reset Password"

            msg.attach(MIMEText(otp, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "facial@2020")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)
            server.quit()

            session["otp"] = otp

            return render_template("admin/addOTP.html")

    except Exception as ex:
        print(ex)


@app.route("/admin/insertOtp", methods=['POST'])
def adminInsertOtp():
    try:
        loginOtp = request.form['loginOtp']
        if session['otp'] == loginOtp:
            return render_template("admin/addNewPassword.html")
        else:
            msg = "Otp is not Match!"
            return render_template("admin/addOTP.html", error=msg)
    except Exception as ex:
        print(ex)


@app.route("/admin/insertNewPassword", methods=['POST'])
def adminInsertNewPassword():
    try:
        loginDAO = LoginDAO()
        loginVO = LoginVO()
        loginPassword = request.form["loginPassword"]

        sender = "mdhfec2020@gmail.com"

        receiver = session["session_loginUsername"]

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "New Password"

        msg.attach(MIMEText(loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "facial@2020")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        server.quit()

        loginVO.loginId = session['session_loginId']
        loginVO.loginPassword = loginPassword
        loginDAO.loginUpdateUser(loginVO)

        return render_template("admin/login.html")

    except Exception as ex:
        print(ex)


@app.route('/user/loadResetPassword')
def userLoadResetPassword():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/resetPassword.html')
        else:
            return redirect(url_for("adminLogoutSession"))

    except Exception as ex:
        print(ex)


@app.route('/user/resetPassword', methods=['POST'])
def userResetPassword():
    try:
        if adminLoginSession() == 'user':
            oldLoginPassword = request.form['oldLoginPassword']
            newLoginPassword = request.form['newLoginPassword']
            confirmNewLoginPassword = request.form['confirmNewLoginPassword']

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginId = session['session_loginId']
            print(loginVO.loginId)
            loginVO.loginUsername = session['session_loginUsername']
            print(loginVO.loginUsername)
            loginVO.loginPassword = oldLoginPassword
            print(loginVO.loginPassword)

            loginDictList = [i.as_dict() for i in loginDAO.validatePassword(loginVO)]
            print(loginDictList)

            if len(loginDictList) != 0:
                print([i.as_dict() for i in loginDAO.validatePassword(loginVO)])
                if newLoginPassword == confirmNewLoginPassword:
                    loginVO.loginPassword = newLoginPassword
                    loginDAO.updateLogin(loginVO)
                    return redirect(url_for('userLoadDashboard'))
                else:
                    return render_template('user/resetPassword.html',
                                           error="Invalid confirmation of new password,Please try again!")
            else:
                return render_template('user/resetPassword.html',
                                       error="Invalid old password,please enter valid Password!")

        else:
            return redirect(url_for("adminLogoutSession"))

    except Exception as ex:
        print(ex)
