'''
Author: acse-xy721 xy721@ic.ac.uk
Date: 2022-07-19 13:32:04
LastEditors: acse-xy721 xy721@ic.ac.uk
LastEditTime: 2022-08-30 14:00:25
FilePath: /YXYIPR/test/testall.py
'''
import pytest
import micromagneticmodel as mm
import oommfc as oc
import discretisedfield as df
import numpy as np
from meanfield.Math import Math
from meanfield.Exchange import Exchange
from meanfield.Zeeman import Zeeman
from meanfield.DMI import DMI
from meanfield.Anisotropy import Anisotropy
import meanfield.meanField as mf
import time


@pytest.fixture(scope='module')
def getdfField(L=50e-9, dx=10e-9, dy=10e-9, dz=10e-9, dim=3, Ms=3.84e5):
    """
    It creates a random magnetization field
    with a given mesh size and magnetization
    param L: int
        length of the continuous magnetization field
    param dx: int
        the size of the discrete magnetization field in the x direction
    param dy: int
        the size of the discrete magnetization field in the y direction
    param dz: int
        the size of the discrete magnetization field in the z direction
    param dim: int
        dimension of the field (3 for a vector field)
    param Ms: int
        Saturation magnetization
    return:
        A field object.
    """
    region = df.Region(p1=(0, 0, 0), p2=(L, L, L))
    mesh = df.Mesh(region=region, cell=(dx, dy, dz))

    def value_fun(point):
        """
        It generates a random vector of length 3, normalizes it,
        and returns the first three elements of the normalized vector
        return:
            A tuple of 3 floats.
        """
        vec = np.random.randn(3)
        unit_vec = vec / np.linalg.norm(vec)
        return (unit_vec[0], unit_vec[1], unit_vec[2])
    m = df.Field(mesh, dim=dim, value=value_fun, norm=Ms)
    return m

@pytest.fixture(scope='module')
def getdfField_2(L=200e-9, dx=10e-9, dy=10e-9, dz=10e-9, dim=3, Ms=1e8):
    region = df.Region(p1=(0, 0, 0), p2=(L, L, L))
    mesh = df.Mesh(region=region, cell=(dx, dy, dz))
    def value_fun(point):
        return (0,0,1)
    m = df.Field(mesh, dim=dim, value=value_fun, norm=Ms)
    return m

@pytest.fixture(scope='module')
def getdfField_3(L=1e-9, dx=1e-9, dy=1e-9, dz=1e-9, dim=3, Ms=8e5):
    region = df.Region(p1=(0, 0, 0), p2=(L, L, L))
    mesh = df.Mesh(region=region, cell=(dx, dy, dz))
    def value_fun(point):
        return (1,0,0)
    m = df.Field(mesh, dim=dim, value=value_fun, norm=Ms)
    return m

@pytest.fixture(scope='module')
def getOommfSystem(getdfField):
    """
    `getOommfSystem` is a fixture that returns a `mm.System` object
    with a `m` attribute that is a`mm.Field` object
    with a `data` attribute that is a `numpy.ndarray` object
    with a `shape` attribute that is a `tuple` object
    with a `len` attribute that is an `int` object
    with a value of `3`
    param getdfFeild: object
        This is the object that contains the field data
    return:
        The system object is being returned.
    """
    system = mm.System(name='test_effective')
    system.m = getdfField
    return system

@pytest.fixture(scope='module')
def getOommfSystem_2(getdfField_2):
    system = mm.System(name='test_effective')
    system.m = getdfField_2
    return system

@pytest.fixture(scope='module')
def getOommfSystem_3(getdfField_3):
    system = mm.System(name='test_effective')
    system.m = getdfField_3
    return system

class TestEffectiveFeild:
    @pytest.mark.parametrize(
        ' dx, dy, dz, A, Ms, dim',
        [
            (10e-9, 10e-9, 10e-9, 1, 3.84e5, 3)
        ]
    )
    def testExchange(self, getdfField, getOommfSystem, dx, dy, dz, A, Ms, dim):
        """
        `testExchange` is a function that takes in a `getdfFeild` object,
        a `getOommfSystem` object, and a set of parameters (`dx, dy, dz,
        A, Ms, dim`) and tests whether the effective field computed by OOMMF
        and the effective field computed by the math module are the same.
        getdfFeild:
            This is the function that returns the field from the OOMMF system
        getOommfSystem:
            This is the OOMMF system that we are testing
        dx:
            cell size in x direction
        dy:
            the y-dimension of the mesh
        dz:
            the thickness of the mesh
        A:
            Exchange constant
        Ms:
            Saturation magnetization
        dim:
            dimension of the mesh
        """
        getOommfSystem.energy = (mm.Exchange(A=A))
        oommf_eff_ex = oc.compute(
            getOommfSystem.energy.exchange.effective_field,
            getOommfSystem).array
        math = Math(getdfField.value/Ms, dim, dx, dy, dz)
        math_eff_ex = Exchange(A=A, miu0=mm.consts.mu0,
                               Ms=Ms).effective_field(math)
        assert np.allclose(oommf_eff_ex, math_eff_ex)
        
    def testExchange_2(self, getdfField_2, getOommfSystem_2, dx=10e-9, dy=10e-9, dz=10e-9, A=1, Ms=1e8, dim=3):
        getOommfSystem_2.energy = (mm.Exchange(A=A))
        oommf_eff_ex = oc.compute(
            getOommfSystem_2.energy.exchange.effective_field,
            getOommfSystem_2).array
        math = Math(getdfField_2.value/Ms, dim, dx, dy, dz)
        math_eff_ex = Exchange(A=A, miu0=mm.consts.mu0,
                               Ms=Ms).effective_field(math)
        assert np.allclose(oommf_eff_ex, math_eff_ex)
        
    def testExchange_3(self, getdfField_3, getOommfSystem_3, dx=1e-9, dy=1e-9, dz=1e-9, A=1, Ms=8e5, dim=3):
            getOommfSystem_3.energy = (mm.Exchange(A=A))
            oommf_eff_ex = oc.compute(
                getOommfSystem_3.energy.exchange.effective_field,
                getOommfSystem_3).array
            math = Math(getdfField_3.value/Ms, dim, dx, dy, dz)
            math_eff_ex = Exchange(A=A, miu0=mm.consts.mu0,
                                Ms=Ms).effective_field(math)
            assert np.allclose(oommf_eff_ex, math_eff_ex)  

    @pytest.mark.parametrize(
        ' dx, dy, dz, dim, H, Ms',
        [
            (10e-9, 10e-9, 10e-9, 3, (3, 2, 1), 3.84e5)
        ]
    )
    def testZeeman(self, getdfField, getOommfSystem, dx, dy, dz, dim, H, Ms):
        """
        `testZeeman` is a function that takes in a `getdfFeild` object,
        a `getOommfSystem` object, and a set of parameters(`dx, dy,
        dz, dim, H`)and tests whether the effective field computed by OOMMF
        and the effective field computed by the math module are the same.
        getdfFeild:
            This is the function that returns the dataframe of the field
        getOommfSystem:
            This is the OOMMF system that we are testing
        dx:
            the x-dimension of the mesh
        dy:
            y-dimension of the mesh
        dz:
            the z-dimension of the mesh
        dim:
            dimension of the system
        H:
            The external magnetic field in A/m
        """
        getOommfSystem.energy = (mm.Zeeman(H=H))
        oommf_eff_zm = oc.compute(
            getOommfSystem.energy.zeeman.effective_field, getOommfSystem).array
        math = Math(getdfField.value/Ms, dim, dx, dy, dz)
        math_eff_zm = Zeeman(H).effective_field(math)
        assert np.allclose(oommf_eff_zm, math_eff_zm)
        
    def testZeeman_2(self, getdfField_2, getOommfSystem_2, dx=10e-9, dy=10e-9, dz=10e-9, dim=3, H = (1,1,1), Ms=1e8):
        getOommfSystem_2.energy = (mm.Zeeman(H=H))
        oommf_eff_zm = oc.compute(
            getOommfSystem_2.energy.zeeman.effective_field, getOommfSystem_2).array
        math = Math(getdfField_2.value/Ms, dim, dx, dy, dz)
        math_eff_zm = Zeeman(H).effective_field(math)
        assert np.allclose(oommf_eff_zm, math_eff_zm)
        
    def testZeeman_3(self, getdfField_3, getOommfSystem_3, dx=1e-9, dy=1e-9, dz=1e-9, dim=3, H = (1,3,1), Ms=8e5):
            getOommfSystem_3.energy = (mm.Zeeman(H=H))
            oommf_eff_zm = oc.compute(
                getOommfSystem_3.energy.zeeman.effective_field, getOommfSystem_3).array
            math = Math(getdfField_3.value/Ms, dim, dx, dy, dz)
            math_eff_zm = Zeeman(H).effective_field(math)
            assert np.allclose(oommf_eff_zm, math_eff_zm)

    @pytest.mark.parametrize(
        ' dx, dy, dz, dim, D, Ms',
        [
            (10e-9, 10e-9, 10e-9, 3, 2, 3.84e5)
        ]
    )
    def testDMI(self, getdfField, getOommfSystem, dx, dy, dz, dim, D, Ms):
        getOommfSystem.energy = (mm.DMI(D=D, crystalclass='T'))
        oommf_eff_dmi = oc.compute(
            getOommfSystem.energy.dmi.effective_field, getOommfSystem).array
        
        math = Math(getdfField.value/Ms, dim, dx, dy, dz)
        math_eff_dmi = DMI(D=D, miu0=mm.consts.mu0,
                           Ms=Ms).effective_field(math)
        assert np.allclose(oommf_eff_dmi, math_eff_dmi)
        
    def testDMI_2(self, getdfField_2, getOommfSystem_2, dx=10e-9, dy=10e-9, dz=10e-9, dim=3, D=0.5, Ms=1e8):
        getOommfSystem_2.energy = (mm.DMI(D=D, crystalclass='T'))
        oommf_eff_dmi = oc.compute(
            getOommfSystem_2.energy.dmi.effective_field, getOommfSystem_2).array
        
        math = Math(getdfField_2.value/Ms, dim, dx, dy, dz)
        math_eff_dmi = DMI(D=D, miu0=mm.consts.mu0,
                           Ms=Ms).effective_field(math)
        assert np.allclose(oommf_eff_dmi, math_eff_dmi)
        
    def testDMI_3(self, getdfField_3, getOommfSystem_3, dx=1e-9, dy=1e-9, dz=1e-9, dim=3, D=1.8, Ms=8e5):
        getOommfSystem_3.energy = (mm.DMI(D=D, crystalclass='T'))
        oommf_eff_dmi = oc.compute(
            getOommfSystem_3.energy.dmi.effective_field, getOommfSystem_3).array
        
        math = Math(getdfField_3.value/Ms, dim, dx, dy, dz)
        math_eff_dmi = DMI(D=D, miu0=mm.consts.mu0,
                           Ms=Ms).effective_field(math)
        assert np.allclose(oommf_eff_dmi, math_eff_dmi)
        
    @pytest.mark.parametrize(
        ' dx, dy, dz, dim, K, u, Ms',
        [
            (10e-9, 10e-9, 10e-9, 3, 1e5, [0, 0, 1], 3.84e5)
        ]
    )
    def testAnisotropy(self, getdfField, getOommfSystem, dx, dy, dz, dim, K, u, Ms):
        getOommfSystem.energy =  mm.UniaxialAnisotropy(K=K, u=u)
        oommf_eff_an = oc.compute(
            getOommfSystem.energy.effective_field, getOommfSystem).array
        math = Math(getdfField.value/Ms, dim, dx, dy, dz)
        math_eff_an = Anisotropy(K=K, u=u, miu0=mm.consts.mu0,
                            Ms=Ms).effective_field(math)
        assert np.allclose(oommf_eff_an, math_eff_an)

    def testAnisotropy_2(self, getdfField_2, getOommfSystem_2, dx=10e-9, dy=10e-9, dz=10e-9, dim=3, K=100, u=[1,0,0], Ms=1e8):
        getOommfSystem_2.energy =  mm.UniaxialAnisotropy(K=K, u=u)
        oommf_eff_an = oc.compute(
            getOommfSystem_2.energy.effective_field, getOommfSystem_2).array
        math = Math(getdfField_2.value/Ms, dim, dx, dy, dz)
        math_eff_an = Anisotropy(K=K, u=u, miu0=mm.consts.mu0,
                            Ms=Ms).effective_field(math)
        assert np.allclose(oommf_eff_an, math_eff_an)
        
    def testAnisotropy_3(self, getdfField_3, getOommfSystem_3, dx=1e-9, dy=1e-9, dz=1e-9, dim=3, K=2e2, u=[1,0,0], Ms=8e5):
        getOommfSystem_3.energy =  mm.UniaxialAnisotropy(K=K, u=u)
        oommf_eff_an = oc.compute(
            getOommfSystem_3.energy.effective_field, getOommfSystem_3).array
        math = Math(getdfField_3.value/Ms, dim, dx, dy, dz)
        math_eff_an = Anisotropy(K=K, u=u, miu0=mm.consts.mu0,
                            Ms=Ms).effective_field(math)
        assert np.allclose(oommf_eff_an, math_eff_an)
        


class TestMath:
    
    def testFirstDerivative(self):
        mesh = df.Mesh(region=df.Region(
            p1=(0, 0, 0),
            p2=(100e-9, 100e-9, 100e-9)),
            cell=(10e-9, 10e-9, 10e-9))

        def test_fun(point):
            x, y, z = point
            return 2*x + y
        fun_matrix = df.Field(mesh, dim=1, value=test_fun).array
        # my own func
        math = Math(m=fun_matrix, dim=1, dx=10e-9, dy=10e-9, dz=10e-9)
        first_Derivative_x = math.derivative(direction="x", n=1,
                                             bc="pbc", bc_input=None)
        first_Derivative_y = math.derivative(direction="y", n=1,
                                             bc="pbc", bc_input=None)
        first_Derivative_z = math.derivative(direction="z", n=1,
                                             bc="pbc", bc_input=None)
        average_x = first_Derivative_x[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_y = first_Derivative_y[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_z = first_Derivative_z[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average_x, 2)
        assert np.allclose(average_y, 1)
        assert np.allclose(average_z, 0)

    def testFirstDerivative_2(self):
        """
        This function tests the first derivative function
        for a vector feild(dim = 3)
        """
        mesh = df.Mesh(region=df.Region(
            p1=(0, 0, 0),
            p2=(100e-9, 100e-9, 100e-9)),
            cell=(10e-9, 10e-9, 10e-9))

        def test_fun(point):
            x, y, z = point
            return (2*x + 1, 3*x, y+z)
        fun_matrix = df.Field(mesh, dim=3, value=test_fun).array
        # my own func
        math = Math(m=fun_matrix, dim=3, dx=10e-9, dy=10e-9, dz=10e-9)
        first_Derivative_x = math.derivative(direction="x", n=1,
                                             bc="pbc", bc_input=None)
        first_Derivative_y = math.derivative(direction="y", n=1,
                                             bc="pbc", bc_input=None)
        first_Derivative_z = math.derivative(direction="z", n=1,
                                             bc="pbc", bc_input=None)
        average_x = first_Derivative_x[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_y = first_Derivative_y[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_z = first_Derivative_z[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average_x, (2, 3, 0))
        assert np.allclose(average_y, (0, 0, 1))
        assert np.allclose(average_z, (0, 0, 1))
        
    def testFirstDerivative_3(self):
        mesh = df.Mesh(region=df.Region(
            p1=(0, 0, 0),
            p2=(100e-9, 100e-9, 100e-9)),
            cell=(10e-9, 10e-9, 10e-9))

        def test_fun(point):
            x, y, z = point
            return 0
        fun_matrix = df.Field(mesh, dim=1, value=test_fun).array
        # my own func
        math = Math(m=fun_matrix, dim=1, dx=10e-9, dy=10e-9, dz=10e-9)
        first_Derivative_x = math.derivative(direction="x", n=1,
                                             bc="pbc", bc_input=None)
        first_Derivative_y = math.derivative(direction="y", n=1,
                                             bc="pbc", bc_input=None)
        first_Derivative_z = math.derivative(direction="z", n=1,
                                             bc="pbc", bc_input=None)
        average_x = first_Derivative_x[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_y = first_Derivative_y[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_z = first_Derivative_z[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average_x, 0)
        assert np.allclose(average_y, 0)
        assert np.allclose(average_z, 0)
    def testFirstDerivative_4(self):
        mesh = df.Mesh(region=df.Region(
            p1=(0, 0, 0),
            p2=(100e-9, 100e-9, 100e-9)),
            cell=(10e-9, 10e-9, 10e-9))

        def test_fun(point):
            x, y, z = point
            return (0,0,0)
        fun_matrix = df.Field(mesh, dim=3, value=test_fun).array
        # my own func
        math = Math(m=fun_matrix, dim=3, dx=10e-9, dy=10e-9, dz=10e-9)
        first_Derivative_x = math.derivative(direction="x", n=1,
                                             bc="pbc", bc_input=None)
        first_Derivative_y = math.derivative(direction="y", n=1,
                                             bc="pbc", bc_input=None)
        first_Derivative_z = math.derivative(direction="z", n=1,
                                             bc="pbc", bc_input=None)
        average_x = first_Derivative_x[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_y = first_Derivative_y[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_z = first_Derivative_z[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average_x, 0)
        assert np.allclose(average_y, 0)
        assert np.allclose(average_z, 0)
        
    def testSecondDerivative(self):
        mesh = df.Mesh(region=df.Region(
            p1=(0, 0, 0),
            p2=(100e-9, 100e-9, 100e-9)),
            cell=(10e-9, 10e-9, 10e-9))

        def test_fun(point):
            x, y, z = point
            return x**2+y
        fun_matrix = df.Field(mesh, dim=1, value=test_fun).array
        math = Math(m=fun_matrix, dim=1, dx=10e-9, dy=10e-9, dz=10e-9)
        second_Derivative_x = math.derivative(direction="x", n=2,
                                              bc="pbc", bc_input=None)
        second_Derivative_y = math.derivative(direction="y", n=2,
                                              bc="pbc", bc_input=None)
        second_Derivative_z = math.derivative(direction="z", n=2,
                                              bc="pbc", bc_input=None)
        average_x = second_Derivative_x[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_y = second_Derivative_y[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_z = second_Derivative_z[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average_x, 2)
        assert np.allclose(average_y, 0)
        assert np.allclose(average_z, 0)
        
    def testSecondDerivative_2(self):
        mesh = df.Mesh(region=df.Region(
        p1=(0, 0, 0),
        p2=(100e-9, 100e-9, 100e-9)),
        cell=(10e-9, 10e-9, 10e-9))

        def test_fun(point):
            x, y, z = point
            return 0
        fun_matrix = df.Field(mesh, dim=1, value=test_fun).array
        math = Math(m=fun_matrix, dim=1, dx=10e-9, dy=10e-9, dz=10e-9)
        second_Derivative_x = math.derivative(direction="x", n=2,
                                              bc="pbc", bc_input=None)
        second_Derivative_y = math.derivative(direction="y", n=2,
                                              bc="pbc", bc_input=None)
        second_Derivative_z = math.derivative(direction="z", n=2,
                                              bc="pbc", bc_input=None)
        average_x = second_Derivative_x[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_y = second_Derivative_y[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_z = second_Derivative_z[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average_x, 0)
        assert np.allclose(average_y, 0)
        assert np.allclose(average_z, 0)

    def testSecondDerivative_3(self):
        """
        This function tests the first derivative function
        for a vector feild(dim = 3)
        """
        mesh = df.Mesh(region=df.Region(
            p1=(0, 0, 0),
            p2=(100e-9, 100e-9, 100e-9)),
            cell=(10e-9, 10e-9, 10e-9))

        def test_fun(point):
            x, y, z = point
            return (z**2, 3*x+1, y**2)
        fun_matrix = df.Field(mesh, dim=3, value=test_fun).array
        # my own func
        math = Math(m=fun_matrix, dim=3, dx=10e-9, dy=10e-9, dz=10e-9)
        second_Derivative_x = math.derivative(direction="x", n=2,
                                              bc="pbc", bc_input=None)
        second_Derivative_y = math.derivative(direction="y", n=2,
                                              bc="pbc", bc_input=None)
        second_Derivative_z = math.derivative(direction="z", n=2,
                                              bc="pbc", bc_input=None)
        average_x = second_Derivative_x[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_y = second_Derivative_y[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_z = second_Derivative_z[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average_x, (0, 0, 0))
        assert np.allclose(average_y, (0, 0, 2))
        assert np.allclose(average_z, (2, 0, 0))

    def testSecondDerivative_4(self):
        mesh = df.Mesh(region=df.Region(
        p1=(0, 0, 0),
        p2=(100e-9, 100e-9, 100e-9)),
        cell=(20e-9, 20e-9, 20e-9))

        def test_fun(point):
            return (0,0,0)
        fun_matrix = df.Field(mesh, dim=3, value=test_fun).array
        math = Math(m=fun_matrix, dim=3, dx=20e-9, dy=20e-9, dz=20e-9)
        second_Derivative_x = math.derivative(direction="x", n=2,
                                              bc="pbc", bc_input=None)
        second_Derivative_y = math.derivative(direction="y", n=2,
                                              bc="pbc", bc_input=None)
        second_Derivative_z = math.derivative(direction="z", n=2,
                                              bc="pbc", bc_input=None)
        average_x = second_Derivative_x[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_y = second_Derivative_y[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        average_z = second_Derivative_z[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average_x, 0)
        assert np.allclose(average_y, 0)
        assert np.allclose(average_z, 0)
    def testLaplace(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(10, 10, 10), cell=(2, 2, 2))
        f = df.Field(mesh, dim=3, value=(0, 0, 0))
        math = Math(m=f.array, dim=3, dx=2, dy=2, dz=2)
        laplace = math.laplace()
        average = laplace[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average, (0, 0, 0))

        def value_fun(point):
            x, y, z = point
            return x + y + z
        f = df.Field(mesh, dim=1, value=value_fun)
        laplace = Math(m=f.array, dim=1, dx=2, dy=2, dz=2).laplace()
        average = laplace[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert average == 0

        def value_fun(point):
            x, y, z = point
            return 2 * x * x + 2 * y * y + 3 * z * z
        f = df.Field(mesh, dim=1, value=value_fun)
        laplace = Math(m=f.array, dim=1, dx=2, dy=2, dz=2).laplace()
        average = laplace[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert average == 14

        def value_fun(point):
            x, y, z = point
            return (2 * x * x, 2 * y * y, 3 * z * z)
        f = df.Field(mesh, dim=3, value=value_fun)
        laplace = Math(m=f.array, dim=3, dx=2, dy=2, dz=2).laplace()
        average = laplace[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average, (4, 4, 6))

    def testCurl(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(10, 10, 10), cell=(2, 2, 2))
        f = df.Field(mesh, dim=3, value=(0, 0, 0))
        math = Math(m=f.array, dim=3, dx=2, dy=2, dz=2)
        curl = math.curl()
        average = curl[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average, (0, 0, 0))

        def value_fun(point):
            x, y, z = point
            return (x, y, z)
        f = df.Field(mesh, dim=3, value=value_fun)
        math = Math(m=f.array, dim=3, dx=2, dy=2, dz=2)
        curl = math.curl()
        average = curl[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average, (0, 0, 0))
        
        def value_fun(point):
            x, y, z = point
            return (x+y+z, 2*x+2*y+2*z, 4*y)
        f = df.Field(mesh, dim=3, value=value_fun)
        math = Math(m=f.array, dim=3, dx=2, dy=2, dz=2)
        curl = math.curl()
        average = curl[1:-1, 1:-1, 1:-1].mean(axis=(0, 1, 2))
        assert np.allclose(average, (2,1,1))
    
    @pytest.mark.parametrize(
        ' p2, dx, dy, dz, bc, bc_input, answer',
        [
            ((30e-9, 30e-9, 30e-9), 10e-9, 10e-9, 10e-9, "pbc", None, [2,2,2]),
            ((50e-9, 50e-9, 50e-9), 10e-9, 10e-9, 10e-9, "neumann", 0, [2,2,2]),
            ((50e-9, 50e-9, 50e-9), 10e-9, 10e-9, 10e-9, "neumann", 2e10, [-198,-198,-198]),
            ((20e-9, 20e-9, 20e-9), 10e-9, 10e-9, 10e-9, "dirichlet", 0, [0,0,0]),
            ((40e-9, 40e-9, 40e-9), 10e-9, 10e-9, 10e-9, "dirichlet", 3, [3,3,3]),
            ((10e-9, 10e-9, 10e-9), 10e-9, 10e-9, 10e-9, "pbc", None, [2,2,2]),
            ((1e-9, 1e-9, 1e-9), 1e-9, 1e-9, 1e-9, "neumann", 0, [2,2,2]),
        ]
    )
    def testPad(self, p2, dx, dy, dz, bc, bc_input, answer):
        mesh = df.Mesh(
            p1=(0, 0, 0),
            p2= p2,
            cell=(dx, dy, dz))

        def test_fun(point):
            x, y, z = point
            return (2, 2, 2)
        fun_matrix = df.Field(mesh, dim=3, value=test_fun).array
        # my own func
        math = Math(m=fun_matrix, dim=3, dx=dx, dy=dy, dz=dz)
        pad_result = math.pad(bc=bc, bc_input=bc_input)
        print(pad_result[0,1:-1,1:-1,])
        assert np.allclose(pad_result[0,1:-1,1:-1,], answer)
  
   
class TestMeanfield:
    def testLangevin(self):
        # When the input is large, Langevin approaches 1
        result = mf.Langevin(1e100)
        assert result == 1
        
        result = mf.Langevin(1e100*np.ones((3,3,3,3)))
        assert np.allclose(result, np.ones((3,3,3,3)))
        
        #When the input is very small,
        # the value of Lang Zhiwan is between 0 and 1,
        # and Y shows an increasing trend with the value of X
        
        result = mf.Langevin(1e-10)
        assert result == 0
        
        result = mf.Langevin(1e-100*np.ones((3,3,3,3)))
        assert np.allclose(result, np.zeros((3,3,3,3)))
        
        result = mf.Langevin(50)
        assert result == 0.98
        
        result = mf.Langevin(288)
        assert result == 0.9965277777777778
        
        result = mf.Langevin(100*np.ones((5,5,5,3)))
        assert np.allclose(result, 0.99*np.ones((5,5,5,3)))
        
        result = mf.Langevin(3*np.ones((3,3,3,3)))
        assert np.allclose(result, 0.67163649*np.ones((3,3,3,3)))
        
    @pytest.mark.parametrize(
        ' iter_num, tol, maxiter, Ms, m , Hef, Judgement',
        [
            (1000, 1e-4, 20000, 8e5,  np.ones((3,3,3,3)), np.ones((3,3,3,3)), True),
            (10, 1e-4, 20000, 1e10,  np.ones((5,5,5,3)), np.ones((5,5,5,3)), True),
            (20000000, 1e-4, 20000, 8e5,  np.ones((3,3,3,3)), np.ones((3,3,3,3)), True),
            (100, 1e-100, 20000, 1,  np.array([x for x in range(1,82)]).reshape(3,3,3,3), np.ones((3,3,3,3)), False),
            (50, 1e-10, 50000, 1e8,  np.array([2*x for x in range(1,82)]).reshape(3,3,3,3), np.ones((3,3,3,3)), False),
        ]
    )
    def testEndcondition(self, iter_num, tol, maxiter, Ms, m , Hef, Judgement):
        # 1. the cross product of the new magnetisation field
        # and the effective field is less than the tolerance return True
        
        # 2. the number of iterations is greater than
        # the maximum number of iterations return True

        assert mf.end_condition(iter_num, m, Hef, tol, maxiter, Ms) == Judgement
        
    def testMeanfield(self,  getdfField, getOommfSystem):
        dx = 10e-9
        dy = 10e-9
        dz = 10e-9
        dim = 3
        Ms = 3.84e5
        miu0 = mm.consts.mu0
        A = 8.78e-12
        D = 1.58e-3
        B = 0.1
        beta = float("inf")
        H = (0, 0, B/miu0)
        lamda = 0.005
        maxiter = 100000
        tol = 1e-5
        K = 1e5
        u = [0,0,1]
     
        getOommfSystem.energy = (mm.Exchange(A=A) + mm.DMI(D=D, crystalclass='T') +
                        mm.Zeeman(H=H) +  mm.UniaxialAnisotropy(K=K, u=u))

        md = oc.MinDriver()
        md.drive(getOommfSystem)
        oommfc_result = getOommfSystem.m.array / Ms
        math = Math(getdfField.array, dim, dx, dy, dz)
        math_eff = mf.mean_field(math, D, Ms, miu0, A, H, beta, lamda, maxiter,
               tol, dim, dx, dy, dz, K, u) / Ms
        assert np.allclose(oommfc_result, math_eff, atol=1e-4)
        
    def testMeanfield_2(self,  getdfField_2, getOommfSystem_2):
        dx = 10e-9
        dy = 10e-9
        dz = 10e-9
        dim = 3
        Ms = 1e8
        miu0 = mm.consts.mu0
        A = 7e-8
        D = 2e-4
        B = 0.1
        beta = float("inf")
        H = (0, 0, B/miu0)
        lamda = 0.05
        maxiter = 100000
        tol = 1e-5
        K = 2e3
        u = [0,1,0]
     
        getOommfSystem_2.energy = (mm.Exchange(A=A) + mm.DMI(D=D, crystalclass='T') +
                        mm.Zeeman(H=H) +  mm.UniaxialAnisotropy(K=K, u=u))

        md = oc.MinDriver()
        md.drive(getOommfSystem_2)
        oommfc_result = getOommfSystem_2.m.array / Ms
        math = Math(getdfField_2.array, dim, dx, dy, dz)
        math_eff = mf.mean_field(math, D, Ms, miu0, A, H, beta, lamda, maxiter,
               tol, dim, dx, dy, dz, K, u) / Ms
        assert np.allclose(oommfc_result, math_eff, atol=1e-4)

       



        
    
        
       
        
        
            
