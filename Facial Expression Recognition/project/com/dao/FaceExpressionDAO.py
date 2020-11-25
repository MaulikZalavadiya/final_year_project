from project import db
from project.com.vo.FaceExpressionVO import FaceExpressionVO


class FaceExpressionDAO:
    def insertFaceExpression(self, faceExpressionVO):
        db.session.add(faceExpressionVO)
        db.session.commit()

    def viewFaceExpressionMonth(self, faceExpressionVO):
        faceExpressionList = FaceExpressionVO.query.filter_by(
            faceExpressionFrom_LoginId=faceExpressionVO.faceExpressionFrom_LoginId).all()
        return faceExpressionList

    def viewFaceExpressionDay(self, faceExpressionVO):
        faceExpressionList = FaceExpressionVO.query.filter_by(
            faceExpressionFrom_LoginId=faceExpressionVO.faceExpressionFrom_LoginId,
            faceExpressionUploadDate=faceExpressionVO.faceExpressionUploadDate).all()
        return faceExpressionList

    def userViewExpression(self, faceExpressionVO):
        faceExpressionList = FaceExpressionVO.query.filter_by(
            faceExpression_DetectionId=faceExpressionVO.faceExpression_DetectionId).all()
        return faceExpressionList

