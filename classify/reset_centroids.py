__author__ = 'ssm'

import numpy as np

cent = np.load("_centroids.npy")

new  = [cent[5],
        cent[3],
        cent[8],
        cent[6],
        cent[0],
        cent[11],
        cent[2],
        cent[13],
        cent[9],
        cent[4],
        cent[7],
        cent[1],
        ]
np.save("centroids.npy", new)