import threading, itertools, sys

# Spinner function to indicate loading
def spinner(spinner_stop, message, interval=0.1):
    chars = itertools.cycle(["◜","◠","◝","◞","◡","◟"])
    while not spinner_stop.is_set():
        c = next(chars)
        sys.stdout.write(f'\r{message}{c}')
        sys.stdout.flush()
        if spinner_stop.wait(interval):
            break

    sys.stdout.write('\r' + ' ' * (len(message) + 2) + '\r')
    sys.stdout.flush()
...

# Start spinner in a separate thread
def start_spinner(message='⏳ Loading... '):
    spinner_stop = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(spinner_stop, message))
    spinner_thread.daemon = True
    spinner_thread.start()
    return (spinner_stop, spinner_thread)
...

# Stop the spinner
def stop_spinner(spinner_stop, spinner_thread):
    spinner_stop.set()
    spinner_thread.join()
    sys.stdout.flush()
...

def spinner_running(spinner_thread):
    return spinner_thread.is_alive()
...