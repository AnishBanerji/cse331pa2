import numpy as np
import math
import time
def gen_matrix(n: int) -> np.array:
    #
	# Step 2: Generate a 2D Array with NxN elements, following the formula on the write-up
	#         
	#     Inputs:
	#          - N:	Size of the array
	#          
	#     Returns:
	#     		A 2D array of doubles, with NxN values that follow the 2D sine wave pattern   
    #
	# TODO: put your CODE here ... return the correct data format 
    a=np.zeros((n,n))
    for row in range(0,n):
        for col in range(0,n):
            a[row,col]=np.round((math.sin(4*math.pi*row/n)*math.sin(4*math.pi*col/n)),3)
    return a



def findnaive(values: np.array, m: int, min_avg: float):
    n = int(values.shape[0])
    patches = []
    for row_start in range(n - m + 1):
        for col_start in range(n - m + 1):
            patch_sum = 0
            for i in range(m):
                for j in range(m):
                    patch_sum += values[row_start + i, col_start + j]
            patch_avg = patch_sum / (m * m)
            if patch_avg >= min_avg:
                patches.append([row_start, row_start + m - 1, col_start, col_start + m - 1])
    return patches


def findbetter(values: np.array, m: int, min_avg: float):
    n = values.shape[0]
    patches = []

    # Step 1: Compute the prefix sum matrix
    prefix_sum = np.zeros((n, n))
    prefix_sum[0, 0] = values[0, 0]

    # Fill the first row
    for j in range(1, n):
        prefix_sum[0, j] = values[0, j] + prefix_sum[0, j - 1]

    # Fill the first column
    for i in range(1, n):
        prefix_sum[i, 0] = values[i, 0] + prefix_sum[i - 1, 0]

    # Fill the rest of the prefix sum matrix
    for i in range(1, n):
        for j in range(1, n):
            prefix_sum[i, j] = values[i, j] + prefix_sum[i - 1, j] + prefix_sum[i, j - 1] - prefix_sum[i - 1, j - 1]

    # Step 2: Find all MxM patches with average >= min_avg
    for row_start in range(n - m + 1):
        for col_start in range(n - m + 1):
            row_end = row_start + m - 1
            col_end = col_start + m - 1

            total = prefix_sum[row_end, col_end]
            if row_start > 0:
                total -= prefix_sum[row_start - 1, col_end]
            if col_start > 0:
                total -= prefix_sum[row_end, col_start - 1]
            if row_start > 0 and col_start > 0:
                total += prefix_sum[row_start - 1, col_start - 1]

            patch_avg = total / (m * m)
            if patch_avg >= min_avg:
                patches.append([row_start, row_end, col_start, col_end])

    return patches
matrix = gen_matrix(1024)
print("Naive")
print("TIme: ", time.localtime())
patches = findnaive(matrix,256//4,0.25)
print(len(patches))
print("Time:", time.localtime())

print("Better")
print("Time", time.localtime())
patches = findbetter(matrix,1024//4,0.25)
print(len(patches))
print("Time:", time.localtime())
