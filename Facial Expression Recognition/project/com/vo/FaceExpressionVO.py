from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.DetectionVO import DetectionVO


class FaceExpressionVO(db.Model):
    __tablename__ = 'faceexpressionmaster'
    faceExpressionId = db.Column('faceExpressionId', db.Integer, primary_key=True, autoincrement=True)
    angryCount = db.Column('angryCount', db.Integer,nullable=True)
    disgustCount = db.Column('disgustCount', db.Integer,nullable=True)
    fearCount = db.Column('fearCount', db.Integer,nullable=True)
    happyCount = db.Column('happyCount', db.Integer,nullable=True)
    sadCount = db.Column('sadCount', db.Integer,nullable=True)
    surpriseCount = db.Column('surpriseCount', db.Integer,nullable=True)
    neutralCount = db.Column('neutralCount', db.Integer,nullable=True)
    faceExpression_DetectionId = db.Column('faceExpression_DetectionId', db.Integer, db.ForeignKey(DetectionVO.detectionId))

    def as_dict(self):
        return {
            'faceExpressionId': self.faceExpressionId,
            'angryCount': self.angryCount,
            'disgustCount': self.disgustCount,
            'fearCount': self.fearCount,
            'happyCount': self.happyCount,
            'sadCount': self.sadCount,
            'surpriseCount': self.surpriseCount,
            'neutralCount': self.neutralCount,
            'detectionDate': self.detectionDate,
            'detectionTime': self.detectionTime,
            'faceExpression_DetectionId': self.faceExpression_DetectionId,
        }


db.create_all()
