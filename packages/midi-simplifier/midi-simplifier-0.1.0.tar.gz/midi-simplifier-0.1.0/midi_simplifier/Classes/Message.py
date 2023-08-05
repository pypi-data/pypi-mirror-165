from mido import tempo2bpm
from typing import Union, Tuple
from ..utils import MidoMessage, MidoMetaMessage


class Message:
    def __init__(self, msg: Union[MidoMessage, MidoMetaMessage]) -> None:
        self.__raw = msg
        self.type = type(msg)
        self.command = self.__get_command()
        # self.params = {kv for kv in str(msg).split(", ")[1:]}
        self.params = self.__get_params()

    def __sepearte(self, kv: str) -> Tuple:
        key, value = kv.split("=")
        if key == "time":
            value = value[:-1]

        try:
            return key, int(value)
        except:
            return key, value

    def __get_command(self) -> str:
        try:
            return str(self.__raw).split("'")[1]
        except:
            result = str(self.__raw).split()[0]
            if result == "note_on":
                pass
            return result

    def __get_params(self) -> list:
        if self.type == MidoMetaMessage:
            result = {self.__sepearte(kv)[0]: self.__sepearte(kv)[
                1] for kv in str(self.__raw).split(", ")[1:]}
            if self.command == "set_tempo":
                result["tempo"] = format(tempo2bpm(result["tempo"]), ".3f")
            return result

        # if self.command in ["note_on", "note_off"]:
        #     channel, note, velocity, time = (self.__sepearte(
        #         kv)[1] for kv in str(self.__raw).split(" ")[1:])
        #     return Note(note, velocity, time)

        result = {self.__sepearte(kv)[0]: self.__sepearte(kv)[
            1] for kv in str(self.__raw).split(" ")[1:]}
        return result

    def __str__(self) -> str:
        return str({"command": self.command, "params": str(self.params)})
