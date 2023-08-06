from dbt.adapters.opengauss.connections import openGaussConnectionManager # noqa
from dbt.adapters.opengauss.connections import openGaussCredentials
from dbt.adapters.opengauss.relation import opengaussColumn  # noqa
from dbt.adapters.opengauss.relation import opengaussRelation  # noqa: F401
from dbt.adapters.opengauss.impl import openGaussAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import opengauss


Plugin = AdapterPlugin(
    adapter=openGaussAdapter,
    credentials=openGaussCredentials,
    include_path=opengauss.PACKAGE_PATH
    )
