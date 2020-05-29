import numpy as np
import math, cmath
from scipy.special import dawsn
from scipy.optimize import fsolve
from functools import lru_cache
import os

""" ALIGNMENT AMPLITUDES """

def ar(rr0,srav,qq,rd0,sd) :
    '''(alpha_r) The uniaxial alignment amplitude for rods
    
    Args:
        rr0 (float): The concentration of monomers
        srav (float): The l-average uniaxial nematic order parameter for rods
        qq (float): The rod-disk/rod-rod excluded volume ratio
        rd0 (float): The concentration of disks
        sd (float): The uniaxial nematic order parameter for disks
    
    Raises:
        ¿RuntimeError: Description? TODO: check this
    
    Returns:
        float: The return value.
        
    '''
    
    return (5/4)*(rr0*srav - 2*qq*rd0*sd)

def ad(zz,rd0,sd,qq,rr0,srav) :
    '''(alpha_d) The uniaxial alignment amplitude for disks
    
    Args:
        zz (float): The disk-disk/rod-rod excluded volume ratio
        rd0 (float): The concentration of disks
        sd (float): The uniaxial nematic order parameter for disks
        qq (float): The rod-disk/rod-rod excluded volume ratio
        rr0 (float): The concentration of monomers
        srav (float): The l-average uniaxial nematic order parameter for rods
    
    Raises:
        ¿RuntimeError: Description? TODO: check this
    
    Returns:
        float: The return value.
        
    '''
    
    return (5/4)*(zz*rd0*sd - 2*qq*rr0*srav)


""" CHI PARAMETER FOR WEAKLY FLEXIBLE RODS """

def xi(rr0,srav,qq,rd0,sd,lp) :
    '''The correction factor on the uniaxial alignment amplitude for rods (it should be alpha_r + xi)
    
    Args:
        rr0 (float): The concentration of monomers
        srav (float): The l-average uniaxial nematic order parameter for rods
        qq (float): The rod-disk/rod-rod excluded volume ratio
        rd0 (float): The concentration of disks
        sd (float): The uniaxial nematic order parameter for disks
        lp (float): The polymer persistence length
    
    Raises:
        ¿RuntimeError: Description? TODO: check this
    
    Returns:
        float: The return value.
        
    '''
    ar_ = ar(rr0,srav,qq,rd0,sd)
    
    return 1 + abs( ar_ ) + lp - math.sqrt(1 + 2*lp + 2*abs( ar_ )*lp + lp**2)

def arbar(rr0,srav,qq,rd0,sd,lp) :
    '''(alpha_r + xi) The effective uniaxial alignment amplitude for rods

    Args:
        rr0 (float): The concentration of monomers
        srav (float): The l-average uniaxial nematic order parameter for rods
        qq (float): The rod-disk/rod-rod excluded volume ratio
        rd0 (float): The concentration of disks
        sd (float): The uniaxial nematic order parameter for disks
        lp (float): The polymer persistence length
    
    Raises:
        ¿RuntimeError: Description? TODO: check this
    
    Returns:
        float: The return value.
        
    '''
    ar_ = ar(rr0,srav,qq,rd0,sd)
    xi_ = xi(rr0,srav,qq,rd0,sd,lp)
    
    return ar_ - np.sign( ar_ ) * xi_


""" POLYMER LENGTH DISTRIBUTION """

def crl(ll,eb,lambda_,rr0,srav,qq,rd0,sd,lp):
    '''(rho_rl) The polymer length distribution in nematic phase
    Returns a complex number, to avoid math domain errors.
    
    Args:
        ll (int): The polymer aggregation number
        eb (float): The association energy
        lambda_ (float): A constant given by the conservation of mass
        rr0 (float): The concentration of monomers
        srav (float): The l-average uniaxial nematic order parameter for rods
        qq (float): The rod-disk/rod-rod excluded volume ratio
        rd0 (float): The concentration of disks
        sd (float): The uniaxial nematic order parameter for disks
        lp (float): The polymer persistence length
    
    Raises:
        ¿RuntimeError: Description? TODO: check this
    
    Returns:
        complex: The return value.
        
    '''
    arbar_ = arbar(rr0,srav,qq,rd0,sd,lp)
    try:
        return ll*math.exp(eb + lambda_*ll)*math.exp(arbar_*ll)*dawsn(
            cmath.sqrt((3*arbar_*ll)/2))/cmath.sqrt((3*arbar_*ll)/2)
    except OverflowError:
        return complex(float('inf'),0)

def crli(ll,eb,rr0):
    '''(rho_rl) The polymer length distribution in isotropic phase
    Returns a complex number, for similarity with crl function.
    
    Args:
        ll (int): The polymer aggregation number
        eb (float): The association energy
        rr0 (float): The concentration of monomers
    
    Raises:
        ¿RuntimeError: Description? TODO: check this
    
    Returns:
        complex: The return value.
        
    '''
    m0 = (1/2) * (1 + cmath.sqrt(1 + 4*rr0*math.exp(-eb)))
    
    try:
        return ll*math.exp(eb)*(1 - m0**-1)**ll
    except OverflowError:
        return complex(float('inf'),0)


""" UNIAXIAL NEMATIC ORDER PARAMETERS """

def csrl(ll, rr0,srav,qq,rd0,sd,lp):
    '''(S_rl) The uniaxial nematic order parameter for rods. 
    Returns a complex number, to avoid math domain errors.
    
    Args:
        ll (int): The polymer aggregation number
        rr0 (float): The concentration of monomers
        srav (float): The l-average uniaxial nematic order parameter for rods
        qq (float): The rod-disk/rod-rod excluded volume ratio
        rd0 (float): The concentration of disks
        sd (float): The uniaxial nematic order parameter for disks
        lp (float): The polymer persistence length
    
    Raises:
        ¿RuntimeError: Description? TODO: check this
    
    Returns:
        complex: The return value.
        
    '''
    arbar_ = arbar(rr0,srav,qq,rd0,sd,lp)
    
    return 1/4*(-2 - 2/(arbar_*ll) + cmath.sqrt(6)/(cmath.sqrt(arbar_*ll)
        *dawsn(cmath.sqrt(3/2)*cmath.sqrt(arbar_*ll))))

def csd(zz,rd0,sd,qq,rr0,srav) :
    '''(S_d) The uniaxial nematic order parameter for disks. 
    Returns a complex number, to avoid math domain errors.
    
    Args:
        zz (float): The disk-disk/rod-rod excluded volume ratio
        rd0 (float): The concentration of disks
        sd (float): The uniaxial nematic order parameter for disks
        qq (float): The rod-disk/rod-rod excluded volume ratio
        rr0 (float): The concentration of monomers
        srav (float): The l-average uniaxial nematic order parameter for rods
    
    Raises:
        ¿RuntimeError: Description? TODO: check this
    
    Returns:
        complex: The return value.
        
    '''
    ad_ = ad(zz,rd0,sd,qq,rr0,srav)
    return 1/4*(-2 - 2/ad_ + cmath.sqrt(6)/(cmath.sqrt(ad_)
        *dawsn(cmath.sqrt(3/2)*cmath.sqrt(ad_))))


""" ISOTROPIC PHASE FUNCTIONALS """

def sigmar(ll, rr0,srav,qq,rd0,sd,lp) :
    '''( sigma(arbar*l) ) orientational entropy for rods. 
    Returns a complex number, to avoid math domain errors.
    
    Args:
        ll (int): The polymer aggregation number
        rr0 (float): The concentration of monomers
        srav (float): The l-average uniaxial nematic order parameter for rods
        qq (float): The rod-disk/rod-rod excluded volume ratio
        rd0 (float): The concentration of disks
        sd (float): The uniaxial nematic order parameter for disks
        lp (float): The polymer persistence length
    
    Raises:
        ¿RuntimeError: Description? TODO: check this
    
    Returns:
        complex: The return value.
        
    '''
    arbar_ = arbar(rr0,srav,qq,rd0,sd,lp)

    return - math.log(math.exp(arbar_*ll)*dawsn(
            cmath.sqrt((3*arbar_*ll)/2))/cmath.sqrt((3*arbar_*ll)/2)
            )+ arbar_*ll*csrl(ll, rr0,srav,qq,rd0,sd,lp)
            
def sigmad(zz,rd0,sd,qq,rr0,srav) :
    '''( sigma(ad) ) orientational entropy for disks. 
    Returns a complex number, to avoid math domain errors.
    
    Args:
        zz (float): The disk-disk/rod-rod excluded volume ratio
        rd0 (float): The concentration of disks
        sd (float): The uniaxial nematic order parameter for disks
        qq (float): The rod-disk/rod-rod excluded volume ratio
        rr0 (float): The concentration of monomers
        srav (float): The l-average uniaxial nematic order parameter for rods

    Raises:
        ¿RuntimeError: Description? TODO: check this
    
    Returns:
        complex: The return value.
        
    '''
    ad_ = ad(zz,rd0,sd,qq,rr0,srav)

    return - math.log(math.exp(ad_)*dawsn(
            cmath.sqrt((3*ad_)/2))/cmath.sqrt((3*ad_)/2)
            )+ ad_*csd(zz,rd0,sd,qq,rr0,srav)

def wr(ll, rr0,srav,qq,rd0,sd,lp) :
    '''( W_Ur(arbar*l) ) W functional for the nematic state.
    Returns a complex number, to avoid math domain errors.
    
    Args:
        ll (int): The polymer aggregation number
        rr0 (float): The concentration of monomers
        srav (float): The l-average uniaxial nematic order parameter for rods
        qq (float): The rod-disk/rod-rod excluded volume ratio
        rd0 (float): The concentration of disks
        sd (float): The uniaxial nematic order parameter for disks
        lp (float): The polymer persistence length
    
    Raises:
        ¿RuntimeError: Description? TODO: check this
    
    Returns:
        complex: The return value.
        
    '''
    arbar_ = arbar(rr0,srav,qq,rd0,sd,lp)

    return - (3/2) * ( (arbar_*ll)**2 + 2*arbar_*ll)*csrl(ll, rr0,srav,qq,rd0,sd,lp)

def wd(ll, rr0,srav,qq,rd0,sd,lp) :
    '''( W_Ud(arbar*l) ) W functional for the anti-nematic state.
    Returns a complex number, to avoid math domain errors.
    
    Args:
        ll (int): The polymer aggregation number
        rr0 (float): The concentration of monomers
        srav (float): The l-average uniaxial nematic order parameter for rods
        qq (float): The rod-disk/rod-rod excluded volume ratio
        rd0 (float): The concentration of disks
        sd (float): The uniaxial nematic order parameter for disks
        lp (float): The polymer persistence length
    
    Raises:
        ¿RuntimeError: Description? TODO: check this
    
    Returns:
        complex: The return value.
        
    '''
    arbar_ = arbar(rr0,srav,qq,rd0,sd,lp)

    return (3/4) * (arbar_*ll)**2 + (3/2*(arbar_*ll)**2-3*arbar_*ll)*csrl(ll, rr0,srav,qq,rd0,sd,lp)

"""EQUATION SYSTEMS SOLVERS"""

@lru_cache(maxsize=32)
def solve_conditions(eb,x,c,zz,qq,lp,llmax,lambdas, sravs, sds):
    """ this iteration resolves S_polymer, S_disc and normalization 
    factor lambda """
    print("Solving conditions for eb = "+str(eb)+", c = "+str(c)+", x = "+str(x))

    # convert to overall monomer and disc concentrations
    rr0 = c*(1 - x)
    rd0 = c*x

    def equations(p) :
        """ Normalization conditions:

        SUM(rho_rl) for every l = rho_r0
        rho_r0^-1 * SUM(S_rl*rho_rl) for every l = S_r average
        sd = 1/4 (-2 - 2/adn + Sqrt[6]/(Sqrt[adn] DawsonF[Sqrt[3/2] Sqrt[adn]])
        """
        lambda_, srav, sd = p
        return (sum([crl(ll,eb,lambda_,rr0,srav,qq,rd0, sd ,lp) for ll in np.arange(1,llmax)])-rr0,  
            sum([csrl(ll, rr0,srav,qq,rd0, sd ,lp)*crl(ll,eb,lambda_,rr0,srav,qq,rd0, sd ,lp)
            for ll in np.arange(1,llmax)])*rr0**-1-srav,
            csd(zz,rd0,sd,qq,rr0,srav) - sd)
    
    # solv1
    solv1 = fsolve(equations, (lambdas, sravs, sds))
    lambdan = solv1[0].real
    sravn = solv1[1].real
    sdn = solv1[2].real
    while 10**5*max([abs(sdn - sds), abs(sravn - sravs), abs(lambdan - lambdas)]) > 1:
        print("Repeating: error = "+str(10**5*max([abs(sdn - sds), abs(sravn - sravs), abs(lambdan - lambdas)])))
        solv1 = fsolve(equations, (lambdas, sravs, sds))
        lambdan = solv1[0].real
        sravn = solv1[1].real
        sdn = solv1[2].real
        sds = sdn
        lambdas = lambdan
        sravs = sravn
    print("Solved!")
    return [sdn,lambdan,sravn]