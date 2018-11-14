import numpy as np
import cv2
import os
import math
import random
import datetime


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - Collage Maker!- - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - Global Variables - - - - - - - - 
direct = os.getcwd()
#images_loc = '/images/'
images_loc = direct + '/images/'
images_square_loc = direct + '/square_images_equal_size/'
merged_images_loc = direct + '/merged_images/'
#images_square_loc = '/test/'
border_color = [0,0,0]
border_lenght = 5
square_size = 150
formato = ".jpg"
max_size = 1000
collage_rows = 30
collage_cols = 30
image_repeat = True
image_ramdomize = True
create_small_images = True



# - - - - - - - - - - - - - - - - - -
# - - - - - Functions - - - - - - - -
# - - - - - - - - - - - - - - - - - -

def nearest_even_down(num_):
	#If odd
	if num_ % 2 == 0:
		return num_
	else:
		return int((math.ceil(num_ / 2.) * 2) - 2)

def remove_extension(name_):
	if name_.endswith(".jpg"):
		return name_.rstrip('.jpg')
	elif name_.endswith(".png"):
		return name_.rstrip('.png')


#This function turns every image in the into a square of 
#the desired dimensions
def make_squares(images_source_fp, images_square_fp, side_lenght_):
	cuantas = 0
	for filename in os.listdir(images_source_fp):
		if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
			cuantas += 1
			print cuantas
			#creates a new image with the centered square of the original image
			#Extracts the image dimensions
			im_ = cv2.imread(images_source_fp  + filename)
			h, w = im_.shape[:2]
			print "dimensions: " + str(w) + " x " + str(h)

			#Determines the side lenght of the squared image to be created
			short_side = nearest_even_down(min(h,w))
			long_side = nearest_even_down(max(h,w))
			print "New Side: " + str(short_side)

			#stacked = np.vstack((stacked, im_))
			mid_p_h = short_side/2
			r_bound_h = short_side/2 + int(short_side/2)
			l_bound_h = short_side/2 - int(short_side/2)

			r_bound_v = long_side/2 + int(short_side/2)
			l_bound_v = long_side/2 - int(short_side/2)

			try:
				stacked = np.array(im_[l_bound_h:r_bound_h,l_bound_v:r_bound_v,:])
				print "try - - - - - -"
			except e as error:
				print "except - - - - - -" + e.args
				stacked = np.array(im_[l_bound_h:r_bound_h,l_bound_v:r_bound_v,:])

			# Saves the image in the imagenes_small 
			new_file_name = images_square_fp + "img_squared_" + str(cuantas) + ".jpg"

			stacked_stnd = cv2.resize(stacked, (side_lenght_,side_lenght_))
			cv2.imwrite(new_file_name,stacked_stnd)
			
			#print cuantas
			#cv2.imshow(str(filename), stacked)
			#cv2.waitKey(0)
			#cv2.destroyAllWindows()


def get_image_names(location_fp):
	image_names = []
	for filename in os.listdir(location_fp):
		if filename.endswith(".jpg") or filename.endswith(".png"):
			image_names.append(filename)
	return image_names

#Creates a collage with all the images in the given matrix
def make_collage(name_matrix_, border_lenght_, square_size_, maximum_size_):
	row_num, col_num = name_matrix_.shape[:2]

	#Creates the outtermost left border so it can attach columns to its right as the loop advances
	cols = np.zeros((1 +(square_size+border_lenght_)*row_num, border_lenght_, 3), np.uint8)

	for j in range(0, len(name_matrix_[0])):
		#Creates the top border so that it can attach images to its bottom
		rows = np.zeros((1,square_size_, 3), np.uint8)
		for i in range(0, len(name_matrix_)):

			im_a = cv2.imread(images_square_loc  + name_matrix_[i][j])
			#border parameters: top, bottom, left, right
			rows = cv2.copyMakeBorder(rows,0,border_lenght_,0,0,cv2.BORDER_CONSTANT,value=border_color)
			rows = np.concatenate((rows, im_a), axis=0)

		cols = np.concatenate((cols, rows), axis=1)
		cols = cv2.copyMakeBorder(cols,0,0,0,border_lenght_,cv2.BORDER_CONSTANT,value=border_color)
	cols = cv2.copyMakeBorder(cols,0,border_lenght_,0,0,cv2.BORDER_CONSTANT,value=border_color)
	print cols.shape
	print len(cols)
	if len(cols) > maximum_size_:
		print "entrando"
		cols = cv2.resize(cols, (0,0), fx=0.5, fy=0.5)
	
	return cols


# Extends the number of images to be used in the collage by replicating them randomly
def replicate_images(image_list_, desired_size_):
	cuantas_ = len(image_list_)
	print cuantas_
	if desired_size_ < len(image_list_):
		return image_list_
	else:	
		mada = False
		current = 0
		while (mada == False):
			print len(image_list_)
			image_list_.append(image_list_[random.randint(0,cuantas_-1)])
			if len(image_list_) == (desired_size_):
				mada = True
			current += 1



# Core method that builds the collage using all of the above functions
# **** Note: this method doesn't take all the parameters here but rather uses global variables declared in the top of this file.
def execute_collage_builder(create_small_images_, image_ramdomize_, image_repeat_):
	
	if create_small_images_:	
		# Excecute this line to create squares with the images in the 'images_loc'
		make_squares(images_loc, images_square_loc, square_size)

	# Extracts the names of the images
	image_names = get_image_names(images_square_loc)
	cuantas = len(image_names)
	print "we have : " + str(len(image_names)) + " images"

	# Determines the number of rows and columns in the final squared collage
	# **** Note: the number of images is trimmed down to the next lower entire root in order to be able to accomodate the collage's dimensions
	final_size_1 = int(math.sqrt(len(image_names)))

	# Checks if there is enough images to build the collage with the desired dimensions
	if cuantas < collage_cols*collage_rows:

		if image_repeat_ == False:   #use each image only once
			raise Exception('ImageQuantityError: At least '+str(collage_rows)+' x ' + str(collage_cols)+' images needed to build the collage')
		else:
			#Replicate the images in the 'image_names' list to achieve the number of tiles necessary to build a collage sized 'collage_rows x collage_cols'
			# **** Note: this method adds to the list in the parameter. DOES NOT RETURN A NEW ONE.
			replicate_images(image_names, collage_rows * collage_cols)

			# Shuffles images
			if image_ramdomize_: random.shuffle(image_names)


	# Creates the final image array, leaving out the extra pictures to round down to the product of the width and height of the collage
	final_image_array = image_names[:collage_cols*collage_rows]

	# Reshapes the array of image names to match the shape of the final squared collage
	#matrix = np.reshape(final_image_array,(final_size_1, final_size_1))
	matrix = np.reshape(final_image_array,(collage_rows,collage_cols))

	# Creates the collage
	collage = make_collage(matrix, border_lenght, square_size, max_size)
	
	# Generates a name to save the collage
	guardo_name = merged_images_loc + 'Collage '+ str(collage_rows) + 'x' + str(collage_cols) + ' - ' + str(datetime.datetime.today().microsecond) + formato
	
	# Saves the collage
	cv2.imwrite(guardo_name, collage)


# - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - Experimentation area - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - 


# Generates and saves the collage
execute_collage_builder(create_small_images, image_ramdomize, image_repeat)

#bla = np.zeros((100, 100, 3))
#bla2 = cv2.imread(images_square_loc  + "img_squared_32.jpg")
#bla[:,:] = [0, 0, 10]
#
##print bla
#
#cv2.imshow("Collage", bla)
#cv2.waitKey(0)
#cv2.destroyAllWindows()



