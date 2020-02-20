from library import Library, load_input, score, score_from_file


def generate(input_file):
    def calculate_alpha(network, lib_id, library, days_left, scanned):
        alpha = 0
        scores = network.scores
        ship_rate = library.ship_rate

        books = sorted(
            library.books,
            key=lambda pk: scores[pk] * (-1 if pk in scanned else 1),
            reverse=True
        )

        i = 0
        for day in range(days_left):
            for j in range(i, i + ship_rate):
                if j >= len(books):
                    return (lib_id, books, alpha / library.signup)
                book_id = books[j]
                if book_id in scanned:
                    return (lib_id, books, alpha / library.signup)
                alpha += scores[book_id]
                scanned.add(book_id)
            i += ship_rate

        return (lib_id, books, alpha / library.signup)

    network = load_input(input_file)
    scanned = set()

    instructions = []
    days_left = network.D

    while days_left > 0 and network.libraries:
        best_lib_id, best_books, best_alpha = max(
            [
                calculate_alpha(network, lib_id, library, days_left, scanned)
                for lib_id, library in network.libraries.items()
            ]
        )
        days_left -= network.libraries[best_lib_id].signup
        instructions.append((best_lib_id, best_books))
        del network.libraries[best_lib_id]
    LIBRARY_COUNT = len(instructions)
    OUTPUT_FILENAME = input_file[:-4] + 'sub' + '.txt'

    with open(OUTPUT_FILENAME, 'w') as output:
        output.write(f"{str(LIBRARY_COUNT)}\n")
        for lib_id, books_to_scan in instructions:
            output.write(f"{str(lib_id)} {len(books_to_scan)}\n")
            output.write(' '.join(str(book_id) for book_id in books_to_scan))
            output.write('\n')
