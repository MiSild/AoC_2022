def read_file(path: str = "input.txt", flag_raw=False):
    with open(path, 'r') as f:
        lines = f.readlines()
        if flag_raw:
            lines = [line.rstrip("\n") for line in lines]
        else:
            lines = [line.rstrip("\n").split(",") for line in lines]

        if len(lines) == 1:
            return lines[0]
        else:
            return lines


def read_file_n(n, folder: str = "inputs", flag_raw=False):
    path = f"{folder}/{n}"
    return read_file(path, flag_raw)

