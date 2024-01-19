from variables import Variables
from visualize import Visualize
import pickle

with open(Variables.dumpfile, 'rb') as fp:
    data = pickle.load(fp)

bounds = [-0.5*Variables.box[0], Variables.box[0]+0.5*Variables.box[0], -0.5*Variables.box[1], Variables.box[1]+0.5*Variables.box[1]]
vis = Visualize(data, bounds)