import arrow


class MoveActivity:
    fields = ['move_id', 'duration', 'distance', 'calories', 'description', 'time_i_s_o_8601']

    def __init__(self, activity_dict: dict) -> None:
        for key in self.fields:
            upper_case_key = key.title().replace("_", "")
            setattr(self, key, activity_dict.get(upper_case_key))

    def __str__(self) -> str:
        return f'Id: {self.id} (Dist: {self.distance}m, Duration: {self.duration}s) [{self.time}]'

    @property
    def id(self) -> str:
        return self.move_id

    @property
    def time(self) -> arrow.arrow.Arrow:
        return arrow.get(self.time_i_s_o_8601)
