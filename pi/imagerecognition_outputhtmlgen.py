# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 02:37:23 2016

@author: MichaelHoeh

Idea:
- load files with computed height and fitted parameters
- create a html file that is auto-refreshing, so that in browser 
"""

import scipy as sp
import numpy as np
import time

fittedparams = np.loadtxt('curve_fittedparams.txt', delimiter=';')
heightmm = np.loadtxt('curve_heightmm.txt', delimiter=';')

refreshtime = 2	# in s

# HTML export
for i in range(len(fittedparams)):
    
    html_str1 = """
    <!DOCTYPE html>
    <html><head>
    <meta http-equiv="refresh" content="""+'"'+str(refreshtime)+'"'+""">
    <title> </title>

    <table style="width:100%">
    <tr>
    <td>
    sample = """+str(i)+"""
    </td>    
    </tr>
    <tr>
    <td>
    <img src=curve_"""+str(i)+""".png alt="Outdoor Scene" height="50%" width="50%"> 
    </td>    
    </tr>
    <tr>
    <td>
    height = """+str(np.round(heightmm[i],2))+""" mm
    </td>    
    </tr>
    <tr>
    <td>
    """
    if fittedparams[i,1]<0:
        html_str2 = """ bad 
                        <img src=pic_redcross.jpeg alt="Outdoor Scene" height="10%" width="10%"> 
                        </tr></td>"""
    else:
        html_str2 = """ good
                        <img src=pic_greenarrow.jpeg alt="Outdoor Scene" height="10%" width="10%"> 
                        </tr></td>"""
    html_str3 ="""
    </table>
    </head><body></body></html>
    """    
    
    html_str = html_str1 + html_str2 + html_str3
         
    time.sleep(refreshtime)

    Html_file= open("web_output.html","w")
    Html_file.write(html_str)
    Html_file.close()