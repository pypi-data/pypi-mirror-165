from typing import List

import attr

from .base import Element, __compiler__, render

__t__ = __compiler__.compile(
    """terraform {
    {{#each elements}}
        {{{render this}}}
    {{/each}}
}
"""
)


@attr.define
class AstTerraform(Element):
    elements: List[Element] = attr.field(factory=list)

    def render(self) -> str:
        return __t__(self, helpers={"render": render})
