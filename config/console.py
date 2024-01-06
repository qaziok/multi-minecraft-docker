#!/usr/bin/env python3

import re
import sys
import docker
import curses
import multiprocessing as mp


def que_message(que, message):
    if message != "":
        que.put(message)


def send_message(container, message):
    mc_command = f"mc-send-to-console {message}"
    container.exec_run(mc_command, detach=True)


def get_container(client):
    try:
        container_id = sys.argv[1]
        return client.containers.get(container_id)
    except docker.errors.NotFound:
        print(f"Container '{container_id}' not found.")
        return None
    except IndexError:
        print("Choose container")

    containers = [c for c in client.containers.list() if c.name.endswith("mc-1")]

    for i, c in enumerate(containers):
        print(f"{i+1}. {c.name}")

    while True:
        try:
            return containers[int(input("Choose: ")) - 1]
        except IndexError:
            print("Wrong number! Try again.")
        except ValueError:
            print("It's not a number! Try again.")


def logger(que, container):
    x = container.logs(tail=10).decode()
    for msg in x.split("\r\n"):
        que_message(que, msg)
    logs = container.attach(stream=True)
    for log in logs:
        try:
            message = log.decode().strip()
        except:
            message = log.strip()
        que_message(que, message)


def get_input(window):
    try:
        return window.get_wch()
    except curses.error:
        return None


def main(stdscr, que, container):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()

    log_win = stdscr.subwin(height - 3, width, 0, 0)
    log_win.scrollok(True)
    log_win.idlok(True)
    log_win.refresh()

    input_win = stdscr.subwin(3, width, height - 3, 0)
    input_win.addstr(1, 1, ">> ")
    input_win.border()
    input_win.refresh()
    input_win.nodelay(True)

    input_text = ""

    while True:
        while (key := get_input(input_win)) is None and que.empty():
            pass

        match key:
            case '\n': # Enter
                if input_text == "exit":
                    break
                send_message(container, input_text)
                input_text = ""
            case '\x7f': # Backspace
                input_text = input_text[:-1]
            case None: # No input
                pass
            case _: # Other
                input_text += key

        re_match = r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])'
        while re.search(re_match, input_text):
            input_text = re.sub(re_match, "", input_text)

        while not que.empty():
            msg = que.get()
            log_win.addstr(f" > {msg}\n")

        input_win.clear()
        input_win.addstr(1, 1, ">> " + input_text)
        input_win.border()
        input_win.refresh()

        log_win.refresh()


if __name__ == "__main__":
    client = docker.from_env()

    container = get_container(client)

    if container is None:
        exit(1)

    que = mp.Queue()
    prcs = mp.Process(target=logger, args=(que, container))
    prcs.start()
    try:
        curses.wrapper(main, que, container)
    except KeyboardInterrupt:
        pass
    finally:
        prcs.terminate()
        prcs.join()
