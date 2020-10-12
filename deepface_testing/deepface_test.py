from deepface import DeepFace

obj = DeepFace.analyze(img_path='michael.jpg', actions = ['race'])

print(obj)