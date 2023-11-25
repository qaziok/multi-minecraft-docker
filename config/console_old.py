import docker
import threading
import multiprocessing
import sys
import readline

def attach(container):
    print(container.logs(tail=10).decode(), end='')
    logs = container.attach(stream=True)
    for log in logs:
        try:
            message = log.decode().strip()
        except:
            message = log.strip()
        print(f'\r{message}')
        print('\r', end='')

def commands(container):
    while True:
        command = input()
        if command.lower() == 'exit':
            break

        mc_command = f"mc-send-to-console {command}"
        container.exec_run(mc_command, detach=True)


readline.parse_and_bind('set editing-mode vi')

if __name__ == '__main__':
    client = docker.from_env()

    try:
        container_id = sys.argv[1]
    except IndexError:
        container_id = None

    try:
        if container_id is None:
            containers = [c for c in client.containers.list() if c.name.endswith('mc-1')]
            
            print('Choose container')
            for i, c in enumerate(containers):
                print(f"{i+1}. {c.name}")

            container = None
            while container is None:
                try:
                    container = containers[int(input('Choose: '))-1]
                except IndexError:
                    print('Wrong number! Try again.')
                except ValueError:
                    print("It's not a number! Try again.")
        else:
            container = client.containers.get(container_id)
    except docker.errors.NotFound:
        print(f"Container '{container_id}' not found.")
        exit(1)



    attacher = multiprocessing.Process(target=attach, args=(container,))
    attacher.start()

    commander = threading.Thread(target=commands, args=(container,))
    commander.start()

    commander.join()
    attacher.terminate()
