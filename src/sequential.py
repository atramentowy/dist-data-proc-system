import string
from pathlib import Path
import utils


def count_words(words):
	counts = {}

	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1

	return counts


def process_file(filepath): # MAP
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


def run_sequential():
	# Generowanie plików testowych
	utils.generate_test_file("data1", 1000)
	utils.generate_test_file("data2", 1000)

	# Ścieżki
	base_dir = Path(__file__).parent.parent  # wyjscie z src
	data_dir = base_dir / "dane"

	# Wczytywanie plików
	files = list(data_dir.glob("*.txt"))

	# Podział pracy
	if not files:
		print("błąd pliku: brak plików w folderze")

	word_counts = {}
	for file in files:
		try:
			# Worker
			counts = process_file(file)

			# REDUCE
			for word, count in counts.items():
				if word in word_counts:
					word_counts[word] += count
				else:
					word_counts[word] = count

			# Wybranie top 20
			word_counts = dict(
				sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
			)

		except Exception as e:
			print("błąd pliku: ", e)

	return word_counts


# Uruchom
result, execution_time = utils.measure_performance(run_sequential)

print(execution_time, result)
