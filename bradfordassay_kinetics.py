# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 11:52:54 2015

@author: madeline
"""
import numpy as np
import matplotlib.pyplot as plt
import lmfit

def model(parameters, xi):
    p1 = parameters['p1'].value
    p2 = parameters['p2'].value
    return p1*xi + p2

def residuals(fit_parameters, x_data, y_data, y_errors):
    return (y_data - model(fit_parameters, x_data))/y_errors

input_file = '/home/madeline/Desktop/BIOC 301/Enzyme Kinetics/csv files for enzyme kinetics/bradford_kinetics.csv'
x, y = np.loadtxt(input_file, delimiter=',', unpack=True, skiprows=0)
y_err = 1

p = lmfit.Parameters()
#(Name, Value, Vary, Min, Max, Expr)
p.add_many(('p1', 1.0, True, None, None, None),
           ('p2', 1.0, True, None, None, None))
fit_results = lmfit.minimize(residuals, p, args=(x, y, y_err))
x_fit = np.linspace(-2,12,num=1000)
y_fit = model(p, x_fit)
# Output Results
print '\nFit Parameters:'
print 'p1 = %.6f, Standard Error in p1 = %.6f' % (p['p1'].value, p['p1'].stderr)
print 'p2 = %.6f, Standard Error in p2 = %.6f' % (p['p2'].value, p['p2'].stderr)
print '\n\'Goodness\' of Fit:'
print 'Chi^2 = ', fit_results.chisqr
print 'Reduced Chi^2 = ', fit_results.redchi

# Plot the data and fitted model
plt.scatter(x, y)
plt.plot(x_fit, y_fit, 'r-')
plt.xlabel('Mass of BSA (ug)')
plt.ylabel('Absorbance')
plt.title('BSA Standard Curve')
plt.xlim(-1,12)
plt.show()