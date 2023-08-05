
class TimeoutOccurred(Exception):

    def __int__(self, max_second_allowed, new_qualname):
        super(f"Function ran out out time: {max_second_allowed} second(s)")
        self.max_second_allowed = max_second_allowed
        self.new_qualname = new_qualname


class MinimalDurationNotRespected(Exception):

    def __int__(self, min_second_allowed):
        super(f"Function returned too fast: {min_second_allowed} second(s) are required")
        self.min_second_allowed = min_second_allowed
