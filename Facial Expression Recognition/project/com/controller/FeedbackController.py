from datetime import datetime
from flask import request, render_template, redirect, url_for, session
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO


@app.route('/user/loadFeedback', methods=['GET'])
def userLoadFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackFrom_LoginId = session['session_loginId']


            FeedbackVOList = feedbackDAO.viewFeedback(feedbackVO)

            return render_template('user/addFeedback.html', FeedbackVOList=FeedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['POST'])
def userInsertFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']

            now = datetime.now()

            feedbackDate = now.strftime("%y/%m/%d")
            feedbackTime = now.strftime("%H:%M:%S")

            feedbackVO.feedbackFrom_LoginId = session['session_loginId']
            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime

            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('userLoadFeedback'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/deleteFeedback', methods=['GET'])
def userDeleteFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackId = request.args.get('feedbackId')

            feedbackVO.feedbackId = feedbackId
            feedbackDAO.deleteFeedback(feedbackVO)

            return redirect(url_for('userLoadFeedback'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


# -----------------------------Admin side-------------------------
@app.route('/admin/viewFeedback', methods=['GET'])
def adminViewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()

            feedbackList = feedbackDAO.adminViewFeedback()

            print("_______feedbackList___________", feedbackList)

            return render_template('admin/viewFeedback.html', feedbackList=feedbackList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/reviewFeedback')
def adminReviewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackId = request.args.get('feedbackId')
            feedbackTo_LoginId = session['session_loginId']

            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId

            feedbackDAO.adminReviewFeedback(feedbackVO)

            return redirect(url_for('adminViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
