from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.VideoVO import VideoVO


class VideoDAO:

    ##########################USER#################################

    def userInsertVideo(self, videoVO):
        db.session.add(videoVO)

        db.session.commit()

    def userViewVideo(self, videoVO):
        videoList = VideoVO.query.filter_by(videoFrom_LoginId=videoVO.videoFrom_LoginId).all()

        return videoList

    def userDeleteVideo(self, videoVO):
        videoList = VideoVO.query.get(videoVO.videoId)

        db.session.delete(videoList)

        db.session.commit()

        return videoList

    ##################################ADMIN#############################

    def adminViewVideo(self):
        videoList = db.session.query(VideoVO, LoginVO) \
            .join(LoginVO, VideoVO.videoFrom_LoginId == LoginVO.loginId).all()

        return videoList
