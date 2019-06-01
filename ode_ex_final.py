# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 13:01:12 2016
@author: Madeline
"""
import scipy as sp, matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np

#define constants
A = np.pi*0.013**2 + 2*np.pi*0.013*0.3
D = 0.026
M = 2700*np.pi*((0.013**2)*0.3 - (0.004**2)*0.083)
C = 900
alpha = -1.32*A*(D**(-0.25))/(M*C)
To = 24.75
sb = 5.67*10**(-8) #Stefan-Boltzmann constant

##load data
input_file = '/home/madeline/Desktop/Physics-type things/cooling.csv'
t, Tr, Tl, Tp = np.loadtxt(input_file, delimiter=',',unpack=True)
dT = 0.2
T0 = Tr[0]
em = 0.6

def F(T, t):
    return -1.32*A*((T-To)**1.25)/((D**0.25)*M*C) + em*sb*A*((To+273.15)**4 - (T+273.15)**4)/(M*C)
    
y_num = odeint(F, T0, 60*t)
  
plt.errorbar(t, Tr, yerr=dT, fmt='.', color='g',label="Rough")
#plt.plot(t,)
    
#def residuals(fit_parameters, x_data, y_data, y_errors):
#	return (y_data - (fit_parameters, x_data)) / y_errors
###
#p = lmfit.Parameters()
####           (Name,   Value,   Vary,   Min,   Max,   Expr)
#p.add_many(('em', 10.0,      True,   None,  None,  None))
##
#fit_results = lmfit.minimize(residuals, p, args=(t, Tr, dT))
#
#num_points = 1000
#x_fit = np.linspace(0.0, 100.0, num=num_points)
#y_fit = model(p, x_fit)
#
##plotting the two solutions
#plt.plot(t,model,label="both")
plt.title('Analysis Part 2')
plt.errorbar(t, Tr, yerr=dT, fmt='.', color='g',label="Rough")
plt.legend(loc='upper right',prop={'size':10})
plt.xlabel('Time (min)')
plt.ylabel('Temperature (C)')
#plt.xlim(0,100)
#plt.show()
