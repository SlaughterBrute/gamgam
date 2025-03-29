import random


def random_sequence(length):
    """
    Returns a X long random sequence of 0's and 1's
    """
    return [random.randint(0, 1) for _ in range(length)]

def generate_hitomezashi_pattern(row_sequence, col_sequence):
    first_col = [0]

    for i, x in enumerate(row_sequence):
        value = (first_col[i] + col_sequence[i]) % 2
        first_col.append(value)

    grid = []

    for y, y0 in enumerate(first_col):
        row = []
        row.append(y0)
        for x, x0 in enumerate(row_sequence):
            value = (row[x] + x0 + y) % 2
            row.append(value)
        grid.append(row)

    return grid

def generate_map(width:int=20, height:int=20):
    sequence_x = random_sequence(width)
    sequence_y = random_sequence(height)
    pattern = generate_hitomezashi_pattern(sequence_x, sequence_y)
    with open('map.gamefile', 'w') as f:
        f.write(''.join([str(num) for num in sequence_x]))
        f.write('\n')
        f.write(''.join([str(num) for num in sequence_y]))
        f.write('\n')
        for l in pattern:
            f.write(''.join([str(num) for num in l]))
            f.write('\n')

if __name__ == "__main__":
    generate_map()