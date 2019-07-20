from enum import Enum

class LogType(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3

def Log(msg_type: LogType, message: str):
    if msg_type == LogType.INFO:
        print(f"** Information: {message} **")
    elif msg_type == LogType.WARNING:
        print(f"!! Warning: {message} !!")
    elif  msg_type == LogType.ERROR:
        print(f"## ERROR: {message}##")