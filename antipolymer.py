import matplotlib.pyplot as plt
import numpy as np
import cmath, math
from scipy.special import dawsn
from scipy.optimize import fsolve
import os

import antip_utils as utils

res = []
os.makedirs("target/data", exist_ok=True)

""" overall concentration and disc mole fraction """

cc = 4
xx = 0.5

""" convert to overall monomer and disc concentrations """

rr0 = cc*(1 - xx)
rd0 = cc*xx

""" excluded volume rations """

qq = 1
zz = 1


""" starting values for nematic order parameters and normalization 
constant, this is the tricky bit, they need to be reasonably close to 
the real values that are a priori unknown """

sravs = 0.8
sds = -0.4
lambdas = -3


""" cut-off for polymerization degree, note: this value should be 
large enough to make sure the polymer distribution remains close to 
zero at llmax, if not llmax should be increased which slows down the 
computation """

llmax = 50

""" persistence length """

lp = 5


""" loop over temperature """


for eb in np.arange(5,1,-0.2) :
    
    """ this iteration resolves S_polymer, S_disc and normalization 
    factor lambda """
    
    # df = 100
    
    # while df > 1 :
        
    #     def equations(p) :
    #         """ Normalization conditions:
    #         SUM(rho_rl) for every l = rho_r0
    #         SUM(S_rl*rho_rl) for every l = S_r average
            
    #          """
    #         lambda_, srav = p
    #         return (sum([antip_utils.crl(ll,eb,lambda_,rr0,srav,qq,rd0, sds ,lp) for ll in np.arange(1,llmax)])-rr0,  
    #             sum([antip_utils.csrl(ll, rr0,srav,qq,rd0, sds ,lp)*antip_utils.crl(ll,eb,lambda_,rr0,srav,qq,rd0, sds ,lp)
    #             for ll in np.arange(1,llmax)])*rr0**-1-srav)
        
    #     # solv1
    #     solv1 = fsolve(equations, (lambdas, sravs))
    #     lambdan = solv1[0].real
    #     sravn = solv1[1].real

    #     def real_sdeq(x1):
    #         # converts a real-valued vector of size 2 to a complex-valued vector of size 1
    #         # outputs a real-valued vector of size 2
    #         x = x1[0]+1j*x1[1]
    #         actual_f = antip_utils.csd(zz,rd0,x,qq,rr0,sravn) - x
    #         return [np.real(actual_f),np.imag(actual_f)]
        
    #     # solv2
    #     sdn = fsolve(real_sdeq, [sds, 0])[0]
        
    #     df = 10**5*max([abs(sdn - sds), abs(sravn - sravs), abs(lambdan - lambdas)])
        
    #     print(df)
        
    #     sds = sdn
        
    #     lambdas = lambdan
        
    #     sravs = sravn
    conditions = utils.solve_conditions(eb,xx,cc,zz,qq,lp,llmax,lambdas, sravs, sds)
    sdn,sds = conditions[0],conditions[0]
    lambdan,lambdas = conditions[1],conditions[1]
    sravn,sravs = conditions[2],conditions[2]

    print("Updated starting values: ",lambdas, "  ",sravs, "  ",sds)
    
    print(lp, "  ", sravn, "   ", sdn, " ", lambdan)
    
    
    """ final polymer length distribution """
    
    def rlf(ll) :
        return utils.crl(ll,eb,lambdan,rr0,sravn,qq,rd0,sdn,lp).real
    
    
    """ write polymer distribution to file """
    resp = []
    for ll in np.arange(1,llmax) :
        resp.append([ll,rlf(ll)])
        np.savetxt("target/data/eb_"+str(eb)+"_dis.txt",resp)
    
    
    """ compute maximum probability for polymer length """
    
    listrlf = [rlf(ii) for ii in np.arange(1,llmax)]
    
    maxprob=max(listrlf)
    
    print(maxprob)
    
    """ polymer length dispersion """
    
    m1 = (sum([rlf(ii) for ii in np.arange(1,llmax)])/
        sum([rlf(ii)/ii for ii in np.arange(1,llmax)]))
    
    m2 = (sum([rlf(ii)*ii for ii in np.arange(1,llmax)])/
        sum([rlf(ii)/ii for ii in np.arange(1,llmax)]))
    
    var = ((m2 - m1**2)/m1**2)**(1/2)
    
    """ number density averaged nematic order parameter """
    
    sw = (sum([utils.csrl(ll, rr0,sravn,qq,rd0,sdn,lp)*rlf(ii)/ii for ii in np.arange(1,llmax)])/
        sum([rlf(ii)/ii for ii in np.arange(1,llmax)])).real
    
    """ append various stuff we want to measure to list "res" """
    
    res.append([eb, m1, var, sravn, sdn, sw, maxprob])
    
    """ write to file """
    np.savetxt("target/data/res.txt",res)