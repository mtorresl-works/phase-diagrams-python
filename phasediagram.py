import antip_utils as utils
import numpy as np
from scipy.optimize import fsolve
from functools import lru_cache
import math, cmath
res = []

""" excluded volume rations """

qq = 1
zz = 1

""" starting values for nematic order parameters and normalization 
constant, this is the tricky bit, they need to be reasonably close to 
the real values that are a priori unknown """

sravs = 0.8
sds = -0.4
lambdas = -3

""" starting values for isotrpic and nematic mole fractions and
concentrations, this is the tricky bit, they need to be reasonably close 
to the real values that are a priori unknown """

xi = 0.01 # we take x_isotropic as the free parameter
xas=0.5
cis=4.0
cas=4.0


""" cut-off for polymerization degree, note: this value should be 
large enough to make sure the polymer distribution remains close to 
zero at llmax, if not llmax should be increased which slows down the 
computation """

llmax = 150

""" persistence length """

lp = 5

@lru_cache(maxsize=32)
def solve_conditions(eb,x,c):
    """ this iteration resolves S_polymer, S_disc and normalization 
    factor lambda """
    print("Solving conditions for eb = "+str(eb)+", c = "+str(c)+", x = "+str(x))
    df = 100

    # convert to overall monomer and disc concentrations
    rr0 = c*(1 - x)
    rd0 = c*x

    # starting values for nematic order parameters and normalization constant
    sravs = 0.8
    sds = -0.4
    lambdas = -3
    
    while df > 1 :
        
        def equations(p) :
            """ Normalization conditions:

            SUM(rho_rl) for every l = rho_r0
            SUM(S_rl*rho_rl) for every l = S_r average
            
            """
            lambda_, srav, sd = p
            return (sum([utils.crl(ll,eb,lambda_,rr0,srav,qq,rd0, sd ,lp) for ll in np.arange(1,llmax)])-rr0,  
                sum([utils.csrl(ll, rr0,srav,qq,rd0, sd ,lp)*utils.crl(ll,eb,lambda_,rr0,srav,qq,rd0, sd ,lp)
                for ll in np.arange(1,llmax)])*rr0**-1-srav,
                utils.csd(zz,rd0,sd,qq,rr0,srav) - sd)
        
        # solv1
        solv1 = fsolve(equations, (lambdas, sravs, sds))
        lambdan = solv1[0].real
        sravn = solv1[1].real
        sdn = solv1[2].real
        
        df = 10**5*max([abs(sdn - sds), abs(sravn - sravs), abs(lambdan - lambdas)])
        print(df)
        
        sds = sdn
        
        lambdas = lambdan
        
        sravs = sravn
    print("Solved!")
    return [sdn,lambdan,sravn]

def muri(eb,x,c) :
    return sum([utils.crli(ll,eb,(1-x)*c)/ll*(cmath.log(utils.crli(ll,eb,(1-x)*c)/ll)-eb) for ll in np.arange(1,llmax)]) + 2*c

def mura(eb,x,c) :
    
    conditions = solve_conditions(eb,x,c)
    sd = conditions[0]
    lambda_ = conditions[1]
    srav = conditions[2]

    def w(ll) :
        if x <= 0.5: return utils.wr(ll, (1-x)*c,srav,qq,x*c,sd,lp)
        else : return utils.wd(ll, (1-x)*c,srav,qq,x*c,sd,lp)
    print("x = "+str(x))
    return sum([ utils.crl(ll,eb,lambda_,(1-x)*c,srav,qq,x*c,sd,lp) / (ll*(1-x)*c) * 
    ( cmath.log(utils.crl(ll,eb,lambda_,(1-x)*c,srav,qq,x*c,sd,lp)/ll) + utils.sigmar(ll, (1-x)*c,srav,qq,x*c,sd,lp)
    - eb - 2*ll/(3*lp)*w(ll) ) for ll in np.arange(1,llmax)]) + 2*(1-x)*c*(1 - (5/8)*srav**2) + 2*x*c*(1 + (5/4)*srav*sd)

def mudi(x,c) :
    return cmath.log(x*c) + 2*c

def muda(eb,x,c) :
    
    conditions = solve_conditions(eb,x,c)
    sd = conditions[0]
    srav = conditions[2]

    return cmath.log(x*c) + utils.sigmad(zz,x*c,sd,qq,(1-x)*c,srav) + 2*x*c*(1 - (5/8)*sd**2) + 2*(1-x)*c*(1 + (5/4)*srav*sd)

def pi(x,c):
    return sum([utils.crli(ll,eb,(1-x)*c)/ll for ll in np.arange(1,llmax)]) + x*c + c**2

def pa(eb,x,c):
    
    conditions = solve_conditions(eb,x,c)
    sd = conditions[0]
    lambda_ = conditions[1]
    srav = conditions[2]

    return sum([utils.crl(ll,eb,lambda_,(1-x)*c,srav,qq,x*c,sd,lp)/ll for ll in np.arange(1,llmax)]
        ) + x*c + ((1-x)*c)**2*(1 - (5/8)*srav**2) + 2*x*(1-x)*c**2*(1 + (5/4)*srav*sd) + (x*c)**2*(1 - (5/8)*sd**2)


for eb in np.linspace(0.01,4,10):
    """ this iteration resolves x_isotropic, c_isotropic, x_anisotropic, c_anisotropic 
    for coexistent phases states """
    def equations(p) :
        """ Coexistence conditions:

        chemical potential mu_i(c_i) = mu_a(c_a)
        osmotic pressure P_i(c_i) = P_a(c_a)
        """
        xa, ci, ca = p
        return (muri(eb,xi,ci) - mura(eb, xa, ca), mudi(xi,ci) - muda(eb,xa,ca), pi(xi,ci) - pa(eb,xa,ca))

    solv2 = fsolve(equations, (xas,cis,cas))
    xan=solv2[0].real
    cin=solv2[1].real
    can=solv2[2].real
    print("Solved coexistence for eb = "+str(eb)+":\n ci = "+str(cin)+", xa = "+str(xan)+", ca = "+str(can))

