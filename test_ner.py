import urduhack.models.ner.predict as predict

print(predict.predict_ner("پاکستان ایک برا ملک ہے "))

print(predict.predict_ner("Pakistan is a Big Country. Hussey loves it"))

print(predict.predict_ner("پاکستان ایک بڑا ملک ہے۔ احمد اسے پسند کرتا ہے۔"))
