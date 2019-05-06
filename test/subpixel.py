# -*- coding: utf-8 -*-



#import geoimread
import numpy as np
from skimage.transform import resize 
from templatematch import templatematch


import unittest


class test_templatematch(unittest.TestCase):
    def test_subpixel(self):

        A = np.random.normal(size=[100,30000])
        B = resize(A,[100,30010],anti_aliasing=True,mode='reflect')
        r = templatematch(A, B, TemplateWidth=64, SearchWidth=64 + 32)
        du = r.du.ravel()
        pu = r.pu.ravel()
        
        ix = ~np.isnan(du)
        du = du[ix]
        pu = pu[ix]
        
        predicted = pu*(B.shape[1]-A.shape[1])/A.shape[1]
        
        residual = du - predicted
        
        #from matplotlib import pyplot as plt
        #plt.plot(predicted % 1,residual,'.')  # try to minimize systematic errors
        
        quality = np.nanstd(residual)
        self.assertLess(quality,0.12,'Poor sub-pixel performance: {}.'.format(quality))
        
        bias = np.nanmedian(residual)
        self.assertLess(bias,0.01,'Biased sub-pixel offset: {}.'.format(bias))
        
        phase = (predicted % 1)*2*np.pi
        X = np.column_stack((np.cos(phase),np.sin(phase)))
        p = np.linalg.lstsq(X,residual)[0]
        hamp = np.sqrt(p[0]**2+p[1]**2)
        self.assertLess(hamp,0.1,'Large systematic bias for sub-pixel offset: {}.'.format(hamp))


if __name__ == "__main__":
    unittest.main()