import pickle

if __name__ == '__main__':
	total_performance = [0] * 100
	puzzle_names = []

	for i in range(20):
		model_result = pickle.load(open('model_refined%i.pkl' % i, 'rb'))

		for puzzle in range(len(model_result)):
			if model_result[puzzle][3] == 1.0:
				total_performance[puzzle] += 1
			
			if i == 0:
				puzzle_names.append(model_result[puzzle][0])

	solved = 0

	for i in total_performance:
		if i >= 1.0:
			solved += 1
	
	for i, j in zip(puzzle_names, total_performance):
		print("%s: %i" % (i, j))
	
	print("\nSolved %i/100" % solved)

