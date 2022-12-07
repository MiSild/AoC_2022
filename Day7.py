from common_aoc import read_file_n
from typing import List, Dict


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name: str, parent: "Directory" = None):
        self.name = name
        self.parent = parent
        self.contents: List["File", "Directory"] = []
        self.size = None

    def calculate_total_size(self):
        self.size = 0
        for content in self.contents:
            if isinstance(content, File):
                self.size += content.size
            elif isinstance(content, Directory):
                self.size += content.get_total_size()

    def get_total_size(self):
        if self.size is None:
            self.calculate_total_size()
        return self.size

    def get_full_path(self):
        if self.parent is not None:
            return f"{self.parent.get_full_path()}/{self.name}"
        else:
            return self.name

    def find_directory(self, name: str) -> "Directory":
        for object in self.contents:
            if object.name == name and isinstance(object, Directory):
                return object


def handle_cd(cd_command, cur_dir):
    if cd_command[2] == '..':
        return cur_dir.parent
    else:
        return cur_dir.find_directory(cd_command[2])


def handle_ls(ls_command, cur_dir, dirs):
    for object in ls_command:
        if object[0] == 'dir':
            new_dir = Directory(object[1], cur_dir)
            cur_dir.contents.append(new_dir)
            dirs.append(new_dir)
        else:
            cur_dir.contents.append(File(object[1], int(object[0])))


def handle_command(full_command, cur_dir, dirs):
    if full_command[0][1] == 'cd':
        return handle_cd(full_command[0], cur_dir)
    else:
        handle_ls(full_command[1:], cur_dir, dirs)
        return cur_dir


commands = [x[0].split(" ") for x in read_file_n(7)]
commands = commands[1:]

root_directory = Directory('/')
directories: List[Directory] = [root_directory]
current_directory = root_directory
full_command = []
for command in commands:
    if command[0] == '$':
        if full_command != []:
            current_directory = handle_command(full_command, current_directory, directories)
        full_command = [command]
    else:
        full_command.append(command)
handle_command(full_command, current_directory, directories)

dir_sum = 0
for directory in directories:
    dir_size = directory.get_total_size()
    if dir_size <= 100000:
        dir_sum += dir_size

# Part 2
total_space = 70000000
required_unused_space = 30000000
deletion_cutoff = required_unused_space - total_space + root_directory.get_total_size()
smallest_directory_to_delete = root_directory
for directory in directories:
    if deletion_cutoff < directory.get_total_size() < smallest_directory_to_delete.get_total_size():
        smallest_directory_to_delete = directory

print(smallest_directory_to_delete.get_total_size())


