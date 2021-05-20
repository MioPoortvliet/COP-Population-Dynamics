import numpy as np
from numba import njit
import numba

nn_array = np.concatenate([np.eye(2, dtype=int), -np.eye(2, dtype=int)])

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

#@njit
def nonzero_idx(a: np.array, x: int, y: int) -> np.array:
	""""From https://stackoverflow.com/questions/43306291/find-the-nearest-nonzero-element-and-corresponding-index-in-a-2d-numpy-array"""
	idx = np.argwhere(a)

	# If (x,y) itself is also non-zero, we want to avoid those, so delete that
	# But, if we are sure that (x,y) won't be non-zero, skip the next step
	idx = idx[~(idx == [x,y]).all(1)]
	#idx_ = idx[~(idx == np.array([x,y]))]

	return idx

@njit
def direction_from_difference(difference):
	largest_idx = np.abs(difference).argmax()
	sign_of_largest = np.sign(difference[largest_idx])

	if largest_idx == 0:
		if sign_of_largest == 1:
			return 1 # right
		else:
			return 3 # left
	else:
		if sign_of_largest == 1:
			return 0 # up
		else:
			return 2 # down

@njit
def process_statistics(to_write, to_read, N):
	for m in range(9):
		for i in range(N):
			to_read_sum = np.sum(to_read[to_read[::, -1] == i][::, m])
			if to_read_sum == 0:
				pass
			else:
				# print(animal_stats[animal_stats[::, -1] == i][::, m])
				to_write[i, m, 0] = to_read_sum / np.count_nonzero(to_read[to_read[::, -1] == i][::, m])
				to_write[i, m, 1] = np.std(to_read[to_read[::, -1] == i][::, m])
	# print(self.animal_stats[cycle, i, ::, ::])