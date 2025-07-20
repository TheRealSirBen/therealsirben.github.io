import os
import sys


def list_files(startpath, ignore_dirs=None, ignore_files=None):
    """
    Generate a tree-like representation of project structure

    Args:
        startpath (str): Root directory to start listing
        ignore_dirs (list): Directories to ignore
        ignore_files (list): File patterns to ignore
    """
    if ignore_dirs is None:
        ignore_dirs = [
            '.git', '.github', '.venv', 'venv', 'env', '.idea',
            '__pycache__', '.pytest_cache', 'node_modules'
        ]

    if ignore_files is None:
        ignore_files = [
            '*.pyc', '*.log', '.DS_Store', 'Thumbs.db',
            '*.swp', '*.swo', '__dev_utils__.py'
        ]

    def should_ignore(name, is_dir):
        """Check if a file or directory should be ignored"""
        if is_dir and name in ignore_dirs:
            return True

        if not is_dir:
            for pattern in ignore_files:
                if name.endswith(pattern.replace('*', '')):
                    return True

        return False

    print(os.path.basename(startpath) + '/')

    def tree(dir_path, prefix=''):
        """Recursively generate tree structure"""
        contents = sorted(os.listdir(dir_path))
        pointers = [('├──' if i < len(contents) - 1 else '└──') for i in range(len(contents))]

        for pointer, content in zip(pointers, contents):
            full_path = os.path.join(dir_path, content)
            is_dir = os.path.isdir(full_path)

            if should_ignore(content, is_dir):
                continue

            print(f"{prefix}{pointer} {content}{'/' if is_dir else ''}".strip())

            if is_dir:
                extension = '│   ' if pointer == '├──' else '    '
                tree(full_path, prefix + extension)

    tree(startpath)


# Use the script
if __name__ == '__main__':
    # Use current directory or provide a path
    project_root = sys.argv[1] if len(sys.argv) > 1 else '.'
    list_files(project_root)
