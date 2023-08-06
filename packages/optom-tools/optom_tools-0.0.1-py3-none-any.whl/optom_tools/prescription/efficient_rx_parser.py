# Efficient Rx -> Real Rx
# "0\n4" -> R plano
#           L +1.00 DS
# "4#" -> R +1.00 DS
#         L +1.00 DS
# "4.-4#110\nx90" -> R +1.00/-1.00x110
#                    L plano/-1.00x90
# "12#.-8#x180#.12# -> R +3.00/-2.00x180  Add: +3.00
#                      L +3.00/-2.00x180  Add: +3.00
# "27.-5x35.6\n30.-11x85.8" -> R +6.75/-1.25x35 Add: +1.50
#                              L +7.50/-2.75x85 Add: +2.00
# "4.8i12u\n30.12.-3x70.8i.8d" -> R +1.00 DS 2 In 3 Up
#                                 L +3.00/-0.75x70 2 In 2 Down
# "0#.6#" -> R plano Add: +1.50
#            L plano Add: +1.50


from typing import Any

from decimal import Decimal

D = Decimal


class EfficientRxError(Exception):
    """Raise exceptions for efficient Rx."""

    def __init__(self, value: Any, message: str):
        """Construct exception."""
        self.value = value
        self.message = message
        super().__init__()


def convert_dioptre(num: int) -> Decimal:
    """Convert number into dioptre.

    Args:
        num (int): ?

    Returns:
        (Decimal): Dioptre rounted to nearest 0.25.
    """
    UNIT = 0.25
    return D(num * UNIT)


def check_carriage_returns(efficient_rx: str) -> tuple[str, str | None]:
    """Check right eye and left eye returned as tuple."""
    result = efficient_rx.split("\n")
    if len(result) > 2:
        raise EfficientRxError(
            value=result, message="Maximum carriage returns is 1"
        )
    if len(result) == 1:
        return result[0], None
    return result[0], result[1]


def period_check(eye_rx: str) -> str:
    result = eye_rx.split(".")


def parse_efficient_normal_rx(efficient_rx: str):
    """Parse."""
    # check carriage returns, can only have one carriage return (2)
    right, left = check_carriage_returns(efficient_rx)
