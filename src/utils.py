import numpy as np

def minimum_int(num, min_num=1):
	num = int(num)
	if num < min_num:
		return min_num
	else:
		return num


def nearest_nonzero_idx(a,x,y):
	""""From https://stackoverflow.com/questions/43306291/find-the-nearest-nonzero-element-and-corresponding-index-in-a-2d-numpy-array"""
	idx = np.argwhere(a)

	# If (x,y) itself is also non-zero, we want to avoid those, so delete that
	# But, if we are sure that (x,y) won't be non-zero, skip the next step
	idx = idx[~(idx == [x,y]).all(1)]

	if idx.size == 0:
		return None
	else:
		return idx[((idx - [x,y])**2).sum(1).argmin()]


def nonzero_idx(a,x,y):
	""""From https://stackoverflow.com/questions/43306291/find-the-nearest-nonzero-element-and-corresponding-index-in-a-2d-numpy-array"""
	idx = np.argwhere(a)

	# If (x,y) itself is also non-zero, we want to avoid those, so delete that
	# But, if we are sure that (x,y) won't be non-zero, skip the next step
	idx = idx[~(idx == [x,y]).all(1)]

	if idx.size == 0:
		return None
	else:
		return idx


def direction_from_difference(difference):
	largest_idx = difference.argmax()
	sign_of_largest = np.sign(difference[largest_idx])

	if largest_idx == 0:
		if sign_of_largest == 1:
			return 0 # right
		else:
			return 2 # left
	else:
		if sign_of_largest == 1:
			return 1 # up
		else:
			return 3 # down
