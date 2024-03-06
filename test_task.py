from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_file(filepath):
    """
    Reads a file and returns a list of integers.
    In case of an error, logs the error and returns the empy list.
    """
    try:
        with open(filepath, 'r') as file:
            return [int(line.strip()) for line in file if line.strip()]
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
    except ValueError:
        logging.error(f"Invalid integer value encountered in the file: {filepath}")
    except Exception as e:
        logging.error(f"Unexpected error reading file {filepath}: {e}")
    return []


class FileAnalyzer:
    def __init__(self, path):
        if not path:
            raise ValueError(f"File path can't be blank")

        logging.info(f"FileAnalyzer created for {path}")
        self._path = path
        self._numbers = []
        self._max_val = None
        self._min_val = None
        self._median = None
        self._avg = None
        self._longest_increasing_sequence = None
        self._longest_decreasing_sequence = None
        self._sum_of_numbers = None
        self._count_of_numbers = None

    def analyze_file(self):
        """
        Analyzes data from a file specified in the variable `_path`.

        The method performs the following steps:
        1. Logs the start of the analysis.
        2. Reads numbers from the file into the `_numbers` instance variable.
        3. Checks if `_numbers` is empty and logs a warning if true.
        4. Calculates and stores the maximum and minimum values, the total sum, count, and the average of the numbers.
        5. Calls the private method `__find_median` to calculate and store the median value.
        6. Calls the private method `__longest_increasing_decreasing_sequences` to find and store the elements
        of the longest increasing and decreasing sequences.
        7. Clears the `_numbers` list to free memory.
        8. Logs the completion of the analysis and its duration.
        """
        logging.info("Starting analysis.")
        start_time = datetime.now()

        self._numbers = read_file(self._path)
        if not self._numbers:
            logging.warning("FileAnalyzer received empty list")
            return
        self._max_val = max(self._numbers)
        self._min_val = min(self._numbers)
        self._sum_of_numbers = sum(self._numbers)
        self._count_of_numbers = len(self._numbers)
        self._avg = round(self._sum_of_numbers / self._count_of_numbers, 1)
        self.__find_median()
        self.__longest_increasing_decreasing_sequences()
        self._numbers = None

        end_time = datetime.now()
        logging.info(f"Analysis completed in {end_time - start_time}.")

    def analysis_result(self):
        """
        Returns dict with metrics of the file: max, min, average, median value,
        length of longest increasing and decreasing sequences
        """
        return {
            'max': self._max_val,
            'min': self._min_val,
            'avg': self._avg,
            'median': self._median,
            'longest_increasing_sequence': self._longest_increasing_sequence,
            'longest_decreasing_sequence': self._longest_decreasing_sequence,
        }

    def __find_median(self):
        """
        Calculates the median of the numbers stored in the instance variable `_numbers`.
        The calculated median is stored in the `_median` instance variable.
        """
        sorted_numbers = sorted(self._numbers)
        if self._count_of_numbers % 2 != 0:
            median = sorted_numbers[self._count_of_numbers // 2]
        else:
            median = (sorted_numbers[self._count_of_numbers // 2 - 1] +
                      sorted_numbers[self._count_of_numbers // 2]) / 2
        self._median = round(median, 1)

    def __longest_increasing_decreasing_sequences(self):
        """
        Calculates and stores the elements of the longest increasing and decreasing subsequences
        within the `_numbers` instance variable.
        """
        longest_increasing_idx = (0, 0)
        longest_decreasing_idx = (0, 0)
        current_incr_start = 0
        current_decr_start = 0

        for i in range(1, len(self._numbers)):
            # Check for end of increasing sequence
            if self._numbers[i] <= self._numbers[i - 1]:
                current_len_incr = i - current_incr_start
                last_len_inc = longest_increasing_idx[1] - longest_increasing_idx[0]
                if current_len_incr > last_len_inc:
                    longest_increasing_idx = (current_incr_start, i)
                current_incr_start = i

            # Check for end of decreasing sequence
            if self._numbers[i] >= self._numbers[i - 1]:
                current_len_decr = i - current_decr_start
                last_len_decr = longest_decreasing_idx[1] - longest_decreasing_idx[0]
                if current_len_decr > last_len_decr:
                    longest_decreasing_idx = (current_decr_start, i)
                current_decr_start = i

        # Check last increasing sequence
        current_len_incr = self._count_of_numbers - current_incr_start
        last_len_inc = longest_increasing_idx[1] - longest_increasing_idx[0]
        if current_len_incr > last_len_inc:
            longest_increasing_idx = (current_incr_start, self._count_of_numbers)

        # Check last decreasing sequence
        current_len_decr = self._count_of_numbers - current_decr_start
        last_len_decr = longest_decreasing_idx[1] - longest_decreasing_idx[0]
        if current_len_decr > last_len_decr:
            longest_decreasing_idx = (current_decr_start, self._count_of_numbers)

        self._longest_decreasing_sequence = self._numbers[longest_decreasing_idx[0]:longest_decreasing_idx[1]]
        self._longest_increasing_sequence = self._numbers[longest_increasing_idx[0]:longest_increasing_idx[1]]

    @property
    def max_val(self):
        return self._max_val

    @property
    def min_val(self):
        return self._min_val

    @property
    def median(self):
        return self._median

    @property
    def avg(self):
        return self._avg

    @property
    def longest_increasing_sequence(self):
        return self._longest_increasing_sequence

    @property
    def longest_decreasing_sequence(self):
        return self._longest_decreasing_sequence


#  example of usage
# file = FileAnalyzer(path_to_file)
# file.analyze_file()
# print(file.analysis_result())
