# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 13:06:20 2024

@author: Ahmedtaman
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 19:55:47 2024

@author: Ahmedtaman
"""
import pandas as pd
import numpy as np
from datetime import datetime, date,time
import os
import datetime as dt









def weekend (radiologist,roasterradio,ris_point):
    consappend=pd.DataFrame()
    assisappend=pd.DataFrame()
    weekendadmission=["O","I"]

    print(len(roasterradio))
    print(len(str(roasterradio.iloc[0, 6])))
    xx=roasterradio['Weekend Reporting   (Friday-Saturday)'].reset_index()
    leng=xx.iloc[0:0]
    #print(len(roasterradio.iloc[0, 9]))
   
        
    roasterradio['Weekend Reporting   (Friday-Saturday)'] = roasterradio['Weekend Reporting   (Friday-Saturday)'].astype(str)
    wdlist=roasterradio['Weekend Reporting   (Friday-Saturday)'].str.split('     ',expand=True).stack().str.strip().reset_index(drop=True) 
    wdlist=wdlist[wdlist!='___']
    wdlist=wdlist[wdlist!='']
    
    wdlist=wdlist[wdlist!='_____']
    
    if((len(str(roasterradio.iloc[0, 6]))>5)):
     for elment in wdlist:
       print((elment.split(',')[0].strip(),'%d/%m/%Y'))
       print(elment.split(',')[1].strip())
       print(radiologist)
       
       if(datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date()>datetime.strptime('3/10/24', '%m/%d/%y').date()):
           if (elment.split(',')[1].strip())=="X-Ray":
               cons=ris_point.loc[((ris_point['SIGNER_Name2']==radiologist)&( (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())|((ris_point['PROCEDURE_END'].dt.date==(datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date()- pd.DateOffset(days=1)).date())&(ris_point['PROCEDURE_END'].dt.time >time( hour=14,minute=59,second=59))))&(ris_point['SECTION_CODE']=='X-Ray'))]
               consappend=pd.concat([consappend,cons],ignore_index=True, sort=False)
               print(datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())
              
               assis=ris_point.loc[((ris_point['Assistant']==radiologist)&(ris_point['SIGNER_Name2']!=radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())&(ris_point['SECTION_CODE']==elment.split(',')[1].strip())&(ris_point['ADMISSION_TYPE'].isin(weekendadmission)))]
               assisappend=pd.concat([assisappend,assis],ignore_index=True, sort=False)
           else :
               cons=ris_point.loc[((ris_point['SIGNER_Name2']==radiologist)&( (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())|((ris_point['PROCEDURE_END'].dt.date==(datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date()- pd.DateOffset(days=1)).date())&(ris_point['PROCEDURE_END'].dt.time >time( hour=14,minute=59,second=59))))&(ris_point['SECTION_CODE']==elment.split(',')[1].strip())&(ris_point['ADMISSION_TYPE'].isin(weekendadmission)))]
               consappend=pd.concat([consappend,cons],ignore_index=True, sort=False)
              
               assis=ris_point.loc[((ris_point['Assistant']==radiologist)&(ris_point['SIGNER_Name2']!=radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())&(ris_point['SECTION_CODE']==elment.split(',')[1].strip())&(ris_point['ADMISSION_TYPE'].isin(weekendadmission)))]
               assisappend=pd.concat([assisappend,assis],ignore_index=True, sort=False)
       else:
        if (elment.split(',')[1].strip())=="X-Ray":
            cons=ris_point.loc[((ris_point['SIGNER_Name2']==radiologist)&( (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())|((ris_point['PROCEDURE_END'].dt.date==(datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date()- pd.DateOffset(days=1)).date())&(ris_point['PROCEDURE_END'].dt.time >time( hour=15,minute=59,second=59))))&(ris_point['SECTION_CODE']=='X-Ray'))]
            consappend=pd.concat([consappend,cons],ignore_index=True, sort=False)
           
            assis=ris_point.loc[((ris_point['Assistant']==radiologist)&(ris_point['SIGNER_Name2']!=radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())&(ris_point['SECTION_CODE']==elment.split(',')[1].strip())&(ris_point['ADMISSION_TYPE'].isin(weekendadmission)))]
            assisappend=pd.concat([assisappend,assis],ignore_index=True, sort=False)
        else :
            cons=ris_point.loc[((ris_point['SIGNER_Name2']==radiologist)&( (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())|((ris_point['PROCEDURE_END'].dt.date==(datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date()- pd.DateOffset(days=1)).date())&(ris_point['PROCEDURE_END'].dt.time >time( hour=15,minute=59,second=59))))&(ris_point['SECTION_CODE']==elment.split(',')[1].strip())&(ris_point['ADMISSION_TYPE'].isin(weekendadmission)))]
            consappend=pd.concat([consappend,cons],ignore_index=True, sort=False)
           
            assis=ris_point.loc[((ris_point['Assistant']==radiologist)&(ris_point['SIGNER_Name2']!=radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())&(ris_point['SECTION_CODE']==elment.split(',')[1].strip())&(ris_point['ADMISSION_TYPE'].isin(weekendadmission)))]
            assisappend=pd.concat([assisappend,assis],ignore_index=True, sort=False)
           
       
       
       
     
     
     consappend['Class']='solo management'
     consappend.rename(columns={'Cons_point':'Earned_point'},inplace=True)
     consappend.rename(columns={'Cons_price':'Earned_M'},inplace=True)

     assisappend['Class']='Under Supervision'
     assisappend.rename(columns={'Assis_point':'Earned_point'},inplace=True)
     assisappend.rename(columns={'Assis_price':'Earned_M'},inplace=True)
     print(len(assisappend))
     if(len(assisappend)>0):
         allapend=pd.concat([consappend,assisappend])
     else:
         allapend=consappend
    
    
    # consappend['Class']='Consultant'
    # consappend.rename(columns={'Cons_point':'Earned_point'},inplace=True)
    # consappend.rename(columns={'Cons_price':'Earned_M'},inplace=True)
    # allapend=consappend

    
        


     allapend.drop_duplicates(inplace=True)
     allapend['day']='WeekEnd'
     return allapend



def thursday_afterhours (radiologist,roasterradio,ris_point):
    consappend=pd.DataFrame()
    assisappend=pd.DataFrame()

    print(len(roasterradio))
    print(len(str(roasterradio.iloc[0, 7])))
    xx=roasterradio['Thursday coverage'].reset_index()
    leng=xx.iloc[0:0]
    #print(len(roasterradio.iloc[0, 9]))
   
        
    roasterradio['Thursday coverage'] = roasterradio['Thursday coverage'].astype(str)
    wdlist=roasterradio['Thursday coverage'].str.split('     ',expand=True).stack().str.strip().reset_index(drop=True) 
    wdlist=wdlist[wdlist!='___']
    wdlist=wdlist[wdlist!='']
    
    wdlist=wdlist[wdlist!='_____']
    
    if((len(str(roasterradio.iloc[0, 7]))>5)):
     for elment in wdlist:
       print((elment.split(',')[0].strip(),'%d/%m/%Y'))
       print(elment.split(',')[1].strip())
       print(radiologist)
       
       if(datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date()>datetime.strptime('3/10/24', '%m/%d/%y').date()):
           ris_point.ADMISSION_TYPE.value_counts()
           cons=ris_point.loc[(ris_point['SIGNER_Name2']==radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())& (ris_point['PROCEDURE_END'].dt.time >time( hour=14,minute=59,second=59))&(ris_point['SECTION_CODE']==elment.split(',')[1].strip())&(ris_point['ADMISSION_TYPE']!='E')]
           consappend=pd.concat([consappend,cons],ignore_index=True, sort=False)
       else:
           cons=ris_point.loc[(ris_point['SIGNER_Name2']==radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())& (ris_point['PROCEDURE_END'].dt.time >time( hour=15,minute=59,second=59))&(ris_point['SECTION_CODE']==elment.split(',')[1].strip())&(ris_point['ADMISSION_TYPE']!='E')]
           consappend=pd.concat([consappend,cons],ignore_index=True, sort=False)

       
       

    
    consappend['Class']='Consultant'
    consappend.rename(columns={'Cons_point':'Earned_point'},inplace=True)
    consappend.rename(columns={'Cons_price':'Earned_M'},inplace=True)


    thursday_afterhours=consappend


    
    thursday_afterhours['day']='Thursday_afterHours'
    return thursday_afterhours



def extrashifts_assist (radiologist,roasterradio,ris_point):

    consappend=pd.DataFrame()
    assisappend=pd.DataFrame()

    print(len(roasterradio))
    print(len(str(roasterradio.iloc[0,11])))
    xx=roasterradio['Extra Shifts for  Assistant'].reset_index()
    leng=xx.iloc[0:0]
    #print(len(roasterradio.iloc[0, 9]))
   
        
    roasterradio['Extra Shifts for  Assistant'] = roasterradio['Extra Shifts for  Assistant'].astype(str)
    wdlist=roasterradio['Extra Shifts for  Assistant'].str.split('     ',expand=True).stack().str.strip().reset_index(drop=True) 
    wdlist=wdlist[wdlist!='___']
    wdlist=wdlist[wdlist!='']
    
    wdlist=wdlist[wdlist!='_____']
    
    if((len(str(roasterradio.iloc[0, 11]))>5)):
     for elment in wdlist:
       print((elment.split(',')[0].strip(),'%d/%m/%Y'))
       print(radiologist)
       
       
      
       cons=ris_point.loc[(ris_point['SIGNER_Name2']==radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())]
       consappend=pd.concat([consappend,cons],ignore_index=True, sort=False)
      
       assis=ris_point.loc[(ris_point['Assistant']==radiologist)&(ris_point['SIGNER_Name2']!=radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())]
       assisappend=pd.concat([assisappend,assis],ignore_index=True, sort=False)
    
    
    consappend['Class']='solo management'
    consappend.rename(columns={'Cons_point':'Earned_point'},inplace=True)
    consappend.rename(columns={'Cons_price':'Earned_M'},inplace=True)

    assisappend['Class']='Under Supervision'
    assisappend.rename(columns={'Assis_point':'Earned_point'},inplace=True)
    assisappend.rename(columns={'Assis_price':'Earned_M'},inplace=True)
    print(len(assisappend))
    if(len(assisappend)>0):
        allapend=pd.concat([consappend,assisappend])
    else:
        allapend=consappend


    
    allapend['day']='Extra Shifts'
    return allapend
def er_reporting (radiologist,roasterradio,ris_point):
    consappend=pd.DataFrame()
    assisappend=pd.DataFrame()

    print(len(roasterradio))
    print(len(str(roasterradio.iloc[0, 9])))
    xx=roasterradio['ER REPORTING'].reset_index()
    leng=xx.iloc[0:0]
    #print(len(roasterradio.iloc[0, 9]))
   
        
    roasterradio['ER REPORTING'] = roasterradio['ER REPORTING'].astype(str)
    wdlist=roasterradio['ER REPORTING'].str.split('     ',expand=True).stack().str.strip().reset_index(drop=True) 
    wdlist=wdlist[wdlist!='___']
    wdlist=wdlist[wdlist!='']
    
    wdlist=wdlist[wdlist!='_____']
    
    if((len(str(roasterradio.iloc[0, 9]))>5)):
     for elment in wdlist:
       print((elment.split(',')[0].strip(),'%d/%m/%Y'))
       print(radiologist)
       
       if(datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date()>datetime.strptime('3/10/24', '%m/%d/%y').date()):
           cons=ris_point.loc[(ris_point['SIGNER_Name2']==radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())& (ris_point['PROCEDURE_END'].dt.time >time( hour=14,minute=59,second=59))&(ris_point['ADMISSION_TYPE']=='E')&(ris_point['Hospital_x'].isin(["PMAH","KFMC"]))]
           consappend=pd.concat([consappend,cons],ignore_index=True, sort=False)
       else:
           cons=ris_point.loc[(ris_point['SIGNER_Name2']==radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split(',')[0].strip(),'%d/%m/%Y').date())& (ris_point['PROCEDURE_END'].dt.time >time( hour=15,minute=59,second=59))&(ris_point['ADMISSION_TYPE']=='E')&(ris_point['Hospital_x'].isin(["PMAH","KFMC"]))]
           consappend=pd.concat([consappend,cons],ignore_index=True, sort=False)

      
       
      
    
    
    consappend['Class']='solo management'
    consappend.rename(columns={'Cons_point':'Earned_point'},inplace=True)
    consappend.rename(columns={'Cons_price':'Earned_M'},inplace=True)
    allapend=consappend


    
    allapend['day']='ER REPORTING'
    return allapend