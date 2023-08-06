from ..ast.data import AstData
from .block import ConfigurationBlock


class Data(ConfigurationBlock):
    def generate(self) -> str:
        self.parse()

        ast = AstData(self.name_, self.type_, self.ast_())
        return ast.render()
