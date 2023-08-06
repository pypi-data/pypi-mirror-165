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
from numpy import rad2deg
from numpy.linalg import inv


def parseOutput(filename):
    """ Retrieve efficiency, mean PSF res, stdev, worst and best PSF res
    from the output log file of the cryoEF execution.
    """
    result = []
    if os.path.exists(filename):
        with open(filename) as f:
            for line in f:
                if "Efficiency:" in line:
                    result.append(line.split()[1])
                elif "Mean PSF resolution:" in line:
                    result.append(line.split()[3])
                elif "Standard deviation:" in line:
                    result.append(line.split()[2])
                elif "Worst PSF resolution:" in line:
                    result.append(line.split()[3])
                elif "Best PSF resolution" in line:
                    result.append(line.split()[3])
                    break

    return map(float, result)


def iterAngles(fn):
    with open(fn) as f:
        for line in f:
            rot, tilt = map(float, line.split())
            yield rot, tilt


def writeAnglesFn(img, fn):
    # get alignment parameters for each particle
    angles = geometryFromMatrix(img.getTransform().getMatrix())
    rot, tilt, _ = angles
    fn.write("%0.6f %0.6f\n" % (rot, tilt))


def geometryFromMatrix(matrix):
    from pwem.convert.transformations import euler_from_matrix

    matrix = inv(matrix)
    angles = -rad2deg(euler_from_matrix(matrix, axes='szyz'))

    return angles
