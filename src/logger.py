# Danganronpa Online Area List Maker by Yuzuru #
# Please contact the following if you encounter any bugs
# Discord: Yuzuru#2897, Gmail: <yuzuru.aceattorneyonline@gmail.com>


from src.constant import Constant
from dataclasses import dataclass, field


@dataclass()
class Logging:
    time: str = field(default="GONE FISHING")
    message: str = field(default="I only say morning because if it's a good morning, I'd be fishing.")

    def prepare_message(self) -> str:
        time = Constant.current_time()
        self.time = time

        message = f"[{self.time}]: {self.message} \n"
        return message
