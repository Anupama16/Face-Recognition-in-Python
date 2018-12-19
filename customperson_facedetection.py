# import libraries
import cv2
import face_recognition

# Get a reference to webcam 
input_movie = cv2.VideoCapture("billgates_speech.mp4")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

images = ["billgates.png","billgates2.jpg","billgates3.jpg","billgates4.jpg","billgates5.jpg"]

known_faces = []
for images in images:
    image = face_recognition.load_image_file(images)
    face_encoding = face_recognition.face_encodings(image)[0]

    known_faces.append(face_encoding)


#fourcc = int(input_movie.get(cv2.CAP_PROP_FOURCC))
#fourcc = cv2.VideoWriter_fourcc('M', 'P', 'E', 'G')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = int(input_movie.get(cv2.CAP_PROP_FPS))
frame_width = int(input_movie.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT))
output_movie = cv2.VideoWriter("Output.mp4", fourcc, fps, (frame_width,frame_height))



# Initialize variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    if not ret:
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]
    #rgb_frame = frame

    # Find all the faces in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    bg = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.40)
        print(match)
        print(len(match))
        
        name = None

        for i in range(len(match)):
            if match[i]:
                name = "Bill Gates"
                face_names.append(name)
                bg.append(face_locations[face_encoding])
        

    # Display the results
    for top, right, bottom, left in bg:
        if not name:
            continue

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)


    # Write the resulting image to the output video file
    #if frame_number/100 == 0:
    print("Writing frame {} / {}".format(frame_number, length))
    #output_movie.write(frame)
    output_movie.write(frame)

# Release handle to the webcam
input_movie.release()
output_movie.release()
cv2.destroyAllWindows()



