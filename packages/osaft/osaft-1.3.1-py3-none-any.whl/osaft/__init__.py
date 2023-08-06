# Import logger
from osaft.core.logger import log

# Import API
from osaft.core.functions import pi
from osaft.core.backgroundfields import BackgroundField, WaveType
from osaft.core.fluids import InviscidFluid, ViscoelasticFluid, ViscousFluid
from osaft.core.solids import ElasticSolid, RigidSolid
from osaft.plotting.arf.arf_plots import ARFPlot
from osaft.plotting.scattering.fluid_plots import FluidScatteringPlot
from osaft.plotting.scattering.particle_plots import (
    ParticleScatteringPlot,
    ParticleWireframePlot,
)
# IMPORT API solutions
import osaft.solutions.gorkov1962 as gorkov1962
import osaft.solutions.king1934 as king1934
import osaft.solutions.yosioka1955 as yosioka1955
import osaft.solutions.doinikov1994rigid as doinikov1994rigid
import osaft.solutions.doinikov1994compressible as doinikov1994compressible
import osaft.solutions.settnes2012 as settnes2012
import osaft.solutions.hasegawa1969 as hasegawa1969
import osaft.solutions.doinikov2021viscous as doinikov2021viscous
import osaft.solutions.doinikov2021viscoelastic as doinikov2021viscoelastic

# Legacy names of modules
Gorkov1962 = gorkov1962
King1934 = king1934
Yosioka1955 = yosioka1955
Doinikov1994Rigid = doinikov1994rigid
Doinikov1994Compressible = doinikov1994compressible
Settnes2012 = settnes2012
Doinikov2021Viscous = doinikov2021viscous
Doinikov2021Viscoelastic = doinikov2021viscoelastic
Hasegawa1969 = hasegawa1969
