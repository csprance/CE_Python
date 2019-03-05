
test_array = [
	[1, 1, 1, 1, 1, 1, 1, 1],
	[0, 0, 0, 1, 0, 0, 0, 1],
	[0, 0, 0, 1, 0, 0, 0, 1],
	[0, 0, 0, 1, 1, 1, 0, 1],
	[0, 0, 0, 0, 0, 1, 1, 1],
	[0, 0, 0, 1, 0, 1, 0, 0],
	[0, 1, 1, 1, 1, 1, 0, 0],
	[0, 1, 0, 0, 0, 0, 0, 0]
]
# loop through test array and create objects based on that value in the array
for row_idx, row in enumerate(test_array):
	for item_idx, item in enumerate(row):
		print item_idx
