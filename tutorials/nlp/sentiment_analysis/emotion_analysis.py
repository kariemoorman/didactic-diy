from transformers import pipeline
import json

def predict_text_emotion(text, model_name):
    '''
    Predict the emotion of input text using Hugging Face pre-trained models.
  
    Parameters: 
    text: input text to be analyzed (str)
    model_name: name of the pre-trained model ('distilbert', 'roberta', 'distilroberta')
    '''
    if model_name == 'distilbert': 
        classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', top_k=None)
        prediction = classifier(text)
        
    elif model_name == 'roberta': 
        classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
        prediction = classifier(text)
    
    elif model_name == 'distilroberta': 
        classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
        prediction = classifier(text)
    
    return json.dumps(prediction, indent=4)

# Test the model
text = "I am so happy to see you!"
predicted_emotion = predict_text_emotion(text, 'distilbert')

print(f"\nText: {text}")
print(f"Predicted Emotion: {predicted_emotion}")
