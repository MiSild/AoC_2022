def read_file(path: str = "input.txt"):
    with open(path, 'r') as f:
        lines = f.readlines()
        lines = [line.rstrip("\n").split(",") for line in lines]

        if len(lines) == 1:
            return lines[0]
        else:
            return lines


def read_file_n(n: int):
    path = f"inputs/{n}"
    return read_file(path)