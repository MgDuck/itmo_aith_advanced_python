import sys

def tail_lines(lines, n):
    """Возвращает последние n строк из списка lines."""
    return lines[-n:] if len(lines) >= n else lines

def main():
    args = sys.argv[1:]
    if not args:
        input_lines = sys.stdin.readlines()
        sys.stdout.write(''.join(tail_lines(input_lines, 17)))
    else:
        multiple_files = len(args) > 1
        for idx, file_name in enumerate(args):
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    file_lines = f.readlines()
            except Exception as e:
                sys.stderr.write(f"tail: cannot open '{file_name}' for reading: {e}\n")
                continue
            if multiple_files:
                if idx > 0:
                    sys.stdout.write("\n")
                sys.stdout.write(f"==> {file_name} <==\n")
            sys.stdout.write(''.join(tail_lines(file_lines, 10)))

if __name__ == "__main__":
    main()