import pickle

if __name__ == '__main__':
	best_perf = 0
	avg_perf = 0

	for i in range(20):
		model_result = pickle.load(open('model_refined%i.pkl' % i, 'rb'))

		local_perf = 0

		for puzzle in range(len(model_result)):
			if model_result[puzzle][3] == 1.0:
				local_perf += 1
		
		avg_perf += local_perf

		if local_perf > best_perf:
			best_perf = local_perf

	avg_perf = avg_perf / 20.0

	print("Best model:", best_perf)
	print("Average model:", avg_perf)