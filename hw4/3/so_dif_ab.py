import multiprocessing
import threading
import time
import datetime
import codecs
import sys

def process_a(input_queue, ab_queue):
    while True:
        # Ожидание сообщения из главного процесса
        msg = input_queue.get()
        msg_lower = msg.lower()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Процесс A получил сообщение: '{msg}' и преобразовал его в: '{msg_lower}'")
        sys.stdout.flush()
        # Задержка 5 секунд
        time.sleep(5)
        ab_queue.put(msg_lower)

def process_b(ab_queue, output_queue):
    while True:
        # Получаем сообщение от процесса A
        msg = ab_queue.get()
        # Применяем ROT13
        msg_rot13 = codecs.encode(msg, 'rot_13')
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Процесс B обработал сообщение (ROT13): '{msg_rot13}'")
        sys.stdout.flush()
        output_queue.put(msg_rot13)

def output_listener(output_queue, log_filename):
    with open(log_filename, "a", encoding="utf-8") as log_file:
        while True:
            # Блокирующее получение сообщения из очереди
            msg = output_queue.get()
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_line = f"[{now}] Сообщение от процесса B: '{msg}'\n"
            print(log_line, end="")
            log_file.write(log_line)
            log_file.flush()

def main():
    input_queue = multiprocessing.Queue()
    ab_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    proc_a = multiprocessing.Process(target=process_a, args=(input_queue, ab_queue))
    proc_b = multiprocessing.Process(target=process_b, args=(ab_queue, output_queue))
    proc_a.start()
    proc_b.start()

    log_filename = "interaction_log.txt"

    # Запускаем поток для прослушивания сообщений из output_queue
    listener_thread = threading.Thread(target=output_listener, args=(output_queue, log_filename), daemon=True)
    listener_thread.start()

    # Открываем файл для записи
    with open(log_filename, "a", encoding="utf-8") as log_file:
        try:
            while True:
                # Чтение ввода пользователя из stdin
                user_input = input("Введите сообщение для отправки в процесс A: ")
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_line = f"[{now}] Пользователь ввёл сообщение: '{user_input}'\n"
                log_file.write(log_line)
                log_file.flush()
                # Передача сообщения в процесс A через очередь
                input_queue.put(user_input)
        except KeyboardInterrupt:
            print("\nЗавершение работы программы...")
    
    proc_a.terminate()
    proc_b.terminate()

if __name__ == '__main__':
    main()
