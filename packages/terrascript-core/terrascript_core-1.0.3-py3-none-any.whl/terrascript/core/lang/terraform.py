from ..ast.terraform import AstTerraform
from .block import AbstractBlock
from .decorators import schema


@schema
class Terraform(AbstractBlock):
    @property
    def namespace_(self):
        return "main"

    def generate(self) -> str:
        self.parse()

        ast = AstTerraform(self.ast_())
        return ast.render()
