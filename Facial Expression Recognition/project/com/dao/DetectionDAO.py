from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.DetectionVO import DetectionVO
from project.com.vo.RegisterVO import RegisterVO


class DetectionDAO():
    ##################################USER#############################

    def insertDetection(self, detectionVO):
        db.session.add(detectionVO)
        db.session.commit()

    def userDeleteDetection(self, detectionVO):
        detectionList = DetectionVO.query.get(detectionVO.detectionId)
        db.session.delete(detectionList)
        db.session.commit()
        return detectionList

    def userViewDetection(self, detectionVO):
        detectionList = DetectionVO.query.filter_by(detectionFrom_LoginId=detectionVO.detectionFrom_LoginId).all()
        return detectionList

    ##################################ADMIN#############################

    def adminViewDetection(self):
        detectionList = db.session.query(DetectionVO, LoginVO) \
            .join(LoginVO, DetectionVO.detectionFrom_LoginId == LoginVO.loginId).all()

        return detectionList

    def getUsers(self):
        detectionList = db.session.query(DetectionVO.detectionFrom_LoginId.distinct(), RegisterVO) \
            .join(RegisterVO, DetectionVO.detectionFrom_LoginId == RegisterVO.register_LoginId).all()
        return detectionList
