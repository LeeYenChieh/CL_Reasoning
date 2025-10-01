from Model.Model import Model
from Model.ModelFactory import ModelFactory

modelFactory = ModelFactory()
model: Model = modelFactory.buildModel('qwen')

print(model.getRes('一步一步計算1+1等於多少'))