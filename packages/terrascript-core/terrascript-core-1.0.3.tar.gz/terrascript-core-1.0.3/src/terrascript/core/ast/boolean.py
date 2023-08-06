import attr

from .base import Element, __compiler__

__t__ = __compiler__.compile("{{#if value}}true{{else}}false{{/if}}")


@attr.define
class AstBoolean(Element):
    value: bool

    def render(self) -> str:
        return __t__(self)
