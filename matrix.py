import numpy as np
import cv2
import os
import math
#from collage import get_image_names





matricita = range(16)
print matricita

final_size_1 = int(math.sqrt(len(matricita)))
print final_size_1
#final_size_2 = int(math.sqrt(len(matricita[0])))
#print final_size_2
final_size_1 = int(math.sqrt(len(matricita)))
matrix = np.reshape(matricita,(final_size_1, final_size_1))
#for i in range(len(matricita)):
#	row = []
#	for j in range(final_size_1):
#		row.append(matricita[i*j])
#	matrix.append(row)




print matrix