# **************************************************************************
# *
# * Authors:     Grigory Sharov (gsharov@mrc-lmb.cam.ac.uk)
# *
# * MRC Laboratory of Molecular Biology (MRC-LMB)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************
import os

from pyworkflow.protocol.constants import LEVEL_ADVANCED
from pyworkflow.protocol.params import LabelParam, EnumParam, IntParam
from pyworkflow.viewer import DESKTOP_TKINTER
from pwem.viewers import DataView, EmPlotter, EmProtocolViewer, ChimeraView

from .protocols import ProtCryoEF
from .convert import iterAngles
from .constants import *


class CryoEFViewer(EmProtocolViewer):
    """ Visualization of cryoEF results. """
           
    _environments = [DESKTOP_TKINTER]
    _targets = [ProtCryoEF]
    _label = 'viewer'

    def __init__(self, **kwargs):
        EmProtocolViewer.__init__(self, **kwargs)

    def _defineParams(self, form):
        form.addSection(label='Visualization')
        group = form.addGroup('Volumes')
        group.addParam('displayVol', EnumParam, choices=['slices', 'chimera'],
                       default=VOLUME_SLICES, display=EnumParam.DISPLAY_HLIST,
                       label='Display volume with',
                       help='*slices*: display volumes as 2D slices along z axis.\n'
                            '*chimera*: display volumes as surface with Chimera.')
        group.addParam('doShowOutVol', EnumParam, default=VOL_RS_PSF,
                       choices=['real space PSF', 'fourier space PSF'],
                       display=EnumParam.DISPLAY_COMBO,
                       label='PSF volume to display',
                       help='Display output volumes:\n'
                            '1) First one contains the shape of the point spread '
                            'function (PSF) corresponding to the geometry of '
                            'the orientation distribution.\n'
                            '2) Second one contains the Fourier space (k-space) '
                            'information coverage of the orientation '
                            'distribution. Ideally, it should be spherically '
                            'symmetric.')
        form.addParam('displayAngDist', LabelParam,
                      label='Display angular distribution',
                      help='Display angular distribution as '
                           'interactive 2D in matplotlib.')
        form.addParam('showMollweidePlot', LabelParam,
                      label='Mollweide projection plot of orientation distribution',
                      help='The orientation distributions of the particles are '
                           'plotted on an equal-area Mollweide projection, with '
                           'the color scale representing the local Gaussian kernel '
                           'density (probability distribution function '
                           '[PDF]) of the distribution at every sampled orientation.')
        form.addParam('spheresScale', IntParam, default=100,
                      expertLevel=LEVEL_ADVANCED,
                      label='Spheres size')
        form.addParam('doShowHistogram', LabelParam,
                      label="Show PSF resolution histogram")
        form.addParam('doShowLog', LabelParam,
                      label="Show output log")

    def _getVisualizeDict(self):
        self.protocol._initialize()  # Load filename templates
        return {'doShowOutVol': self._showVolumes,
                'displayAngDist': self._showAngularDistribution,
                'showMollweidePlot': self._showMollweide,
                'doShowHistogram': self._showHistogram,
                'doShowLog': self._showLogFile
                }

# =============================================================================
# ShowVolumes
# =============================================================================
    def _showVolumes(self, param=None):
        if self.displayVol == VOLUME_CHIMERA:
            return self._showVolumesChimera()
        elif self.displayVol == VOLUME_SLICES:
            return self._showVolumeShowj()

    def _showVolumesChimera(self):
        """ Create a chimera script to visualize selected volumes. """
        volume = self._getVolumeName()
        cmdFile = self.protocol._getExtraPath('chimera_volumes.cxc')
        with open(cmdFile, 'w+') as f:
            localVol = os.path.relpath(volume,
                                       self.protocol._getExtraPath())
            if os.path.exists(volume):
                f.write("open %s\n" % localVol)
        view = ChimeraView(cmdFile)
        return [view]

    def _showVolumeShowj(self):
        return [DataView(self._getVolumeName())]

# =============================================================================
# showAngularDistribution
# =============================================================================
    def _showAngularDistribution(self, param=None):
        views = []
        plot = self._createAngDist2D()
        views.append(plot)

        return views

    def _createAngDist2D(self):
        # Common variables to use
        nparts = self.protocol._getInputParticles().getSize()
        title = "Angular Distribution"
        plotter = EmPlotter(windowTitle=title)
        sqliteFn = self.protocol._getFileName('projections')
        if not os.path.exists(sqliteFn):
            self.createAngDistributionSqlite(sqliteFn, nparts,
                                             itemDataIterator=iterAngles(
                                                 self.protocol._getFileName('anglesFn')))
        plotter.plotAngularDistributionFromMd(sqliteFn, title)

        return plotter

    def _showMollweide(self, param=None):
        """ This plot script is based on two scripts by their respective authors:
            - PlotOD.py from cryoEF package
            - https://github.com/PirateFernandez/python3_rln_scripts/blob/main/rln_star_2_mollweide_any_star.py
        """
        import numpy as np
        from matplotlib import spines
        from scipy.stats import gaussian_kde

        views = []
        xplotter = EmPlotter(windowTitle="Mollweide projection plot of orientation distribution")
        fn = np.genfromtxt(self.protocol._getFileName('anglesFn'), delimiter=' ')
        phi = fn[:, 0]
        theta = fn[:, 1]

        # Convert degrees to radians and obey angular range conventions
        x = phi / 180 * np.pi  # x is the phi angle (longitude)
        y = theta / 180 * np.pi  # y is the theta angle (latitude)
        y = -1 * y + np.pi / 2  # The convention in RELION is [0, 180] for theta,
        # whereas for the projection function it is [90, -90], so this conversion is required.
        vertical_rad = np.vstack([y, x])
        m = gaussian_kde(vertical_rad)(vertical_rad)

        ax = xplotter.createSubPlot('', 'phi', 'theta',
                                    projection="mollweide")
        # Plot your points on the projection
        #ax.plot(x, y, ',', alpha=0.5, color='#64B5F6')  # alpha - transparency (from 0 to 1), color - specify hex code
        a = ax.scatter(x, y, cmap='plasma', c=m, s=2, alpha=0.4)
        # Draw the horizontal and the vertical grid lines. Can add more grid lines if required.
        major_ticks_x = [-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi]
        major_ticks_y = [-np.pi / 2, -np.pi / 4, 0, np.pi / 4, np.pi / 2]
        ax.set_xticks(major_ticks_x)
        ax.set_yticks(major_ticks_y)
        ax.set_xticklabels(['-180$^\circ$','-90$^\circ$','0$^\circ$','90$^\circ$','180$^\circ$'],
                           color='grey')
        ax.set_yticklabels(['-90$^\circ$','-45$^\circ$','0$^\circ$','45$^\circ$','90$^\circ$'],
                           color='grey')

        # Set the color and the thickness of the grid lines
        ax.grid(which='both', linestyle='--', linewidth=1, color='#555F61')

        # Set the color and the thickness of the outlines
        for child in ax.get_children():
            if isinstance(child, spines.Spine):
                child.set_color('#555F61')

        xplotter.getColorBar(a)
        xplotter.tightLayout()
        xplotter.show()

        return views.append(xplotter)

# =============================================================================

    def _showHistogram(self, param=None):
        fn = self.protocol._getFileName('output_hist')
        with open(fn) as f:
            views = []
            numberOfBins = 10
            plotter = EmPlotter()
            plotter.createSubPlot("PSF Resolution histogram",
                                  "Resolution (A)", "Ang (str)")
            resolution = [float(line.strip()) for line in f]
        plotter.plotHist(resolution, nbins=numberOfBins)
        plotter.show()

        return views.append(plotter)

    def _showLogFile(self, param=None):
        view = self.textView([self.protocol._getFileName('output_log')],
                             "Output log file")
        return [view]

    def _getVolumeName(self):
        if self.doShowOutVol.get() == VOL_RS_PSF:
            vol = self.protocol._getFileName('real space PSF')
        else:  # VOL_FS_PSF
            vol = self.protocol._getFileName('fourier space PSF')

        return vol
