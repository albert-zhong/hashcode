class Library:
    def __init__(self, books, signup, ship_rate):
        self.books = books  # set of book_ids
        self.signup = signup  # time to signup library
        self.ship_rate = ship_rate  # books/day shipping rate


class Network:
    def __init__(self, B, L, D, scores, libraries):
        self.B = B  # number of books
        self.L = L  # number of libraries
        self.D = D  # number of days
        self.scores = scores  # maps book_id to its score
        self.libraries = libraries  # maps lib_id to Library object


def load_input(input_file):
    with open(input_file, 'r') as reader:
        lines = [line.rstrip() for line in reader]

    B, L, D = [int(num) for num in lines[0].split(' ')]
    scores = {i: int(score) for i, score in enumerate(lines[1].split(' '))}

    libraries = {}

    lib_id = 0
    i = 2
    while i < len(lines):
        book_count, signup, ship_rate = [int(num) for num in lines[i].split(' ')]
        books = {int(num) for num in lines[i + 1].split(' ')}
        libraries[lib_id] = Library(books, signup, ship_rate)
        i += 2
        lib_id += 1

    return Network(B, L, D, scores, libraries)


def score_from_file(input_file, submission_file):
    return score(load_input(input_file), submission_file)


def score(network, submission_file):
    with open(submission_file, 'r') as reader:
        lines = [line.rstrip() for line in reader]

    libraries_to_scan = int(lines[0])
    instructions = []

    lib_id = 0
    i = 1
    while i < len(lines):
        lib_id, books_to_scan_count = [int(num) for num in lines[i].split(' ')]
        books_to_scan = [int(num) for num in lines[i + 1].split(' ')]
        instructions.append((lib_id, books_to_scan))
        i += 2
        lib_id += 1

    scanned = set()
    final_score = 0
    all_days_left = network.D

    for lib_id, books_to_scan in instructions:
        library = network.libraries[lib_id]
        all_days_left -= library.signup
        if all_days_left <= 0:
            break
        
        final_score += score_from_library(
            network,
            library,
            books_to_scan,
            all_days_left,
            scanned
        )
    
    return final_score

def score_from_library(network, library, books_to_scan, days_left, scanned):
    score = 0
    i = 0

    for _ in range(days_left):
        for j in range(i, i + library.ship_rate):
            if j >= len(books_to_scan):
                return score
            book_id = books_to_scan[j]
            if book_id not in scanned:
                score += network.scores[book_id]
                scanned.add(book_id)
        i += library.ship_rate

    return score
