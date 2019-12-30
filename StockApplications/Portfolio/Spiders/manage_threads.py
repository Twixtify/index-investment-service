import threading


class ManageThreads:
    def __init__(self):
        self.threads = []

    def add_threads(self, threads):
        for thread in threads:
            self.add_thread(thread)

    def add_thread(self, thread):
        if isinstance(thread, threading.Thread):
            self.threads.append(thread)
        else:
            raise TypeError("Expected '%s', got '%s' " % (threading.Thread.__name__, type(thread).__name__))

    def start_threads(self):
        for thread in self.threads:
            thread.start()

    def join_threads(self):
        for thread in self.threads:
            thread.join()
