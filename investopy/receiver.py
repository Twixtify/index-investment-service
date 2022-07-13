from typing import Protocol


class Receiver(Protocol):
    """
    Know how to perform the operations associated with carrying out a
    request. Any class may serve as a Receiver.
    """

    def action(self):
        pass
