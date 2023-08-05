import threading


class MultiThread:
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments
        self.threads = [threading.Thread(target=self.function, args=(argument,)) for argument in arguments]

    def run(self):
        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()
