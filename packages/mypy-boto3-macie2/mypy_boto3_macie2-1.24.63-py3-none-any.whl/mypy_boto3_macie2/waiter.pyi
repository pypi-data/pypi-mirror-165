"""
Type annotations for macie2 service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie2/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_macie2.client import Macie2Client
    from mypy_boto3_macie2.waiter import (
        FindingRevealedWaiter,
    )

    session = Session()
    client: Macie2Client = session.client("macie2")

    finding_revealed_waiter: FindingRevealedWaiter = client.get_waiter("finding_revealed")
    ```
"""
from botocore.waiter import Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("FindingRevealedWaiter",)

class FindingRevealedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Waiter.FindingRevealed)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie2/waiters/#findingrevealedwaiter)
    """

    def wait(self, *, findingId: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Waiter.FindingRevealed.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie2/waiters/#findingrevealedwaiter)
        """
