from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class MySchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_sintering.schema_packages.mypackage import m_package
 
        return m_package


mypackage = MySchemaPackageEntryPoint(
    name='MyPackage',
    description='Schema package defined using the new plugin mechanism.',
)

class SinteringEntryPoint(SchemaPackageEntryPoint):

    def load(self):
        from nomad_sintering.schema_packages.sintering import m_package
 
        return m_package


sintering = SinteringEntryPoint(
    name='Sintering',
    description='Schema package defined using the new plugin mechanism.',
)
