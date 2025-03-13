import sys

def main():
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            sys.stderr.write(f"Ошибка: файл '{sys.argv[1]}' не найден.\n")
            sys.exit(1)
    else:
        lines = sys.stdin.readlines()
    
    for idx, line in enumerate(lines, start=1):
        sys.stdout.write(f"{idx:>6}\t{line}")

if __name__ == "__main__":
    main()
