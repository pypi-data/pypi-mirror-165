from typing import List

import attr

from .base import Element, __compiler__, render

__t__ = __compiler__.compile(
    """resource "{{{type}}}" "{{{name}}}" {
    {{#each elements}}
        {{{render this}}}
    {{/each}}
}
"""
)


@attr.define
class AstResource(Element):
    name: str
    type: str
    elements: List[Element] = attr.field(factory=list)

    def render(self) -> str:
        return __t__(self, helpers={"render": render})
