import cv2

## Download haarcascade_frontalface_default.xml using the following link, and place it in the : 
#    -  https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml

## For side profile (portrait) use the following link: 
#    -  #https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_profileface.xml

classifier = './haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(classifier)

def face_detection(video_filepath): 
    cap = cv2.VideoCapture(video_filepath)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(3))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(
        'video_output.mp4',
        fourcc,
        20.0, 
        (frame_width, frame_height))

    while True: 
        ret, frame = cap.read()
        if not ret: 
            break
        gray = cv2.cvtColor(
            frame, 
            cv2.COLOR_BGR2GRAY
        )
        
        faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1, minNeighbors=5,
        minSize=(30,30)
        )
        
        for (x,y,w, h) in faces:
            cv2.rectangle(
                frame,
                (x,y),
                (x + w, y + h),
                (0, 255, 0), 
                3
            )
        out.write(frame)
        
        cv2.imshow(
            'Face Detection', 
            frame
        )
        
        if cv2.waitKey(1) & 0xFF ==ord('q'): 
            break
        
    cap.release()
    out.release()    

    cv2.destroyAllWindows()
    
