from tensorflow_core.python.keras.models import load_model

from project import app
from flask import render_template, request, redirect, url_for, session, jsonify
import random
import string
from datetime import datetime
from project.com.dao.DetectionDAO import DetectionDAO
from project.com.vo.DetectionVO import DetectionVO
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession

### General imports ###
# from __future__ import division

import numpy as np
import pandas as pd
import cv2

from time import time
from time import sleep
import re
import os

import argparse
from collections import OrderedDict

### Image processing ###
from scipy.ndimage import zoom
from scipy.spatial import distance
import imutils
from scipy import ndimage

import dlib

from imutils import face_utils
from project.com.dao.FaceExpressionDAO import FaceExpressionDAO
from project.com.vo.FaceExpressionVO import FaceExpressionVO

import requests

global shape_x
global shape_y
global input_shape
global nClasses


##########################USER##########################

@app.route('/user/liveDetection')
def userLiveDetection():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/liveDetection.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/live')
def userLoadLive():
    try:
        if adminLoginSession() == 'user':

            shape_x = 48
            shape_y = 48
            input_shape = (shape_x, shape_y, 1)
            nClasses = 7

            thresh = 0.25
            frame_check = 20
            faceexpression = {0}

            def eye_aspect_ratio(eye):
                A = distance.euclidean(eye[1], eye[5])
                B = distance.euclidean(eye[2], eye[4])
                C = distance.euclidean(eye[0], eye[3])
                ear = (A + B) / (2.0 * C)
                return ear

            def detect_face(frame):

                # Cascade classifier pre-trained model
                cascPath = "project/static/adminResources/Landmarks/face_landmarks.dat"
                faceCascade = cv2.CascadeClassifier(cascPath)

                # BGR -> Gray conversion
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Cascade MultiScale classifier
                detected_faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6,
                                                              minSize=(shape_x, shape_y),
                                                              flags=cv2.CASCADE_SCALE_IMAGE)
                coord = []

                for x, y, w, h in detected_faces:
                    if w > 100:
                        sub_img = frame[y:y + h, x:x + w]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 1)
                        coord.append([x, y, w, h])

                return gray, detected_faces, coord

            def extract_face_features(faces, offset_coefficients=(0.075, 0.05)):
                gray = faces[0]
                detected_face = faces[1]

                new_face = []

                for det in detected_face:
                    x, y, w, h = det

                    horizontal_offset = np.int(np.floor(offset_coefficients[0] * w))
                    vertical_offset = np.int(np.floor(offset_coefficients[1] * h))

                    extracted_face = gray[y + vertical_offset:y + h, x + horizontal_offset:x - horizontal_offset + w]

                    new_extracted_face = zoom(extracted_face,
                                              (shape_x / extracted_face.shape[0], shape_y / extracted_face.shape[1]))

                    new_extracted_face = new_extracted_face.astype(np.float32)

                    new_extracted_face /= float(new_extracted_face.max())

                    new_face.append(new_extracted_face)

                return new_face

            (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
            (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

            (nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
            (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
            (jStart, jEnd) = face_utils.FACIAL_LANDMARKS_IDXS["jaw"]

            (eblStart, eblEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
            (ebrStart, ebrEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]

            model = load_model("project/static/adminResources/EmotionXCeption/video.h5")
            face_detect = dlib.get_frontal_face_detector()
            predictor_landmarks = dlib.shape_predictor("project/static/adminResources/Landmarks/face_landmarks.dat")

            # video_capture = cv2.VideoCapture('project/static/adminResources/videos/lunch_scene.mp4')
            video_capture = cv2.VideoCapture(0)

            fourcc = cv2.VideoWriter_fourcc(
                *'vp80')  # four character code give the video ext. , color and value of the pixel

            filepath = "project/static/adminResources/livedetection/"
            randomNo = random.randint(1, 1000)
            filename = 'output_{}.webm'.format(randomNo)

            outputVideo = filepath + filename
            print('óutputVideo>>>>>', outputVideo)

            frame_width = int(video_capture.get(3))
            frame_height = int(video_capture.get(4))
            fps = int(video_capture.get(5))
            print(frame_width, frame_height, fps)

            out = cv2.VideoWriter(outputVideo, fourcc, fps, (frame_width, frame_height))

            angryCount = 0
            disgustCount = 0
            fearCount = 0
            happyCount = 0
            sadCount = 0
            surpriseCount = 0
            neutralCount = 0

            while True:

                ret, frame = video_capture.read()
                # print(ret)
                if ret == True:
                    face_index = 0

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    rects = face_detect(gray, 1)

                    for (i, rect) in enumerate(rects):

                        shape = predictor_landmarks(gray, rect)
                        shape = face_utils.shape_to_np(shape)

                        (x, y, w, h) = face_utils.rect_to_bb(rect)

                        face = gray[y:y + h, x:x + w]
                        try:

                            face = zoom(face, (shape_x / face.shape[0], shape_y / face.shape[1]))

                        except:
                            break

                        face = face.astype(np.float32)

                        face /= float(face.max())
                        face = np.reshape(face.flatten(), (1, 48, 48, 1))

                        prediction = model.predict(face)
                        prediction_result = np.argmax(prediction)

                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        cv2.putText(frame, "Face #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (0, 255, 0), 2)

                        for (j, k) in shape:
                            cv2.circle(frame, (j, k), 1, (0, 0, 255), -1)

                        cv2.putText(frame, "----------------", (40, 100 + 180 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255,
                                    0)
                        cv2.putText(frame, "Emotional report : Face #" + str(i + 1), (40, 120 + 180 * i),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 0)
                        cv2.putText(frame, "Angry : " + str(round(prediction[0][0], 3)), (40, 140 + 180 * i),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 0)
                        cv2.putText(frame, "Disgust : " + str(round(prediction[0][1], 3)), (40, 160 + 180 * i),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 0)
                        cv2.putText(frame, "Fear : " + str(round(prediction[0][2], 3)), (40, 180 + 180 * i),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
                        cv2.putText(frame, "Happy : " + str(round(prediction[0][3], 3)), (40, 200 + 180 * i),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
                        cv2.putText(frame, "Sad : " + str(round(prediction[0][4], 3)), (40, 220 + 180 * i),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
                        cv2.putText(frame, "Surprise : " + str(round(prediction[0][5], 3)), (40, 240 + 180 * i),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
                        cv2.putText(frame, "Neutral : " + str(round(prediction[0][6], 3)), (40, 260 + 180 * i),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)

                        if prediction_result == 0:
                            cv2.putText(frame, "Angry", (x + w - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                        2)
                            angryCount += 1
                            print("Angry")
                        elif prediction_result == 1:
                            cv2.putText(frame, "Disgust", (x + w - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (0, 255, 0), 2)
                            disgustCount += 1
                            print("Disgust")
                        elif prediction_result == 2:
                            cv2.putText(frame, "Fear", (x + w - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                        2)
                            fearCount += 1
                            print("Fear")
                        elif prediction_result == 3:
                            cv2.putText(frame, "Happy", (x + w - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                        2)
                            happyCount += 1
                            print("Happy")
                        elif prediction_result == 4:
                            cv2.putText(frame, "Sad", (x + w - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            sadCount += 1
                            print("Sad")
                        elif prediction_result == 5:
                            cv2.putText(frame, "Surprise", (x + w - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (0, 255, 0), 2)
                            surpriseCount += 1
                            print("Surprise")
                        else:
                            cv2.putText(frame, "Neutral", (x + w - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (0, 255, 0), 2)
                            neutralCount += 1
                            print("Neutral")

                        leftEye = shape[lStart:lEnd]
                        rightEye = shape[rStart:rEnd]

                        leftEAR = eye_aspect_ratio(leftEye)
                        rightEAR = eye_aspect_ratio(rightEye)
                        ear = (leftEAR + rightEAR) / 2.0

                        # leftEyeHull = cv2.convexHull(leftEye)
                        # rightEyeHull = cv2.convexHull(rightEye)
                        # cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                        # cv2.drawContours(frame, [11111111111rightEyeHull], -1, (0, 255, 0), 1)

                        # nose = shape[nStart:nEnd]
                        # noseHull = cv2.convexHull(nose)
                        # cv2.drawContours(frame, [noseHull], -1, (0, 255, 0), 1)

                        # mouth = shape[mStart:mEnd]
                        # mouthHull = cv2.convexHull(mouth)
                        # cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

                        # jaw = shape[jStart:jEnd]
                        # jawHull = cv2.convexHull(jaw)
                        # cv2.drawContours(frame, [jawHull], -1, (0, 255, 0), 1)

                        # ebr = shape[ebrStart:ebrEnd]
                        # ebrHull = cv2.convexHull(ebr)
                        # cv2.drawContours(frame, [ebrHull], -1, (0, 255, 0), 1)
                        # ebl = shape[eblStart:eblEnd]
                        # eblHull = cv2.convexHull(ebl)
                        # cv2.drawContours(frame, [eblHull], -1, (0, 255, 0), 1)

                    cv2.putText(frame, 'Number of Faces : ' + str(len(rects)), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                155, 1)
                    out.write(frame)

                    cv2.imshow('Video', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break

            # When everything is done, release the capture
            video_capture.release()
            out.release()
            cv2.destroyAllWindows()

            detectionDAO = DetectionDAO()
            detectionVO = DetectionVO()
            faceExpressionVO = FaceExpressionVO()
            faceExpressionDAO = FaceExpressionDAO()

            uploadDate = datetime.today().strftime("%d/%m/%Y")

            uploadTime = datetime.now().strftime("%H:%M:%S")

            detectionVO.detectionFileName = filename
            detectionVO.detectionFilePath = filepath.replace('project', '..')
            detectionVO.detectionUploadDate = uploadDate
            detectionVO.detectionUploadTime = uploadTime
            detectionVO.detectionFrom_LoginId = session['session_loginId']

            detectionDAO.insertDetection(detectionVO)

            faceExpressionVO.angryCount = angryCount
            faceExpressionVO.disgustCount = disgustCount
            faceExpressionVO.fearCount = fearCount
            faceExpressionVO.happyCount = happyCount
            faceExpressionVO.sadCount = sadCount
            faceExpressionVO.surpriseCount = surpriseCount
            faceExpressionVO.neutralCount = neutralCount
            faceExpressionVO.faceExpression_DetectionId = detectionVO.detectionId

            faceExpressionDAO.insertFaceExpression(faceExpressionVO)

            return redirect(url_for("userViewDetection"))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewDetection', methods=['GET'])
def userViewDetection():
    try:
        if adminLoginSession() == 'user':
            detectionVO = DetectionVO()
            detectionDAO = DetectionDAO()

            # detectionId = request.args.get('detectionId')

            detectionVO.detectionFrom_LoginId = session['session_loginId']

            detectionVOList = detectionDAO.userViewDetection(detectionVO)

            return render_template('user/viewDetection.html', detectionVOList=detectionVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteDetection', methods=['GET'])
def userDeleteDetection():
    try:
        if adminLoginSession() == "user":

            detectionVO = DetectionVO()
            detectionDAO = DetectionDAO()

            detectionId = request.args.get('detectionId')

            detectionVO.detectionId = detectionId

            detectionList = detectionDAO.userDeleteDetection(detectionVO)

            path = detectionList.detectionFilePath.replace("..", "project") + detectionList.detectionFileName
            os.remove(path)

            return redirect(url_for('userViewDetection'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


#######################ADMIN###############################

@app.route('/admin/viewDetection', methods=['GET'])
def adminViewDetection():
    try:
        if adminLoginSession() == 'admin':
            detectionDAO = DetectionDAO()
            detectionVOList = detectionDAO.adminViewDetection()

            return render_template('admin/viewDetection.html', detectionVOList=detectionVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewExpression', methods=['GET'])
def userViewExpression():
    try:
        if adminLoginSession() == 'user':
            detectionId = request.args.get('detectionId')
            faceExpressionVO = FaceExpressionVO()
            faceExpressionDAO = FaceExpressionDAO()
            faceExpressionVO.faceExpression_DetectionId = detectionId
            faceExpressionList = faceExpressionDAO.userViewExpression(faceExpressionVO)

            return render_template('user/viewFaceExpression.html', faceExpressionList=faceExpressionList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxLoadDetection')
def adminAjaxDateRegister():
    index_User_LoginId = request.args.get('index_User_LoginId')

    detectionVO = DetectionVO()

    detectionDAO = DetectionDAO()

    detectionVO.detectionFrom_LoginId = index_User_LoginId

    ajaxDetectionVOList = detectionDAO.userViewDetection(detectionVO)

    print("ajaxDetectionVOList >>>>>>>>>>>>>>>>>> ", ajaxDetectionVOList)

    ajaxDetectionDictList = [i.as_dict() for i in ajaxDetectionVOList]

    print("ajaxDetectionDictList >>>>>>>>>>>>>>>>>> ", ajaxDetectionDictList)

    return jsonify(ajaxDetectionDictList)


@app.route('/admin/ajaxGetGraphData')
def adminAjaxGetGraphData():
    index_DetectionId = request.args.get('index_DetectionId')

    faceExpressionVO = FaceExpressionVO()
    faceExpressionDAO = FaceExpressionDAO()

    faceExpressionVO.faceExpression_DetectionId = index_DetectionId

    ajaxGraphDataList = faceExpressionDAO.userViewExpression(faceExpressionVO)

    print("ajaxGraphDataList >>>>>>>>>>>>>>>>>> ", ajaxGraphDataList)

    graphDict = {}
    counter = False
    if len(ajaxGraphDataList) != 0:
        counter = True
        graphDict = {"angryCount": ajaxGraphDataList[0].angryCount, "disgustCount": ajaxGraphDataList[0].disgustCount,
                     "fearCount": ajaxGraphDataList[0].fearCount, "happyCount": ajaxGraphDataList[0].happyCount,
                     "sadCount": ajaxGraphDataList[0].sadCount, "surpriseCount": ajaxGraphDataList[0].surpriseCount,
                     "neutralCount": ajaxGraphDataList[0].neutralCount}

    print('graphDict>>>', graphDict)
    if counter:
        response = {'responseKey': graphDict}
        print('response>>>>>>>>', response)

    else:
        response = {'responseKey': 'Error'}

    return jsonify(response)


'''   ************************************     '''
# from flask import request, render_template, redirect, url_for, session
# from project import app
# import numpy
# import cv2
# from project.com.controller.LoginController import adminLoginSession, adminLogoutSession


# @app.route('/user/viewDetection', methods=['GET'])
# def userViewDetection():
#     try:
#         if adminLoginSession() == 'user':
#             return render_template('user/webCam.html')
#         else:
#             return adminLogoutSession()
#     except Exception as ex:
#         print(ex)
#
# @app.route('/user/live')
# def userLoadLive():
#     try:
#         if adminLoginSession() == 'user':
#             cap = cv2.VideoCapture(0)
#
#             # Check if the webcam is opened correctly
#             if not cap.isOpened():
#                 raise IOError("Cannot open webcam")
#
#             while True:
#                 ret, frame = cap.read()
#                 frame = cv2.resize(frame, None, fx=1.0, fy=1.0, interpolation=cv2.INTER_AREA)
#                 cv2.imshow('Input', frame)
#
#                 c= cv2.waitKey(1)
#                 if c==27:
#                     break
#
#             cap.release()
#             cv2.destroyAllWindows()
#             return redirect(url_for('userViewDetection'))
#
#         else:
#             return adminLogoutSession()
#
#     except Exception as ex:
#         print(ex)
