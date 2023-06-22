import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification

model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
model.load_weights('gender_model_weights.h5')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
def predict_gender(name):
    encoding = tokenizer([name], truncation=True, padding=True)
    input_dataset = tf.data.Dataset.from_tensor_slices(dict(encoding)).batch(1)
    predictions = model.predict(input_dataset)
    predicted_label = tf.argmax(predictions.logits, axis=1)[0].numpy()
    gender = "male" if predicted_label == 0 else "female"
    return gender

# name = input("Enter a name: ")
# predicted_gender = predict_gender(name)
# print(f"The predicted gender for the name '{name}' is: {predicted_gender}")
