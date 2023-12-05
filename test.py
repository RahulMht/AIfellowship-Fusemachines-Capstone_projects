import cv2
import numpy as np
import utils
import time 

webCamFeed = False
Tval = 178  # 178 / 240

pathImage = r"D:\OMR project\Data\1001.1.jpeg"
heightImg = 707
widthImg  = 500
questions=50
choices=4
ans=[0, 1, 1, 2, 0, 3, 1, 3, 1, 2, 1, 2, 1, 3, 0, 2, 1, 2, 1, 3, 1, 3, 1, 3, 0, 0, 0, 1, 0, 3, 0, 1, 3, 1, 1, 0, 2, 3, 1, 3, 1, 3, 2, 1, 3, 1, 3, 1, 2, 3]
cameraNo=0

cap = cv2.VideoCapture(cameraNo)
cap.set(10,150)
count=0

while True:

      if webCamFeed:
            success, img = cap.read()
      else:
            img = cv2.imread(pathImage)

      #preprocessimg
      img = cv2.resize(img, (widthImg, heightImg)) # RESIZE IMAGE
      imgContours = img.copy()
      imgBigContour = img.copy()
      imgFinal =img.copy()
      imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
      imgBlur = cv2.GaussianBlur(imgGray, (5, 5),1) # ADD GAUSSIAN BLUR
      retval, threshold = cv2.threshold(imgBlur, Tval, 255, cv2.THRESH_BINARY_INV) 
      try:

            contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # FIND ALL CONTOURS
            cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
            # find rectangle
            rectCon = utils.rectContour(contours) # FILTER FOR RECTANGLE CONTOURS
            print(len(rectCon))
            biggestPoints= utils.getCornerPoints(rectCon[0]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
            secPoints = utils.getCornerPoints(rectCon[1]) # GET CORNER POINTS OF THE SECOND BIGGEST RECTANGLE
            gradePoints = utils.getCornerPoints(rectCon[2]) # GET CORNER POINTS OF THE SECOND BIGGEST RECTANGLE

            if biggestPoints.size != 0 and gradePoints.size != 0 and secPoints.size != 0:

            #     # BIGGEST RECTANGLE WARPING
                  biggestPoints= utils.reorder(biggestPoints) # REORDER FOR WARPING
                  cv2.drawContours(imgBigContour, biggestPoints, -1, (0, 255, 0), 10) # DRAW THE BIGGEST CONTOUR
                  pts1 = np.float32(biggestPoints) # PREPARE POINTS FOR WARP
                  pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
                  matrix = cv2.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
                  imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE

                  
                  secPoints= utils.reorder(secPoints) # REORDER FOR WARPING
                  cv2.drawContours(imgBigContour, secPoints, -1, (255, 255, 0), 10) # DRAW THE BIGGEST CONTOUR
                  spts1 = np.float32(secPoints) # PREPARE POINTS FOR WARP
                  spts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
                  matrix = cv2.getPerspectiveTransform(spts1, spts2) # GET TRANSFORMATION MATRIX
                  simgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE

                  gradePoints= utils.reorder(gradePoints) # REORDER FOR WARPING
                  cv2.drawContours(imgBigContour,  gradePoints, -1, (255,0, 0), 10) # DRAW THE BIGGEST CONTOUR
                  gpts1 = np.float32(gradePoints) # PREPARE POINTS FOR WARP
                  gpts2 = np.float32([[0, 0],[450, 0], [0, 100],[450, 100]]) # PREPARE POINTS FOR WARP
                  matrix = cv2.getPerspectiveTransform(gpts1, gpts2) # GET TRANSFORMATION MATRIX
                  imgGradeDisplay = cv2.warpPerspective(img, matrix, (450,100)) # APPLY WARP PERSPECTIVE
                  print()

            img1WarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
            img2WarpGray = cv2.cvtColor(simgWarpColored,cv2.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
            img1Thresh = cv2.threshold(img1WarpGray, 84, 255,cv2.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE
            img2Thresh = cv2.threshold(img2WarpGray, 84, 255,cv2.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE

            boxes = utils.splitBoxes(img1Thresh,img2Thresh) # GET INDIVIDUAL BOXES
            # cv2.imshow("Split Test ", boxes[195])
            countR=0
            countC=0
            myPixelVal = np.zeros((questions,choices)) # TO STORE THE NON ZERO VALUES OF EACH BOX
            for image in boxes:
                  totalPixels = cv2.countNonZero(image)
                  myPixelVal[countR][countC]= totalPixels
                  countC += 1
                  if (countC==choices):countC=0;countR +=1


            myIndex=[]
            for x in range (0,questions):
                  arr = myPixelVal[x]
                  myIndexVal = np.where(arr == np.amax(arr))
                  myIndex.append(myIndexVal[0][0])
            print(myIndex)
            grading=[]
            for x in range(0,questions):
                  if ans[x] == myIndex[x]:
                        grading.append(1)
                  else:grading.append(0)
            #print("GRADING",grading)
            score = (sum(grading)/questions)*100 # FINAL GRADE
            print("SCORE",score)


            # DISPLAYING ANSWERS
            imageresult = imgWarpColored.copy()
            utils.showAnswers(imageresult,myIndex[:25],grading[:25],ans[:25]) # DRAW DETECTED ANSWERS
            imageresult2 = simgWarpColored.copy()
            utils.showAnswers(imageresult2,myIndex[25:],grading[25:],ans[25:]) # DRAW DETECTED ANSWERS

            imgRawDrawings = np.zeros_like(imgWarpColored) # NEW BLANK IMAGE WITH WARP IMAGE SIZE
            imgRawDrawings2 =  np.zeros_like(simgWarpColored) # NEW BLANK IMAGE WITH WARP IMAGE SIZE
            utils.showAnswers(imgRawDrawings,myIndex[:25],grading[:25],ans[:25]) # DRAW ON NEW IMAGE
            utils.showAnswers(imgRawDrawings2,myIndex[25:],grading[25:],ans[25:]) # DRAW ON NEW IMAGE

            invMatrix = cv2.getPerspectiveTransform(pts2, pts1) # INVERSE TRANSFORMATION MATRIX
            imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (widthImg, heightImg)) # INV IMAGE WARP

            invMatrix2 = cv2.getPerspectiveTransform(spts2, spts1) # INVERSE TRANSFORMATION MATRIX
            imgInvWarp2 = cv2.warpPerspective(imgRawDrawings2, invMatrix2, (widthImg, heightImg)) # INV IMAGE WARP


            # DISPLAY GRADE
            imgRawGrade = np.zeros_like(imgGradeDisplay,np.uint8) # NEW BLANK IMAGE WITH GRADE AREA SIZE
            cv2.putText(imgRawGrade,str(int(score))+"%",(135,60)
                        ,cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),3) # ADD THE GRADE TO NEW IMAGE
            invMatrixG = cv2.getPerspectiveTransform(gpts2, gpts1) # INVERSE TRANSFORMATION MATRIX
            imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg, heightImg)) # INV IMAGE WARP

            # SHOW ANSWERS AND GRADE ON FINAL IMAGE
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1,0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp2, 1,0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1,0)


            imageBlank = np.zeros_like(img)
            lables = [["Original","Threshold","Contours"],
              ["Left Half","Right Half","Final"]]
            
            imageArray = ([img,threshold, imgContours],[imageresult,imageresult2,imgFinal])
            

            stackedImage = utils.stackImages(imageArray,0.5)
            cv2.imshow("stacked images", stackedImage)
            cv2.imshow("output",imgFinal )
            if cv2.waitKey(1) & 0xFF == ord('s'):
                  cv2.imwrite("Scanned/myImage"+str(count)+".jpg",imgFinal)
                  cv2.putText(stackedImage, "Scan Saved press q to close", (int(stackedImage.shape[1] / 2) - 300, int(stackedImage.shape[0] / 2)),
                              cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 255), 4, cv2.LINE_AA)
                  cv2.imshow('Process', imgFinal)
                  cv2.waitKey(300)
                  time.sleep(3)


      except:
            lables = [["Original","Threshold","Contours"],
              ["Left Half","Right Half","Final"]]
            imageBlank = np.zeros_like(img)
            imageArray = ([img,threshold, imgContours],[imageBlank,imageBlank, imageBlank])
            stackedImage = utils.stackImages(imageArray,0.5)
            cv2.imshow("stacked images", stackedImage)
      if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite("Scanned/myImage"+str(count)+".jpg",imgFinal)
            cv2.putText(stackedImage, "Scan Saved", (int(stackedImage.shape[1] / 2) - 200, int(stackedImage.shape[0] / 2)),
                        cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)
            cv2.imshow('Result', stackedImage)
            cv2.waitKey(300)
            count += 1
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break