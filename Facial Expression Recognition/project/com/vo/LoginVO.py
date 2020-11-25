from project import db


class LoginVO(db.Model):
    __tablename__ = 'loginmaster'
    loginId = db.Column('loginId', db.INTEGER, primary_key=True, autoincrement=True)
    loginUsername = db.Column('loginUsername', db.String(30), nullable=False)
    loginPassword = db.Column('loginPassword', db.String(60), nullable=False)
    loginRole = db.Column('loginRole', db.String(60), nullable=False)
    loginStatus = db.Column('loginStatus', db.String(60), nullable=False)

    def as_dict(self):
        return {
            'loginId': self.loginId,
            'loginUsername': self.loginUsername,
            'loginPassword': self.loginPassword,
            'loginRole': self.loginRole,
            'loginStatus': self.loginStatus
        }


db.create_all()
