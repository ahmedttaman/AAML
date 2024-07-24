# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 19:55:47 2024

@author: Ahmedtaman
"""
import pandas as pd
import numpy as np
from datetime import datetime, date
import os
import datetime as dt









def weekend (radiologist,roasterradio,ris_point):
    consappend=pd.DataFrame()
    assisappend=pd.DataFrame()

    print(len(roasterradio))
    print(len(str(roasterradio.iloc[0, 9])))
    xx=roasterradio['Weekend Reporting   (Friday-Saturday)'].reset_index()
    leng=xx.iloc[0:0]
    #print(len(roasterradio.iloc[0, 9]))
   
        
    roasterradio['Weekend Reporting   (Friday-Saturday)'] = roasterradio['Weekend Reporting   (Friday-Saturday)'].astype(str)
    wdlist=roasterradio['Weekend Reporting   (Friday-Saturday)'].str.split('     ',expand=True).stack().str.strip().reset_index(drop=True) 
    wdlist=wdlist[wdlist!='___']
    wdlist=wdlist[wdlist!='']
    
    wdlist=wdlist[wdlist!='_____']
    
    if((len(str(roasterradio.iloc[0, 9]))>5)):
     for elment in wdlist:
       print((elment.split(',')[0].strip(),'%d/%m/%Y'))
       print(elment.split(',')[1].strip())
       print(radiologist)
      
       cons=ris_point.loc[(ris_point['SIGNER_Name2']==radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())&(ris_point['SECTION_CODE']==elment.split(',')[1].strip())]
       consappend=pd.concat([consappend,cons],ignore_index=True, sort=False)
      
       assis=ris_point.loc[(ris_point['Assistant']==radiologist)&(ris_point['SIGNER_Name2']!=radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())&(ris_point['SECTION_CODE']==elment.split(',')[1].strip())]
       assisappend=pd.concat([assisappend,assis],ignore_index=True, sort=False)
    
    
    consappend['Class']='Consultant'
    consappend.rename(columns={'Cons_point':'Earned_point'},inplace=True)
    consappend.rename(columns={'Cons_price':'Earned_M'},inplace=True)

    assisappend['Class']='Assistant'
    assisappend.rename(columns={'Assis_point':'Earned_point'},inplace=True)
    assisappend.rename(columns={'Assis_price':'Earned_M'},inplace=True)
    print(len(assisappend))
    if(len(assisappend)>0):
        allapend=pd.concat([consappend,assisappend])
    else:
        allapend=consappend


    
    allapend['day']='WeekEnd'
    return allapend