from pathlib import Path
import random
import string


def generate_test_file(filename, num_words=1000):
	base_dir = Path(__file__).parent.parent
	folder = base_dir / "data" / "dataset_small"

	folder.mkdir(parents=True, exist_ok=True)

	filepath = folder / f"{filename}.txt"

	if filepath.is_file():
		print("plik testowy: już istnieje")
		return filepath

	print("plik testowy: generuję")

	words = [
		'python', 'programming', 'distributed', 'system',
		'data', 'processing', 'parallel', 'computing'
	]

	with open(filepath, 'w') as f:
		for _ in range(num_words):
			f.write(random.choice(words) + ' ')

	print("plik testowy: wygenerowano pomyślnie")

	return filepath

def count_words(words):
	counts = {}

	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1

	return counts


def process_file(filepath):  # MAP
	try:
		with open(filepath, "r", encoding="utf-8") as f:
			text = f.read()

			# Małe litery
			text = text.lower()

			# Usuniecie interpunkcji
			text = text.translate(str.maketrans("", "", string.punctuation))

			# Tokenizacja
			words = text.split()

			# Usuwanie liczb
			# Usuwa tokeny będące tylko liczbami, pozostawia ciągi alfanumeryczne
			words = [w for w in words if not w.isdigit()]

			# Zliczanie słów
			counts = count_words(words)

			return counts

	except Exception as e:
		print("błąd pliku: ", filepath, e)
		return {}


def merge_results(results):  # REDUCE
	_final = {}

	for result in results:
		for key, value in result.items():
			_final[key] = _final.get(key, 0) + value

	return _final


def top_k_words(data, k=20):
	return dict(
		sorted(data.items(), key=lambda x: x[1], reverse=True)[:k]
	)
