from project import db
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.LoginVO import LoginVO


class RegisterDAO:
    def insertRegister(self, registerVO):
        db.session.add(registerVO)
        db.session.commit()

    def adminViewUser(self):
        userVOList = db.session.query(RegisterVO, LoginVO). \
            join(LoginVO, RegisterVO.register_LoginId == LoginVO.loginId).all()
        return userVOList
