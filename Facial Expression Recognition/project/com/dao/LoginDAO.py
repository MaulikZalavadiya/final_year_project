from project import db
from project.com.vo.LoginVO import LoginVO


class LoginDAO:
    def insertLogin(self, userVO):
        db.session.add(userVO)
        db.session.commit()

    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername,
                                            loginPassword=loginVO.loginPassword,
                                            loginStatus=LoginVO.loginStatus)

        return loginList

    def updateLogin(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def validateLoginUsername(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername).all()

        return loginList

    def loginUpdateUser(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def validatePassword(self, loginVO):
        loginList = LoginVO.query.filter_by(loginId=loginVO.loginId,
                                            loginUsername=loginVO.loginUsername,
                                            loginPassword=loginVO.loginPassword).all()

        return loginList
