from Context import Context

from Model.Model import Model
from Dataset.Dataset import Dataset

context = Context()
model = Model()
dataset = Dataset()

context.setStrategy('onlyChinese')
context.runExperiment(model, dataset)
