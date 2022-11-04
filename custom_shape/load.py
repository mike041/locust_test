import math
from collections import namedtuple

from locust import LoadTestShape


class StagesShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 10, },
        {"duration": 100, "users": 50, "spawn_rate": 10},
        {"duration": 180, "users": 100, "spawn_rate": 10},
        {"duration": 220, "users": 30, "spawn_rate": 10},
        {"duration": 230, "users": 10, "spawn_rate": 10},
        {"duration": 240, "users": 1, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None


class LoadShape(LoadTestShape):
    max_users = 100
    spawn_rate = 10
    max_time = 30 * 60

    def tick(self):
        run_time = self.get_run_time()
        current_user_count = self.get_current_user_count()
        print('run_time', run_time)
        print('current_user_count', current_user_count)
        if run_time < self.max_time:
            if self.get_current_user_count() < self.max_users:
                tick_data = (self.max_users, self.spawn_rate)
                return tick_data
            return (self.max_users, self.max_users)
        return None


class DoubleWave(LoadTestShape):
    """
    A shape to imitate some specific user behaviour. In this example, midday
    and evening meal times. First peak of users appear at time_limit/3 and
    second peak appears at 2*time_limit/3
    Settings:
        min_users -- minimum users
        peak_one_users -- users in first peak
        peak_two_users -- users in second peak
        time_limit -- total length of test
    """

    min_users = 20
    peak_one_users = 60
    peak_two_users = 40
    time_limit = 600

    def tick(self):
        run_time = round(self.get_run_time())

        if run_time < self.time_limit:
            user_count = (
                    (self.peak_one_users - self.min_users)
                    * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 5) ** 2)
                    + (self.peak_two_users - self.min_users)
                    * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 10) ** 2)
                    + self.min_users
            )
            return (round(user_count), round(user_count))
        else:
            return None


class StepLoadShape(LoadTestShape):
    """
    A step load shape
    Keyword arguments:
        step_time -- Time between steps
        step_load -- User increase amount at each step
        spawn_rate -- Users to stop/start per second at every step
        time_limit -- Time limit in seconds
    """

    step_time = 30
    step_load = 10
    spawn_rate = 10
    time_limit = 600

    def tick(self):
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            return None

        current_step = math.floor(run_time / self.step_time) + 1
        return (current_step * self.step_load, self.spawn_rate)


Step = namedtuple("Step", ["users", "dwell"])


class StepLoadShape(LoadTestShape):
    """
    A step load shape that waits until the target user count has
    been reached before waiting on a per-step timer.
    The purpose here is to ensure that a target number of users is always reached,
    regardless of how slow the user spawn rate is. The dwell time is there to
    observe the steady state at that number of users.
    Keyword arguments:
        targets_with_times -- iterable of 2-tuples, with the desired user count first,
            and the dwell (hold) time with that user count second
    """

    targets_with_times = (Step(10, 10), Step(20, 15), Step(10, 10))

    def __init__(self, *args, **kwargs):
        self.step = 0
        self.time_active = False
        super().__init__(*args, **kwargs)

    def tick(self):
        if self.step >= len(self.targets_with_times):
            return None

        target = self.targets_with_times[self.step]
        users = self.get_current_user_count()

        if target.users == users:
            if not self.time_active:
                self.reset_time()
                self.time_active = True
            run_time = self.get_run_time()
            if run_time > target.dwell:
                self.step += 1
                self.time_active = False

        # Spawn rate is the second value here. It is not relevant because we are
        # rate-limited by the User init rate.  We set it arbitrarily high, which
        # means "spawn as fast as you can"
        return (target.users, 100)
