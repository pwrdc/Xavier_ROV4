import time


class Stopwatch:
    """
        Class for time measurements.
    """

    def __init__(self):
        self.time_counted = 0
        self.last_start_time = 0
        self.is_running = False

    def start(self) -> None:
        """
        Starts time counting
        :return: None
        """
        self.last_start_time = time.time()
        self.is_running = True

    def stop(self) -> float:
        """
        Stops the timer and returns time
        :return: Time counted by stopwatch (in seconds)
        """
        if self.is_running:
            self.time_counted = self.time_counted + time.time() - self.last_start_time
            self.is_running = False

        return self.time_counted

    def time(self) -> float:
        """
        Returns time counted by stopwatch. Does not stops the counting it it is running
        :return: Time counted by stopwatch (in seconds)
        """
        time_counted = self.time_counted
        if self.is_running:
            time_counted += time.time() - self.last_start_time

        return time_counted

    def reset(self) -> None:
        """
        Resets counted time to 0
        :return: None
        """
        self.time_counted = 0
        self.last_start_time = 0
        self.is_running = False

    @staticmethod
    def measure_function(func, arguments=(), verbose=False) -> float:
        """
        :param func: function whose execution time will be measured
        :param arguments: arguments provided to measured function
        :param verbose: prints executuion time if set to true
        :return: function execution time, measured in seconds
        """
        time_start = time.time()
        func(*arguments)
        end_time = time.time()

        if verbose:
            print(f"Function execution time: {end_time - time_start} seconds")

        return end_time - time_start


if __name__ == "__main__":
    # Usage example:
    s = Stopwatch()

    s.start()
    time.sleep(2)
    t = s.stop()
    print(f"t = {t}")  # Expect t roughly equal to 2

    s.start()
    time.sleep(3)
    t = s.stop()
    print(f"t = {t}")  # Expect t roughly equal to 5

    s.reset()
    s.start()
    time.sleep(1)
    t = s.stop()
    print(f"t = {t}")  # Expect t roughly equal to 1

    t = Stopwatch.measure_function(time.sleep, (5,), True)  # Expect time roughly equal to 5
