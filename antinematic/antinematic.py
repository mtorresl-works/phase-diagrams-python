import numpy as np
import os

from utils import roddisk_utils as utils
import config

# Data folder inside target
target_dir = config.data_dir(__file__)
os.makedirs(target_dir, exist_ok=True)

res = []

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

sravs = -0.4
sds = 0.8
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
    
    conditions = utils.solve_conditions(eb,xx,cc,zz,qq,lp,llmax,lambdas, sravs, sds)
    sdn,sds = conditions[0],conditions[0]
    lambdan,lambdas = conditions[1],conditions[1]
    sravn,sravs = conditions[2],conditions[2]
    
    print(eb, "  ", sravn, "   ", sdn, " ", lambdan)
    
    
    """ final polymer length distribution """
    
    def rlf(ll) :
        return utils.crl(ll,eb,lambdan,rr0,sravn,qq,rd0,sdn,lp)
    
    
    """ write polymer distribution to file """
    resp = []
    for ll in np.arange(1,llmax) :
        resp.append([ll,rlf(ll).real])
        np.savetxt(target_dir+"dis_at_eb_"+str(round(eb,1))+"_.txt",resp)
    
    
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
    
    res.append([eb, m1, var, sravn, sdn, sw, maxprob.real])
    
    """ write to file """
    np.savetxt(target_dir+"res.txt",res)