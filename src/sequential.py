import time
from pathlib import Path
import utils


def run_sequential(data_dir=None, verbose=False):
	total_start = time.perf_counter()

	# Ścieżki
	base_dir = Path(__file__).parent.parent  # wyjscie z src
	if data_dir is None:
		# data_path = base_dir / "data"
		print("data dir error")
		return
	else:
		data_path = (base_dir / data_dir).resolve()

	# Wczytywanie plików
	files = list(data_path.glob("*.txt"))

	# Podział pracy
	if not files:
		print("[sequential] błąd danych: brak plików w folderze")

	map_start = time.perf_counter()

	results = []
	for file in files:
		# Worker
		result = utils.process_file(file)
		results.append(result)

	map_end = time.perf_counter()

	reduce_start = time.perf_counter()
	# REDUCE
	word_count = utils.merge_results(results)
	word_count = utils.top_k_words(word_count)
	#
	reduce_end = time.perf_counter()

	total_end = time.perf_counter()

	# METRYKI
	map_time = map_end - map_start
	reduce_time = reduce_end - reduce_start
	total_time = total_end - total_start

	# WYNIKI
	if verbose:
		print("TOP 20:", word_count)
		print(f"sequential map time:     {map_time:.6f}s")
		print(f"sequential reduce time:  {reduce_time:.6f}s")
		print(f"sequential total time:   {total_time:.6f}s")

	return word_count, total_time, map_time, reduce_time


# Uruchom
# run_sequential()
