import pickle, os

def print_results():
	total_performance = [0] * 100
	puzzle_names = []

	for i in range(30):
		try:
			model_result = pickle.load(open(os.getcwd() + '/1/model_refined%i.pkl' % i, 'rb'))
		except IOError:
			print(i)
			continue

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

def export_sequences():
	to_write = open(os.getcwd() + '/sentrna_v1_sols.txt', 'w')

	model_result = pickle.load(open('1/model_refined%i.pkl' % 20, 'rb'))

	for puzzle in range(len(model_result)):
		to_write.write("" + model_result[puzzle][0] + '\t' + model_result[puzzle][1] + '\t' + model_result[puzzle][2] + '\n')

	to_write.close()
	

if __name__ == '__main__':
	print_results()

