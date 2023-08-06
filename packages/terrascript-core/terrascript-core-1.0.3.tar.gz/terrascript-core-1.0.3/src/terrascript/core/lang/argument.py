from typing import Optional

import attr as attrs


@attrs.define
class Argument:
    key: str
    alias: Optional[str] = attrs.ib(default=None, kw_only=True)

    @property
    def name(self):
        return self.alias if self.alias else self.key
