from sequential import run_sequential
from coordinator import run_coordinator
# import utils


def benchmark():
	# Generowanie małego zestawu danych
	# utils.generate_test_file("data1", 1000)
	# utils.generate_test_file("data2", 1000)

	print("program started")

	datasets = [
		"data/small_dataset",
		"data/medium_dataset",
		"data/large_dataset"
	]

	verbose = False

	for dataset in datasets:
		results = {}

		avg_seq = {
			"seq_total": 0,
			"seq_map": 0,
			"seq_reduce": 0,
			"runs": 0,

		}

		avg_par = {
			avg_par_dict: {
				"par_total": 0,
				"par_map": 0,
				"par_reduce": 0,
				"runs": 0
			}
			for avg_par_dict in [1, 2, 4]
		}

		# 3 passes for average
		for run in range(0, 3):
			if verbose:
				print(f"====================")
				print(f"RUN NR: {run}")
				print(f"[Benchmark map-reduce] DATASET: {dataset}")

				print(f"[Sequential]")
				print(f"-------------------------------------")

			word_count, seq_total, seq_map, seq_reduce = run_sequential(data_dir=dataset)

			# save results
			avg_seq["seq_total"] += seq_total
			avg_seq["seq_map"] += seq_map
			avg_seq["seq_reduce"] += seq_reduce
			avg_seq["runs"] += 1

			if verbose:
				print(f"Sequential total:   {seq_total:.6f}s")
				print(f"Sequential map:     {seq_map:.6f}s")
				print(f"Sequential reduce:  {seq_reduce:.6f}s")
				print(f"-------------------------------------")

				print("[Parallel]")
				print(f"-------------------------------------")

			worker_counts = [1, 2, 4]
			for workers in worker_counts:
				word_count, par_total, par_map, par_reduce = run_coordinator(workers, data_dir=dataset)

				results = word_count

				avg_par[workers]["par_total"] += par_total
				avg_par[workers]["par_map"] += par_map
				avg_par[workers]["par_reduce"] += par_reduce
				avg_par[workers]["runs"] += 1

				if verbose:
					speedup_total = seq_total / par_total
					efficiency = speedup_total / workers
					speedup_map = seq_map / par_map
					speedup_reduce = seq_reduce / par_reduce

					print(f"{workers} workers")
					print(f"Parallel total:     {par_total:.4f}s (Speedup: {speedup_total:.2f}x)")
					print(f"Parallel map:       {par_map:.4f}s (Speedup: {speedup_map:.2f}x)")
					print(f"Parallel reduce:    {par_reduce:.4f}s (Speedup: {speedup_reduce:.2f}x)")
					print(f"Efficiency:         {efficiency * 100 :.2f}%")
					print(f"-------------------------------------")

		# average from 3 runs
		# sequential
		runs = avg_seq["runs"]
		for key, value in avg_seq.items():
			if key != "runs":
				avg_seq[key] /= runs

		# parallel
		for w in avg_par:
			runs = avg_par[w]["runs"]

			if runs > 0:
				for key in avg_par[w]:
					if key != "runs" or key != "efficiency":
						avg_par[w][key] /= runs

		# RESULTS
		print(f"\nDataset: {dataset}")
		print(f"Average results for 3 passes of sequential and parallel (with 1, 2 and 4 workers) MAP REDUCE algorithm.")

		print("\n=== AVERAGE RESULTS FOR SEQUENTIAL VERSION ===\n")
		# for key, value in avg_seq.items():
		# 	print(key, value)

		print(f"Total:   {avg_seq['seq_total']:.4f}s")
		print(f"Map:     {avg_seq['seq_map']:.4f}s")
		print(f"Reduce:  {avg_seq['seq_reduce']:.4f}s")

		print("\n=== AVERAGE RESULTS FOR PARALLEL VERSION ===")
		# for workers, stats in avg_par.items():
		# 	print(f"\nWorkers: {workers}")
		# 	for key, value in stats.items():
		# 		print(f"{key}: {value}")

		for workers, stats in avg_par.items():
			avg_speedup_total = avg_seq['seq_total'] / stats["par_total"]
			avg_speedup_map = avg_seq["seq_map"] / stats["par_map"]
			avg_speedup_reduce = avg_seq["seq_reduce"] / stats["par_reduce"]
			efficiency = avg_speedup_total / workers

			print(f"\n--- {workers} workers ---")
			print(f"Total:   {stats['par_total']:.4f}s  (Speedup: {avg_speedup_total:.2f}x)")
			print(f"Map:     {stats['par_map']:.4f}s  (Speedup: {avg_speedup_map:.2f}x)")
			print(f"Reduce:  {stats['par_reduce']:.4f}s  (Speedup: {avg_speedup_reduce:.2f}x)")
			print(f"Efficiency: {efficiency * 100:.2f}%")

		# DATASET RESULTS:
		print(f"\n=== Results: ===")
		for key, value in results.items():
			print(key, value)


if __name__ == "__main__":
	benchmark()
