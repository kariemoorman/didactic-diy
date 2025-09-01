## pip install numpy pillow ultralytics opencv-python

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
from ultralytics import YOLO



def process_image(image_filepath: str, model_type: str):
  '''
  Example:
  process_image(image_filepath, 'obj')
  process_image(image_filepath, 'pose')
  process_image(image_filepath, 'seg')
  '''
    if not os.path.isfile(image_filepath):
        raise ValueError(f"Invalid file path: {image_filepath}. The file does not exist or is not a valid file.")
    
    model_dict = {
        'pose': "yolo11m-pose.pt",
        'obj': "yolo11m.pt",
        'seg': "yolo11m-seg.pt"
    }

    model_name = model_dict.get(model_type)

    if model_name is None:
        raise ValueError(f"Invalid model_type: {model_type}. Choose from 'pose', 'obj', or 'seg'.")
    
    model = YOLO(model_name)

    filepath = os.path.splitext(os.path.basename(image_filepath))[0]
    results = model(image_filepath)
    for result in results:
        annotated_image = result.plot()
    cv2.imwrite(f"{filepath}_{model_type}.png", annotated_image)


def extract_image_objs(image_filepath: str, background_type: str ='transparent'):
  '''
  Example:
  extract_image_objs(image_filepath, 'black')
  extract_image_objs(image_filepath, 'transparent')
  '''
    if not os.path.isfile(image_filepath):
        raise ValueError(f"Invalid file path: {image_filepath}. The file does not exist or is not a valid file.")
    
    if background_type not in ['black', 'transparent']:
        raise ValueError(f"Invalid background_type: {background_type}. Please select 'transparent' or 'black'.")

    filepath = os.path.splitext(os.path.basename(image_filepath))[0]

    model = YOLO("yolo11m-seg.pt")

    results = model.predict(image_filepath)
    result = results[0]
    masks = result.masks
    class_names = result.names
    img = cv2.imread(image_filepath)
    if masks is not None:
        for j, mask in enumerate(masks):
            mask_array = mask.data[0].numpy()
            mask_resized = cv2.resize(mask_array, (img.shape[1], img.shape[0]))
            binary_mask = np.uint8(mask_resized * 255)
            if background_type == 'black':
                mask_img = np.zeros_like(img)
                mask_img[binary_mask == 255] = img[binary_mask == 255]
            elif background_type == 'transparent':
                mask_img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
                mask_img[:, :, 3] = 0
                mask_img[binary_mask == 255, :3] = img[binary_mask == 255]
                mask_img[binary_mask == 255, 3] = 255
            class_idx = result.boxes.cls[j]
            class_name = class_names[int(class_idx)]
            output_filename = f'{filepath}_{class_name}_{j}_{background_type}.png'
            cv2.imwrite(output_filename, mask_img)
            print(f"Saved extracted object {j} as {output_filename}")
    else:
        print(f"No masks found for result")



def process_video(video_filepath: str):
  '''
  Example:
  process_video(video_filepath)
  '''
    if not os.path.isfile(video_filepath):
        raise ValueError(f"Invalid file path: {video_filepath}. The file does not exist or is not a valid file.")

    filepath = os.path.splitext(os.path.basename(video_filepath))[0]
    model = YOLO("yolo11n-pose.pt") 

    cap = cv2.VideoCapture(video_filepath)  

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_filepath = f"{filepath}_pose.mp4"
    out = cv2.VideoWriter(output_filepath, 
                        cv2.VideoWriter_fourcc(*'mp4v'), fps, 
                        (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model(frame, show=False, verbose=False)

        if results:
            result = results[0]
            annotated_frame = result.plot()
            people_count = sum(1 for cls in result.boxes.cls if cls == 0) 
            cv2.putText(annotated_frame, f"Person Count: {people_count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            out.write(annotated_frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
