"""
Limb darkening toolkit
Copyright (C) 2015  Hannu Parviainen <hpparvi@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import numpy as np
from numpy import asarray, sqrt, log2


class LDModel(object):
    npar = None
    name = None
    abbr = None

    def __init__(self):
        raise NotImplementedError

    def __call__(self, mu, pv):
        raise NotImplementedError

    @classmethod
    def eval(cl, mu, pv):
        raise NotImplementedError


class LinearModel(LDModel):
    """Linear limb darkening model (Mandel & Agol, 2001)."""
    npar = 1
    name = 'linear'
    abbr = 'ln'

    @classmethod
    def evaluate(cl, mu, pv):
        assert len(pv) == cl.npar
        mu = asarray(mu)
        return 1. - pv[0]*(1.-mu)


class QuadraticModel(LDModel):
    """Quadratic limb darkening model (Kopal, 1950)."""
    npar = 2
    name = 'quadratic'
    abbr = 'qd'

    @classmethod
    def evaluate(cl, mu, pv):
        assert len(pv) == cl.npar
        mu = asarray(mu)
        return 1. - pv[0]*(1.-mu) - pv[1]*(1.-mu)**2


class TriangularQuadraticModel(LDModel):
    """Quadratic limb darkening model with the parametrisation described by Kipping (MNRAS 435, 2013)."""
    npar = 2
    name = 'triangular_quadratic'
    abbr = 'tq'

    @classmethod
    def evaluate(cl, mu, pv):
        assert len(pv) == cl.npar
        mu = asarray(mu)
        a, b = sqrt(pv[0]), 2*pv[1]
        u, v = a*b, a*(1. - b)
        return 1. - u*(1.-mu) - v*(1.-mu)**2


class SquareRootModel(LDModel):
    """Square root limb darkening model (van Hamme, 1993)."""
    npar = 2
    name = 'sqrt'
    abbr = 'sq'

    @classmethod
    def evaluate(cl, mu, pv):
        assert len(pv) == cl.npar
        mu = asarray(mu)
        return 1. - pv[0]*(1.-mu) - pv[1]*(1.-mu**0.5)


class NonlinearModel(LDModel):
    """Nonlinear limb darkening model (Claret, 2000)."""
    npar = 4
    name = 'nonlinear'
    abbr = 'nl'

    @classmethod
    def evaluate(cl, mu, pv):
        assert len(pv) == cl.npar
        mu = asarray(mu)
        return (1. - (pv[0]*(1.-mu**0.5) + pv[1]*(1.-mu) +
                      pv[2]*(1.-mu**1.5) + pv[3]*(1.-mu**2  )))


class GeneralModel(LDModel):
    """General limb darkening model (Gimenez, 2006)"""
    npar = None
    name = 'general'
    abbr = 'ge'

    @classmethod
    def evaluate(cl, mu, pv):
        mu = asarray(mu)
        return 1. - np.sum([c*(1.-mu**(i+1)) for i,c in enumerate(pv)], 0)

class Power2Model(LDModel):
    """Power-2 limb darkening model (Morello et al, 2017)."""
    npar = 2
    name = 'power2'
    abbr = 'p2'

    @classmethod
    def evaluate(cl, mu, pv):
        assert len(pv) == cl.npar
        mu = asarray(mu)
        return 1. - pv[0]*(1.-(mu**pv[1]))

class Power2MPModel(LDModel):
    """Power-2 limb darkening model with an alternative parametrisation (Maxted, P.F.L., 2018)."""
    npar = 2
    name = 'power2mp'
    abbr = 'p2mp'

    @classmethod
    def evaluate(cl, mu, pv):
        assert len(pv) == cl.npar
        mu = asarray(mu)
        c = 1 - pv[0] + pv[1]
        a = log2(c/pv[1])
        return 1. - c*(1.-(mu**a))


models = {'linear':    LinearModel,
          'quadratic': QuadraticModel,
          'triquadratic': TriangularQuadraticModel,
          'sqrt':      SquareRootModel,
          'nonlinear': NonlinearModel,
          'general':   GeneralModel,
          'power2':    Power2Model,
          'power2mp': Power2MPModel}

