from project import app
from flask import render_template

from project.com.controller.LoginController import adminLoginSession, adminLogoutSession


# @app.route('/admin/viewDetection')
# def adminViewDetection():
#     try:
#         if adminLoginSession() == 'admin':
#             return render_template('admin/viewDetection.html')
#         else:
#             return adminLogoutSession()
#
#     except Exception as ex:
#         print(ex)


# userside

@app.route('/')
def userloadDashboard():
    return render_template('user/index.html')


# @app.route('/user/loadVideo')
# def userLoadVideo():
#     return render_template('user/addVideo.html')


@app.route('/user/viewContact')
def userViewContant():
    return render_template('user/contactus.html')


@app.route('/user/viewAbout')
def userViewAbout():
    return render_template('user/aboutus.html')


# @app.route('/user/viewVideo')
# def userViewVideo():
#     return render_template('user/viewVideo.html')
