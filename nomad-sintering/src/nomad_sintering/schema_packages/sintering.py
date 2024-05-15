#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo.basesections import Process
from nomad.datamodel.metainfo.basesections import ProcessStep
import numpy as np
from typing import (
    TYPE_CHECKING,
)
from nomad.metainfo import (
    Package,
    Quantity,
    SubSection,
    Section,
)
from nomad.datamodel.data import (
    EntryData,
    ArchiveSection,
)
if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.units import ureg

import pandas as pd 
import numpy as np

m_package = Package(name='Tutorial 13 sintering schema')


class TemperatureRamp(ProcessStep, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
        a_eln={
            "properties": {
                "order": [
                    "name",
                    "start_time",
                    "initial_temperature",
                    "final_temperature",
                    "duration",
                    "comment"
                ]
            }
        },)
    initial_temperature = Quantity(
        type=np.float64,
        description='initial temperature set for ramp',
        a_eln={
            "component": "NumberEditQuantity",
            "defaultDisplayUnit": "celsius"
        },
        unit="celsius",
    )
    final_temperature = Quantity(
        type=np.float64,
        description='final temperature set for ramp',
        a_eln={
            "component": "NumberEditQuantity",
            "defaultDisplayUnit": "celsius"
        },
        unit="celsius",
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        '''
        The normalizer for the `TemperatureRamp` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        '''
        super().normalize(archive, logger)


class Sintering(Process, EntryData, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section()
    steps = SubSection(
        section_def=TemperatureRamp,
        repeats=True,
    )

    data_file = Quantity(
        type=str,
        description='The recipe file for the sintering process.',
        a_eln={
            "component": "FileEditQuantity",
        },
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        '''
        The normalizer for the `Sintering` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        '''
        super().normalize(archive, logger)

        if self.data_file:
            with archive.m_context.raw_file(self.data_file) as file:
                df = pd.read_csv(file)

        steps = []

        for i, row in df.iterrows():
            step = TemperatureRamp()
            step.name = row['step name']
            step.duration = ureg.Quantity(float(row['duration [min]']), 'minutes')
            step.initial_temperature = ureg.Quantity(row['initial temperature [C]'], 'celsius')
            step.final_temperature = ureg.Quantity(row['final temperature [C]'], 'celsius')
            steps.append(step)

        self.steps = steps

m_package.__init_metainfo__()
