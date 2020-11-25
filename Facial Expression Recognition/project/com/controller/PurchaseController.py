from flask import request, render_template, redirect, url_for, session
from datetime import datetime, date
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.PurchaseDAO import PurchaseDAO
from project.com.vo.PackageVO import PackageVO
from project.com.vo.PurchaseVO import PurchaseVO
from project.com.dao.PackageDAO import PackageDAO

@app.route('/user/insertPurchase', methods=['GET'])
def userInsertPurchase():
    try:
        if adminLoginSession() == 'user':
            purchase_LoginId = session['session_loginId']
            purchase_PackageId = request.args.get('packageId')

            purchaseDate = str(date.today())
            purchaseTime = str(datetime.now().strftime("%H:%M:%S"))

            purchaseVO = PurchaseVO()
            purchaseDAO = PurchaseDAO()

            purchaseVO.purchaseDate = purchaseDate
            purchaseVO.purchaseTime = purchaseTime
            purchaseVO.purchase_LoginId = purchase_LoginId
            purchaseVO.purchase_PackageId = purchase_PackageId

            purchaseDAO.insertPurchase(purchaseVO)

            return redirect(url_for('userViewPurchase'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewPurchase', methods=['GET'])
def userViewPurchase():
    try:
        if adminLoginSession() == 'user':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()

            purchase_LoginId = session['session_loginId']

            purchaseVO.purchase_LoginId = purchase_LoginId

            purchaseVOList = purchaseDAO.viewPurchase(purchaseVO)

            return render_template('user/viewPurchase.html', purchaseVOList=purchaseVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deletePurchase', methods=['GET'])
def userDeletePurchase():
    try:
        if adminLoginSession() == 'user':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()

            purchaseId = request.args.get('purchaseId')
            purchaseVO.purchaseId = purchaseId

            purchaseDAO.deletePurchase(purchaseVO)

            return redirect(url_for('userViewPurchase'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/searchPurchase', methods=['GET'])
def adminSearchPurchase():
    try:
        if adminLoginSession() == 'admin':

            purchaseDAO = PurchaseDAO()

            purchaseVOList = purchaseDAO.searchPurchase()
            print("__________________", purchaseVOList)
            return render_template('admin/viewPurchase.html', purchaseVOList=purchaseVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/payment', methods=['GET'])
def userPayment(packageName, packageDuration, packagePrice):
    try:
        if adminLoginSession() == 'user':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()

            packageDAO = PackageDAO()
            packageVO = PackageVO()

            packageVO.packageName = packageName
            packageVO.packageDuration = packageDuration
            packageVO.packagePrice = packagePrice

            purchase_LoginId = session['session_loginId']


            purchaseVO.purchase_LoginId = purchase_LoginId

            purchaseVOList = purchaseDAO.userPayment(purchaseVO)

            return render_template('user/viewPurchase.html', purchaseVOList=purchaseVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

