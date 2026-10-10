from typing import Annotated

from pydantic import StringConstraints

# Whitespace is stripped first, so an all-spaces string counts as blank and is rejected.
NonBlankText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
