from variables import Variables
from visualize import Visualize
import pickle

with open("checkpoints/N_49.save", 'rb') as fp:
    data = pickle.load(fp)

bounds = [0, Variables.box[0], 0, Variables.box[1]]
vis = Visualize(data, bounds)