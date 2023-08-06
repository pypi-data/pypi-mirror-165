from ..ast.provider import AstProvider
from .block import AbstractBlock


class Provider(AbstractBlock):
    @property
    def namespace_(self):
        return "main"

    @property
    def name_(self) -> str:
        return getattr(self.__class__, "_name")

    def generate(self) -> str:
        self.parse()

        ast = AstProvider(self.name_, self.ast_())
        return ast.render()
