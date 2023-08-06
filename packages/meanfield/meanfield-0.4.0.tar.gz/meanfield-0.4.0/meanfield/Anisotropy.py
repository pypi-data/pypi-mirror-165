'''
Author: acse-xy721 xy721@ic.ac.uk
Date: 2022-08-14 16:14:01
LastEditors: acse-xy721 xy721@ic.ac.uk
LastEditTime: 2022-08-30 13:58:22
FilePath: /irp-xy721/meanfield/A.py
'''
from .EnergyTerm import EnergyTerm
# from EnergyTerm import EnergyTerm


class Anisotropy(EnergyTerm):
    """Uniaxial Anisotropy energy term class
    This class defines effective field of uniaxial anisotropy energy term.

    ``K``, ``u``, ``miu0``,  ``Ms`` are used to define the uniaxial
    anisotropy energy term.

    Parameters
    ----------
    K : float, int
        Anisotropy energy constant
    u : tuple, list
        Axis unit-vector
    miu0: float, int
        the permeability of free space
    Ms: float, int
        Saturation magnetisation

    Examples
    --------
    1. Defining a three-dimensional vector field then
    initialize the uniaxial anisotropy energy term

    >>> import discretisedfield as df
    >>> import numpy as np
    >>> from Math import Math
    >>> region = df.Region(p1=(0, 0, 0), p2=(50e-9, 50e-9, 50e-9))
    >>> mesh = df.Mesh(region=region, cell=(10e-9, 10e-9, 10e-9))
    >>> def value_fun(point):
    ...     vec = np.random.randn(3)
    ...     unit_vec = vec / np.linalg.norm(vec)
    ...     return (unit_vec[0], unit_vec[1], unit_vec[2])
    >>> Ms =  8e5
    >>> K = 1e5
    >>> u = [0,0,1]
    >>> miu0 = 12.57*1e-7
    >>> m = df.Field(mesh, dim=3, value=value_fun, norm=Ms)
    >>> math = Math(m.array/Ms, dim=3, dx=10e-9, dy=10e-9, dz=10e-9)
    >>> result = Anisotropy(K, u, miu0, Ms)

    """

    def __init__(self, K, u, miu0, Ms):
        self.K = K
        self.u = u
        self.miu0 = miu0
        self.Ms = Ms

    def effective_field(self, m):
        """
        effective field for uniaxial anisotropy energy term
        .. math::
        $\\vec{H}_{\\text {eff }}^{an}=\\frac{2 K_{u}}{\\mu_{0} M_{s}}
        (\vec{m}\\cdot\\hat{u})\\hat{u}$

        Parameters
        ----------
        m: ndarray
        normalised magnetisation field

        Returns
        -------
        The effective field for uniaxial anisotropy energy term of
        the magnetisation field

        Examples
        --------
        1. Calculate effective field for DMI energy term
        >>> import discretisedfield as df
        >>> import numpy as np
        >>> from Math import Math
        >>> region = df.Region(p1=(0, 0, 0), p2=(50e-9, 50e-9, 50e-9))
        >>> mesh = df.Mesh(region=region, cell=(10e-9, 10e-9, 10e-9))
        >>> def value_fun(point):
        ...     vec = np.random.randn(3)
        ...     unit_vec = vec / np.linalg.norm(vec)
        ...     return (unit_vec[0], unit_vec[1], unit_vec[2])
        >>> Ms =  8e5
        >>> K = 1e5
        >>> u = [0,0,1]
        >>> miu0 = 12.57*1e-7
        >>> m = df.Field(mesh, dim=3, value=value_fun, norm=Ms)
        >>> math = Math(m.array/Ms, dim=3, dx=10e-9, dy=10e-9, dz=10e-9)
        >>> result = Anisotropy(K, u, miu0, Ms).effective_field(math)
        """
        return (2 * self.K * m.m * self.u *
                self.u) / (self.miu0 * self.Ms)
