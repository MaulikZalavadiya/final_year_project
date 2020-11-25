from project import db
from project.com.vo.ComplainVO import ComplainVO
from project.com.vo.LoginVO import LoginVO


class ComplainDAO:
    def insertComplain(self, complainVO):
        db.session.add(complainVO)
        db.session.commit()

    def viewComplain(self, complainVO):
        complainList = ComplainVO.query.filter_by(complainFrom_LoginId=complainVO.complainFrom_LoginId).all()
        return complainList

    def deleteComplain(self, complainVO):
        complainList = ComplainVO.query.get(complainVO.complainId)

        db.session.delete(complainList)

        db.session.commit()

        return complainList

    def viewComplainReply(self, complainVO):
        complainReplyList = ComplainVO.query.filter_by(complainId=complainVO.complainId).all()
        return complainReplyList

    def adminViewComplain(self, complainVO):
        complainList = db.session.query(ComplainVO, LoginVO) \
            .filter(ComplainVO.complainStatus == complainVO.complainStatus) \
            .join(LoginVO, ComplainVO.complainFrom_LoginId == LoginVO.loginId).all()

        return complainList

    def adminInsertReply(self, complainVO):
        db.session.merge(complainVO)
        db.session.commit()