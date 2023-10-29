from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import pandas as pd

def fb_image_object_detection(image_filepath, threshold=0.9): 
    image = Image.open(image_filepath)
    
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]])
    
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=threshold)[0]

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        print(
                f"Detected '{model.config.id2label[label.item()]}' with confidence "
                f"{round(score.item(), 3)} at location {box}"
        )
        

def yolov_image_object_detection(image_filepath): 
    image = Image.open(image_filepath)
    
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    
    results = model(image, size=640)
    results.print()
    results.show()
    table = results.pandas().xyxy[0]
    return table

