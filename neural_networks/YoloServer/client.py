import numpy as np
import requests
import pickle

ones = np.ones((2,3))
print(ones)
requests.post("http://localhost:5000/predict", pickle.dumps(ones))