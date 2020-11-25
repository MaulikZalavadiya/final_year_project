from project import db
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.LoginVO import LoginVO
# from project.com.vo.AreaVO import AreaVO

class ProfileDAO():

    def viewProfile(self,registerVO):
        profileList = db.session.query(RegisterVO,LoginVO).join(LoginVO,RegisterVO.register_LoginId == LoginVO.loginId).filter_by(loginId=registerVO.register_LoginId).all()

        return profileList


    def userUpdateLoginProfile(self,loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def userUpdateRegisterProfile(self,registerVO):
        db.session.merge(registerVO)
        db.session.commit()

    def viewLoginDetails(self,loginVO):
        profileList = LoginVO.query.get(loginVO.loginId)
        return profileList

    def userInsertPassword(self,loginVO):
        db.session.merge(loginVO)
        db.session.commit()

