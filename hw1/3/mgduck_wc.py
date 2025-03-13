import sys

def count_stats(content: str):
    lines = content.count('\n')
    words = len(content.split())
    bytes_count = len(content.encode('utf-8'))
    return lines, words, bytes_count

def process_file(filename: str):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        sys.stderr.write(f"wc: {filename}: {e}\n")
        return None
    return count_stats(content)

def main():
    args = sys.argv[1:]
    total_lines = total_words = total_bytes = 0
    results = []

    if not args:
        content = sys.stdin.read()
        lines, words, bytes_count = count_stats(content)
        print(f"{lines:1d} {words:2d} {bytes_count:1d}")
    else:
        for filename in args:
            stats = process_file(filename)
            if stats is None:
                continue
            lines, words, bytes_count = stats
            total_lines += lines
            total_words += words
            total_bytes += bytes_count
            results.append((lines, words, bytes_count, filename))
            print(f"{lines:1d} {words:2d} {bytes_count:1d} {filename}")
        if len(results) > 1:
            print(f"{total_lines:1d} {total_words:2d} {total_bytes:1d} итого")

if __name__ == "__main__":
    main()
