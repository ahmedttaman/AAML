# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 20:07:29 2024

@author: Ahmedtaman
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 13:51:30 2024

@author: Ahmedtaman
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
import os
import datetime as dt
from Point_functions import *




#############################master Tables

import calendar

def get_weekends(year, month):
    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    month_matrix = cal.monthdatescalendar(year, month)
    
    weekends = []
    for week in month_matrix:
        for day in week:
            if day.weekday() == calendar.FRIDAY or day.weekday() == calendar.SATURDAY:
                weekends.append(day)
    
    return weekends
weekend_dates=get_weekends(2023, 12)


import python_calamine
from python_calamine import CalamineWorkbook

workbook = CalamineWorkbook.from_path(r"D:\AAML\CCC\Hospitals data\ph_kf_yam_ar_dw_zu_mj_19 May, 2024.xlsx")
workbook.sheet_names
# ["Sheet1", "Sheet2"]

recs: list[list]=workbook.get_sheet_by_name("ِAll").to_python()
ris1 = pd.DataFrame.from_records(recs)


new_header = ris1.iloc[0] #grab the first row for the header
ris1 = ris1[1:] #take the data less the header row
ris1.columns = new_header
ris2=ris1.head()




#ris = pd.read_csv(r"D:\AAML\CCC\Hospitals data\ph_kf_yam_ar_dw_zu_mj19 Feb, 2024.csv")
ris1 = pd.read_excel(r"D:\AAML\CCC\Hospitals data\ph_kf_yam_ar_dw_zu_mj_22 May, 2024.xlsx")
invoice = pd.read_excel(r"D:\AAML\CCC\Hospitals data\Radiologist Productivity\Invoices\Reported Procedures - February 2024_PPP Radiology C2_AT.xlsx",sheet_name="Accessions")
#invoice = pd.read_excel(r"D:\AAML\CCC\Hospitals data\Radiologist Productivity\Invoices\Reported Procedures - January 2024_PPP Radiology C2_AT.xlsx",sheet_name="Accessions")



# procduremapping_points = pd.read_excel(r"D:\AAML\CCC\Hospitals data\Radiologist Productivity\NPHIES Points System modified 21-4-2024.xlsx",sheet_name="KFMC to NICIP to NPHIES Mapping")

# procduremapping_points.info()

point_map = pd.read_excel(r"D:\AAML\CCC\Hospitals data\Radiologist Productivity\NPHIES Points System modified 21-4-2024.xlsx",sheet_name="Sheet1")

Reading_price = pd.read_excel(r"D:\AAML\CCC\Hospitals data\Radiologist Productivity\Reading Fee_ Jan.24 Invoice v1.xlsx",sheet_name="Reading_Master")


#roaster = pd.read_excel(r"D:\AAML\CCC\Hospitals data\Radiologist Productivity\Rota\Dec.2023-Productivity-FINAL.xlsx")

#roaster = pd.read_excel(r"D:\AAML\CCC\Hospitals data\Radiologist Productivity\Rota\JAN productivity-Final.xlsx")

roaster = pd.read_excel(r"D:\AAML\CCC\Hospitals data\Radiologist Productivity\Rota\FEB 2024 PRODUCTIVITY-Final.xlsx")
# roaster.columns=roaster.iloc[0]
# roaster=roaster[1:]



roaster.info()
roaster.replace('____',np.nan ,inplace=True)
roaster.replace('__',np.nan,inplace=True)
roaster = roaster.dropna(subset=['ID No.'])
roaster['TOTAL ACTIVITIES']=roaster['TOTAL ACTIVITIES'].apply(lambda x: x if x >0 else 0)

roaster['workhours']=(roaster['No. of Workdays']*8)-roaster['TOTAL ACTIVITIES']
Radiolgistnames = pd.read_excel(r"D:\AAML\CCC\Hospitals data\ALL RADIOLOGOSITS MAPPED NAMES 15 May 24.xlsx")
roaster2=pd.merge(roaster, Radiolgistnames,left_on=roaster['Name'].str.upper().apply(lambda x: x.replace(' ','')),right_on=Radiolgistnames['Final unified list'].astype(str).str.upper().apply(lambda x: x.replace(' ','')),how="left")

roaster2=roaster2.iloc[: , :-9]
educationhrs=56
northconsultant=['Dr. Fawzy Mohamed','Dr. Jaafar Abdul Rahman','Dr. Ahmed Ibrahim Abdel Aal','Dr. Ehab Ali Ahmed']
eduocationnormalize=.675
monthworkdays=max(roaster2['No. of Workdays'])
roaster2.loc[roaster2['Category']=="Consultant",'educations_hrs']=(roaster2['No. of Workdays']*educationhrs)/monthworkdays
roaster2.loc[roaster2['Admin']==1,'admin_hrs']=roaster2['No. of Workdays']*8*.2
roaster2.fillna(0,inplace=True)
roaster2.loc[roaster2['Name'].isin(northconsultant),'educations_hrs']=educationhrs/1.8
roaster2['net_report_hrs']=roaster2.workhours-roaster2.educations_hrs -roaster2.admin_hrs

roaster2['required_report_point']=roaster2.net_report_hrs*4
roaster2['required_eductio_point']=roaster2.educations_hrs *4*eduocationnormalize
roaster2['total_required_point']=roaster2.required_report_point +roaster2.required_eductio_point
roaster2.fillna(0)
roaster2=roaster2.drop_duplicates(['Name'])































ris=ris1.copy()
invtest2=ris1.loc[ris1['PROCEDURE_KEY']=="PRCA000000193299"]
ris.info()
outprocedur=['XR INTRAOPERATIVE','XR Dental Panoramic','MRI Contrast Material','RAD OUTSIDE CD FOR REVIEW']
ris=ris.loc[~ris['PROCEDURE_NAME'].isin(outprocedur)]

ris['PROCEDURE_END']=pd.to_datetime(ris['PROCEDURE_END'],errors="coerce")
ris['REPORT_VERIFICATION_DATE']=pd.to_datetime(ris['REPORT_VERIFICATION_DATE'],errors="coerce")

startstr='12/01/23 00:00:01'
start = datetime.strptime(startstr, '%m/%d/%y %H:%M:%S')
endstr='2/29/24 23:59:59'
end = datetime.strptime(endstr, '%m/%d/%y %H:%M:%S')
ris.loc[ris['Hospital']=='Al Artaweyyah','PROCEDURE_KEY']=ris['PROCEDURE_KEY'].str.replace('.0','')

ris_dec=ris.loc[ris['PROCEDURE_KEY'].isin(invoice['Acc_hospital'])]
invtest=invoice.loc[~invoice['Acc_hospital'].isin(ris['PROCEDURE_KEY'])].dropna()
ris['Hospital'].value_counts()




# ris_dec=ris.loc[(ris['PROCEDURE_END'].between(start,end))]
#ris_dec=ris.loc[(ris['PROCEDURE_END'].between(start,end))&(ris['REPORT_VERIFICATION_DATE'].between(start,end))]

ris_dec.loc[(ris_dec['SIGNER_Name2']=='AHMAD ADNAN MOHAMMED ALDEREIHIM'),'SIGNER_Name2']='AHMED IBRAHIM ALDRAIHEM'

ris_dec=ris_dec.iloc[:,0:70]

non_clinc_hours=0
Baseline_Points_hour=4
Baseline_Points_hour_xr=30
Baseline_Points_hour_mamo=20
normlization_mamo=5
normlization_xr=7.5
normalized_modality=['X-Ray','Mamo']
peditric_factor=.8
er_in_factor=.625
er_list=['Emergency',"E","InPatient","I"]

ris_dec["PROCEDURE_NAME_Nicp2"]=ris_dec["PROCEDURE_NAME_Nicp"].astype(str)

ris_dec["PROCEDURE_NAME_Nicp2"]=ris_dec["PROCEDURE_NAME_Nicp2"].str.upper()
ris_dec["PROCEDURE_NAME_Nicp2"]=ris_dec["PROCEDURE_NAME_Nicp2"].apply(lambda x: x.replace(' ','') )

point_map["NICIP Examination Name2"]=point_map["NICIP Examination Name"].astype(str).str.upper()
point_map["NICIP Examination Name2"]=point_map["NICIP Examination Name2"].apply(lambda x: x.replace(' ','') )

point_map=point_map.drop_duplicates(['NICIP Examination Name2'],keep="first")



ris_point=pd.merge(ris_dec, point_map,left_on=['PROCEDURE_NAME_Nicp2'],right_on=['NICIP Examination Name2']  ,how="left")
# ris_point['scanday']=ris_point['PROCEDURE_END'].dt.dayofweek
# ris_point['reportday']=ris_point['REPORT_VERIFICATION_DATE'].dt.dayofwee
ris_point['scan_weekday']=""
ris_point.loc[((ris_point['PROCEDURE_END'].dt.dayofweek==3)&(ris_point['PROCEDURE_END'].dt.time >= pd.to_datetime('16:30').time())),'scan_weekday']='Scanweekend'
ris_point.loc[((ris_point['PROCEDURE_END'].dt.dayofweek>3)&(ris_point['PROCEDURE_END'].dt.dayofweek<=5)),'scan_weekday']='Scanweekend'
ris_point['report_weekday']=""
ris_point.loc[((ris_point['REPORT_VERIFICATION_DATE'].dt.dayofweek==3)&(ris_point['REPORT_VERIFICATION_DATE'].dt.time >= pd.to_datetime('16:30').time())),'report_weekday']='Reportweekend'
ris_point.loc[((ris_point['REPORT_VERIFICATION_DATE'].dt.dayofweek>3)&(ris_point['REPORT_VERIFICATION_DATE'].dt.dayofweek<=5)),'report_weekday']='Reportweekend'
ris_point.loc[(ris_point['scan_weekday']=='Scanweekend')&(ris_point['report_weekday']=='Reportweekend'),'Weekend']=1


ris_point['scan_Bshift']=""
ris_point.loc[((ris_point['PROCEDURE_END'].dt.time >= pd.to_datetime('16:00').time())|(ris_point['PROCEDURE_END'].dt.time <= pd.to_datetime('7:00').time())),'scan_Bshift']='Scan_Bshift'
ris_point.loc[((ris_point['REPORT_VERIFICATION_DATE'].dt.time >= pd.to_datetime('16:00').time())|(ris_point['REPORT_VERIFICATION_DATE'].dt.time <= pd.to_datetime('7:00').time())),'report_Bshift']='Report_Bshift'
ris_point['TAT']=ris_point['REPORT_VERIFICATION_DATE']-ris_point['PROCEDURE_END']


filtered_df = ris_point.loc[(ris_point['PROCEDURE_END'].dt.weekday >= 3) & (ris_point['PROCEDURE_END'].dt.weekday <= 5) &((ris_point['PROCEDURE_END'].dt.weekday == 5) | (ris_point['PROCEDURE_END'].dt.time >= pd.to_datetime('16:30').time()))]

ris_point.info()

# def calcpoint():
#     if ris_dec['Age']<=14:
#         ris_point['point']=Baseline_Points_hour/(ris_point['OPD 2024']*peditric_factor)
#     if ris_dec['ADMISSION_TYPE'].isin('Emergency',"E","InPatient","I"):
#         ris_point['point']=Baseline_Points_hour/(ris_point['OPD 2024']*er_in_factor)
#     return ris_point['point']
    
ris_point['point']=0
# ER & INPATIENT facor
ris_point.loc[(ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"])&(ris_point['SECTION_CODE'].str not in normalized_modality)),'point']=Baseline_Points_hour/(ris_point['OPD 2024']*er_in_factor)
ris_point.loc[(ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"])&(ris_point['SECTION_CODE']=="X-Ray")),'point']=(Baseline_Points_hour_xr/(ris_point['OPD 2024']*er_in_factor))/normlization_xr
ris_point.loc[(ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"])&(ris_point['SECTION_CODE']=="Mamo")),'point']=(Baseline_Points_hour_mamo/(ris_point['OPD 2024']*er_in_factor))/normlization_mamo

# # PED ER & INPATIENT
# ris_point.loc[(ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"])&(ris_point['SECTION_CODE'].str not in normalized_modality)&(ris_point['Age']<=14)),'point']=Baseline_Points_hour/(ris_point['OPD 2024']*peditric_factor*er_in_factor)
# ris_point.loc[(ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"])&(ris_point['SECTION_CODE']=="X-Ray")&(ris_point['Age']<=14)),'point']=(Baseline_Points_hour_xr/(ris_point['OPD 2024']*peditric_factor*er_in_factor))/normlization_xr
# ris_point.loc[(ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"])&(ris_point['SECTION_CODE']=="Mamo")&(ris_point['Age']<=14)),'point']=(Baseline_Points_hour_mamo /(ris_point['OPD 2024']*peditric_factor*er_in_factor))/normlization_mamo





# Out patient
ris_point.loc[(~ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"])&(ris_point['SECTION_CODE'].str not in normalized_modality)&(ris_point['Age']>14)),'point']=Baseline_Points_hour/(ris_point['OPD 2024'])
ris_point.loc[(~ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"])&(ris_point['SECTION_CODE']=="X-Ray")&(ris_point['Age']>14)),'point']=(Baseline_Points_hour_xr/(ris_point['OPD 2024']))/normlization_xr
ris_point.loc[(~ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"])&(ris_point['SECTION_CODE']=="Mamo")&(ris_point['Age']>14)),'point']=(Baseline_Points_hour_mamo /(ris_point['OPD 2024']))/normlization_mamo



# PED OPD
ris_point.loc[(~ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"])&(ris_point['SECTION_CODE'].str not in normalized_modality)&(ris_point['Age']<=14)),'point']=Baseline_Points_hour/(ris_point['OPD 2024']*peditric_factor)
ris_point.loc[(~ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"])&(ris_point['SECTION_CODE']=="X-Ray")&(ris_point['Age']<=14)),'point']=(Baseline_Points_hour_xr/(ris_point['OPD 2024']*peditric_factor))/normlization_xr
ris_point.loc[(~ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"])&(ris_point['SECTION_CODE']=="Mamo")&(ris_point['Age']<=14)),'point']=(Baseline_Points_hour_mamo/(ris_point['OPD 2024']*peditric_factor))/normlization_mamo

ris_point.loc[ ((ris_point['SIGNER_Name2']==ris_point['Assistant'])|(ris_point['Assistant'].astype(str)=='nan')),'Cons_point']=ris_point['point']
ris_point.loc[ ((ris_point['SIGNER_Name2']!=ris_point['Assistant'])&(ris_point['Assistant'].astype(str)!='nan')),'Cons_point']=ris_point['point']*.6
ris_point.loc[ ((ris_point['SIGNER_Name2']!=ris_point['Assistant'])&(ris_point['Assistant'].astype(str)!='nan')),'Assis_point']=ris_point['point']*.4
ris_point.loc[ris_point['Hospital']=='Al Artaweyyah','Hospital']='Al Artaweyah'
ris_point.loc[ris_point['Hospital']=='Al Majmaah','Hospital']='Al Majmah'


ris_point['Hospital_Proc']=ris_point['Hospital']+"_"+ris_point['PROCEDURE_CODE']

Reading_price['Hospital_Proc']=Reading_price['Hospital']+"_"+Reading_price['Procedure ID']
Reading_price.drop_duplicates(['Hospital_Proc'],inplace=True)
Reading_price['Old Reading Price']=Reading_price['Reading Price']
Reading_price['Reading Price']=Reading_price['Old Reading Price']*.9
ris_point=pd.merge(ris_point,Reading_price,on='Hospital_Proc',how='left')

ris_point.loc[ ((ris_point['SIGNER_Name2']==ris_point['Assistant'])|(ris_point['Assistant'].astype(str)=='nan')),'Cons_price']=ris_point['Reading Price']
ris_point.loc[ ((ris_point['SIGNER_Name2']!=ris_point['Assistant'])&(ris_point['Assistant'].astype(str)!='nan')),'Cons_price']=ris_point['Reading Price']*.6
ris_point.loc[ ((ris_point['SIGNER_Name2']!=ris_point['Assistant'])&(ris_point['Assistant'].astype(str)!='nan')),'Assis_price']=ris_point['Reading Price']*.4


#ris_point['point']=ris_point.point.astype(float).round(1) 





# ris_point.loc[ris_point['ADMISSION_TYPE'].isin(['Emergency',"E"]),'WTime']=ris_point['READ_DATE']-ris_point['PROCEDURE_END']
# ris_point.loc[~ris_point['ADMISSION_TYPE'].isin(['Emergency',"E"]),'WTime']=ris_point['REPORT_VERIFICATION_DATE']-ris_point['PROCEDURE_END']


# TAT applying
# ris_point=ris_point.loc[~(ris_point['ADMISSION_TYPE'].isin(['Emergency',"E"]) & (ris_point['TAT']>"0 days 2:00:00"))]
# ris_point=ris_point.loc[~(ris_point['ADMISSION_TYPE'].isin(["InPatient","I"]) & (ris_point['TAT']>"1 days 00:00:00"))]
# ris_point=ris_point.loc[~(~ris_point['ADMISSION_TYPE'].isin(['Emergency',"E","InPatient","I"]) & (ris_point['TAT']>"2 days 00:00:00"))]









ris_point['SIGNER_Name2']=ris_point['SIGNER_Name2'].str.strip()
# ris_point.columns

# RIS_GROUP=ris_point.groupby(['NICIP Examination Name','SECTION_CODE']).agg({'Hospital_x':'count' ,'OPD 2024':'max'}).reset_index()










radiolgist_time=ris_point.groupby(['SIGNER_Name2','SECTION_CODE'])['Hospital_x'].count()  

assistant_time=ris_point.loc[ ((ris_point['SIGNER_Name2']!=ris_point['Assistant'])&(ris_point['Assistant'].astype(str)!='nan'))].groupby(['Assistant','SECTION_CODE'])['Hospital_x'].count()  
assistant_time=ris_point.groupby(['Assistant','SECTION_CODE'])['Hospital_x'].count()  

radiolgist_time.columns=['Radiologist','Modalitiy','Hospital','# Cases']
radiolgist_time=radiolgist_time.reset_index()

radioglist_list=ris_point['SIGNER_Name2'].drop_duplicates().dropna()
radioglist_list2=ris_point['Assistant'].drop_duplicates().dropna()
radioglist_list=pd.concat([radioglist_list,radioglist_list2]).drop_duplicates().dropna()


radioglist_list.index=radioglist_list[:]
radioglist_list=radioglist_list.drop(labels =['SALEM AHMED BAUONES','ALIYA IBRAHIM ALAWAJI','Dr. Salah Mohammed Alhumaid NTRP','Dr. Ahmed Alrizqi','Dr. Nouman Hassan','Dr. Faisal Alfaisal','Dr. Saleh Alreshoodi','Dr. Tariq Alotaibi','Dr. Mohammed Alsabti','Dr. Waleed Althobaity','Dr. Hamad Aljubair','Dr. Maha Alhusain','Dr. Ibrahim Alturki','Dr. Rumian Alrumian','Dr. Mohammed Alahmadi','Dr. Saud Alawad','Dr. Reem Mahmoud','Dr. Asif Dar','Dr. Amal Alsaedi','Dr. Rawan Alharbi','Dr. Fares Garad','Dr. Asma Alakeel','Dr. Mohammed Qureshi','Dr. Salem Bauones','Abrar Alduraiby','Physician','Hissah Albilali','Norah Alsadhan','Sara ALbawardy','Sara  Mohammed Alghamdi','Dr. Musab Alamri','Dr. Halia Alshehri','Dr. Massod Jamil','OR User','Dr. Mohammed Alhowaish'],errors='ignore')


allproduc=pd.DataFrame(columns=['Radiologist','Total Point','Overtime Point','Hit target Date'])

radtotalpoints=pd.DataFrame()
rad_hos_moda=pd.DataFrame()
allapend4=pd.DataFrame()



i=1
for radiologist in radioglist_list:
  print(radiologist)
  consappend=pd.DataFrame()
  assisappend=pd.DataFrame()
  roaster2.fillna(0)
  consappend=pd.DataFrame()
  assisappend=pd.DataFrame() 
  consappend2=pd.DataFrame()
  assisappend2=pd.DataFrame()
  
  roasterradio=roaster2.loc[roaster2['Name'].astype(str).str.upper().apply(lambda x: x.replace(' ',''))==radiologist.upper().replace(' ','')]
  
  # Week days
  cons2=ris_point.loc[(ris_point['SIGNER_Name2'].astype(str).str.upper().apply(lambda x: x.replace(' ',''))==radiologist.upper().replace(' ',''))]
  consappend2=pd.concat([consappend2,cons2],ignore_index=True, sort=False)
  
  assis2=ris_point.loc[(ris_point['Assistant'].astype(str).str.upper().apply(lambda x: x.replace(' ',''))==radiologist.upper().replace(' ',''))&(ris_point['SIGNER_Name2'].astype(str).str.upper().apply(lambda x: x.replace(' ',''))!=radiologist.upper().replace(' ',''))]
  assisappend2=pd.concat([assisappend2,assis2],ignore_index=True, sort=False)
  
  
  constest=ris_point.loc[(ris_point['Assistant']=='Dr. Sumaira Chauhdary')]
  ris_point['SECTION_CODE'].value_counts()
  
  
  
  ris_point.info()
  
  
  

  #print(len(roasterradio.iloc[0, 9]))
  if ((len(roasterradio)>0)):
      allapend=weekend(radiologist, roasterradio, ris_point)
      thursday=thursday_afterhours(radiologist, roasterradio, ris_point)
      er_reportinf=er_reporting(radiologist, roasterradio, ris_point)
      extra_shifts=extrashifts_assist(radiologist, roasterradio, ris_point)
      Overtime=pd.concat([allapend,thursday,er_reportinf,extra_shifts]) 


  else:
      continue
      
      
  #allapend.to_excel(r'D:\AAML\CCC\Hospitals data\Radiologist Productivity\Weekend '+radiologist+'.xlsx', sheet_name = "All", index = False) 
  
  consappend2['Class']='solo management'
  consappend2.rename(columns={'Cons_point':'Earned_point'},inplace=True)
  consappend2.rename(columns={'Cons_price':'Earned_M'},inplace=True)

  assisappend2['Class']='Under Supervision'
  assisappend2.rename(columns={'Assis_point':'Earned_point'},inplace=True)
  assisappend2.rename(columns={'Assis_price':'Earned_M'},inplace=True)

  if(len(assisappend2)>0):
       allapend2=pd.concat([consappend2,assisappend2])
  else:
       allapend2=consappend2

  allapend2['day']='WeekDay'
  allapend2.info()
  if(len(Overtime)>0):
      allapend2=allapend2.loc[~allapend2['PROCEDURE_KEY'].isin(Overtime['PROCEDURE_KEY'])]
#     merged_df = pd.merge(allapend2, allapend, on='PROCEDURE_KEY', how='left', indicator=True)

# # Filter out the rows from df1 that are not in df2
#     filtered_df = merged_df[merged_df['_merge'] == 'left_only']

# # Drop the '_merge' column
#     filtered_df = filtered_df.drop('_merge', axis=1)
#     allapend2=filtered_df
  
  
  
  
  
  
  overtime_classes=['WeekEnd','Thursday_afterHours','Extra Shifts','ER REPORTING']
  allapend3=pd.concat([Overtime,allapend2]) 
  allapend3 = allapend3.reset_index(drop=True)
  allapend3.sort_values('REPORT_VERIFICATION_DATE')
  allapend3.loc[allapend3['day']=="WeekDay",'Accu_point']=allapend3.loc[allapend3['day'] == "WeekDay", 'Earned_point'].cumsum()
  allapend3.loc[allapend3['day'].isin(overtime_classes),'Accu_M_end']=allapend3.loc[allapend3['day'] .isin(overtime_classes), 'Earned_M'].cumsum()

  allapend3.loc[allapend3['day']=="WeekDay",'Accu_M']=allapend3.loc[allapend3['day'] == "WeekDay", 'Earned_M'].cumsum()
  # allapend3['Accu_point']=allapend3['Earned_point'].cumsum()

  allapend3.loc[allapend3['Accu_point']>roasterradio ['total_required_point'].sum(),'Accu_M_day']=allapend3.loc[allapend3['Accu_point']>roasterradio ['total_required_point'].sum(),'Earned_M'].cumsum()
  
  # allapend3.loc[allapend3['day']=="WeekDay",'Accu_point']= allapend3['Earned_point'].cumsum()
  # allapend3.loc[allapend3['day'].isin(overtime_classes),'Accu_M_end']=allapend3[ 'Earned_M'].cumsum()

  # allapend3.loc[allapend3['day']=="WeekDay",'Accu_M']=allapend3[ 'Earned_M'].cumsum()
  # #allapend3['Accu_point']=allapend3['Earned_point'].cumsum()

  # allapend3.loc[allapend3['Accu_point']>roasterradio ['total_required_point'].sum(),'Accu_M_day']=allapend3['Earned_M'].cumsum()
  
  
  
  
  final=allapend3.groupby(['Class','day']).agg({'Hospital_x':'count' ,'Earned_point':'sum','Accu_M_day':['max','count'],'Accu_M_end':'max'})
  final.columns = final.columns.map('_'.join).str.strip('_')
  final1= final.reset_index()
  final2=allapend3.groupby(['Hospital_x','SECTION_CODE','day']).agg({'Hospital_x':'count' ,'Earned_point':'sum'})
  final2.columns = final2.columns.map('_'.join).str.strip('_')
  final2= final2.reset_index()
  final2['Radiolgist']=radiologist

  allapend4=pd.concat([allapend4,allapend3])
  xx=allapend4.drop_duplicates(['PROCEDURE_KEY'])
  xx1=allapend4.loc[allapend4['Accu_M_day']>0]
  final1['Radiolgist']=radiologist
  
  
  
  
  
  radtotalpoints=pd.concat([radtotalpoints,final1])
  rad_hos_moda=pd.concat([rad_hos_moda,final2])
  radtotalpoints['Month']=end
  rad_hos_moda['Month']=end

  
  #allapend3.to_excel(r'D:\AAML\CCC\Hospitals data\Radiologist Productivity\Weekend '+radiologist+'.xlsx', sheet_name = "All", index = False) 
  
  
  # i+=1
  
  # if i > 34: 
  #   break
  #  #if i > 50: 
  
  #     break
fin=pd.merge(radtotalpoints, roaster2,left_on='Radiolgist',right_on='Name',how="left")
fin.info()
fin.rename(columns={'Hospital_x_count':'no._cases','Earned_point_sum':'total_point','Accu_M_day_max':'Ot_weekday_sr','Accu_M_day_count':'ot_weekday_cases','Accu_M_end_max':'Ot_weekend_sr',},inplace=True)
fin['Overtime']=0
fin.loc[fin['day']=='WeekDay','Overtime']=fin['total_point']-fin['total_required_point']
fin.to_excel(r'D:\AAML\CCC\Hospitals data\Radiologist Productivity\Radpoins_FEB_22may.xlsx', sheet_name = "All", index = False)
rad_hos_moda.to_excel(r'D:\AAML\CCC\Hospitals data\Radiologist Productivity\Radstats_Feb_22may.xlsx', sheet_name = "All", index = False)


ris_point.to_excel(r'D:\AAML\CCC\Hospitals data\Radiologist Productivity\risall_jan2.xlsx', sheet_name = "All", index = False)

xx=ris_point.loc[ris_point['OPD'].isnull()]
xx=ris_point.loc[ris_point['OPD 2024'].isnull()]
xx=ris_point.loc[(ris_point['OPD 2024'].isnull())&(~ris_point['PROCEDURE_NAME'].isnull())]
xx=ris_point.loc[(ris_point['OPD 2024'].isnull())&(~ris_point['PROCEDURE_NAME_Nicp'].isnull())]

xxx=ris_point.loc[ris_point['SIGNER_Name2']=='Dr. Eman Abdelgadir']

ris_dec.to_excel(r'D:\AAML\CCC\Hospitals data\Radiologist Productivity\Invoices\InvoiceDec_data.xlsx', sheet_name = "All", index = False) 

    
    
#     # Weekend cases
#     radiologist='Dr.Muath Zaher Alyami'
#     roastermuath=roaster2.loc[roaster2['Name']==radiologist]
#     wdlist=roastermuath['Weekend Reporting   (Friday-Saturday)'].str.split('     ',expand=True).stack().str.strip().reset_index(drop=True)
#     wdlist=wdlist[wdlist!='']
#     for elment in wdlist:
#         aa=ris_point.loc[(ris_point['SIGNER_Name2']==radiologist)& (ris_point['PROCEDURE_END'].dt.date==datetime.strptime( elment.split('-')[0].strip(),'%d/%m/%Y').date())]
    
    
    
#     weekendprocd=ris_point.loc[((ris_point['SIGNER_Name2']==radiologist)&(ris_point['Weekend']==1 ))]
#     weekendprocd['Class']='Consultant'
#     weekendprocd.rename(columns={'Cons_point':'Earned_point'},inplace=True)

#     weekendprocd_assis=ris_point.loc[((ris_point['Assistant']==radiologist)&(ris_point['SIGNER_Name2']!=radiologist))&(ris_point['Weekend']==1 )]
#     weekendprocd_assis['Class']='Assistant'
#     weekendprocd_assis.rename(columns={'Assis_point':'Earned_point'},inplace=True)
#     weekendall=pd.concat([weekendprocd, weekendprocd_assis], ignore_index=True, sort=False)
#     weekendall.sort_values('REPORT_VERIFICATION_DATE')
#     weekendall['Accu_point']=weekendall['Earned_point'].cumsum()
#     weekendfin=weekendall.groupby(['Class']).agg({'Hospital':'count' ,'Earned_point':'sum'})
#     weekendfin.reset_index(level=0, inplace=True)
#     weekendfin['Day']='Weekend'
#     weekendfin['Radiologist']=radiologist

    

#     # B-Shift 



ris_point['report_verf_date2']=ris_point['REPORT_VERIFICATION_DATE'].dt.date
test2=ris_point.loc[ris_point['SIGNER_Name2']=="Dr.Leena Kattan"].groupby(['SIGNER_Name2','SECTION_CODE','Hospital_x','ADMISSION_TYPE','report_verf_date2','PROCEDURE_NAME_Nicp']).agg({'PROCEDURE_KEY':'count' })
test2=test2.reset_index()


#     #Weekdays cases
#     radiologistpro=ris_point.loc[(ris_point['SIGNER_Name2']==radiologist)&(ris_point['Weekend']!=1 )]
#     radiologistpro['Class']='Consultant'
#     radiologistpro.rename(columns={'Cons_point':'Earned_point'},inplace=True)
    
    
#     assispro=ris_point.loc[((ris_point['Assistant']==radiologist)&(ris_point['SIGNER_Name2']!=radiologist))&(ris_point['Weekend']!=1 )]
#     assispro['Class']='Assistant'
#     assispro.rename(columns={'Assis_point':'Earned_point'},inplace=True)
#     allprod=pd.concat([radiologistpro, assispro], ignore_index=True, sort=False)
#     allprod.sort_values('REPORT_VERIFICATION_DATE')
#     allprod['Accu_point']=allprod['Earned_point'].cumsum()
#     allprodfin=allprod.groupby(['Class']).agg({'Hospital':'count' ,'Earned_point':'sum'})
#     allprodfin.reset_index(level=0, inplace=True)

#     allprodfin['Day']='Weekday'
#     allprodfin['Radiologist']=radiologist
#     allprodfin2=pd.concat([allprodfin,weekendfin], ignore_index=True, sort=False)



#     i+=1
    
#     if i == 1: 
#         break
    
#     radiolgist_group=radiolgist_time[radiolgist_time['SIGNER_Name2']==radiologist]
#     radiolgist_group['per']=(radiolgist_group['Hospital']/radiolgist_group['Hospital'].sum())*100
#     radiolgist_group['hours']=((21*8)*radiolgist_group['per'])/100
#     radiolgist_group.loc[radiolgist_group['SECTION_CODE']=='X-Ray','expected']=(radiolgist_group['hours']*Baseline_Points_hour_xr)/7.5
#     radiolgist_group.loc[radiolgist_group['SECTION_CODE']!='X-Ray','expected']=(radiolgist_group['hours']*Baseline_Points_hour)
#     radiologistpro.loc[radiologistpro['Accu_point']>=radiolgist_group['expected'].sum(),'Hit Target']='Overtime'
#     radiolgist_group.columns=['Radiologist','Modalitiy','# Cases','Moadlity %','Modality Month Hrs','Expected Points']
#     # allproduc['Radiologist']=radiologist
#     # allproduc['Total Point']=radiologistpro['point'].sum()
#     # allproduc['Overtime Point']=radiologistpro['point'].sum()-672
#     #allproduc.loc[dx] = [radiologist, radiologistpro['point'].sum(), radiologistpro['point'].sum()-672,'']
#     total_point=radiologistpro['point'].fillna(0).sum()
#     new_row={'Radiologist':radiologist,'Total Point':total_point,'Overtime Point':radiologistpro['point'].sum()-672,'Hit target Date':' '}
#     allproduc=allproduc._append(new_row,ignore_index=True)
#     #allproduc['Hit target Date']=radiologistpro['point']
#     radiologistpro.iloc[0:0]
#     radiolgist_group.iloc[0:0]
    

   

#     i+=1
    
#     if i == 1: 
#         break



    
# roaster = pd.read_excel(r"D:\AAML\CCC\Hospitals data\Radiologist Productivity\Updated ROTA names Dec & Jan 2024.xlsx")
# roaster.columns=roaster.iloc[0]
# roaster=roaster[2:]
# roaster.info()
# roaster.replace('____',np.nan ,inplace=True)
# roaster.replace('__',np.nan,inplace=True)
# roaster = roaster.dropna(subset=['ID No.'])
# roaster['TOTAL ACTIVITIES']=roaster['TOTAL ACTIVITIES'].apply(lambda x: x if x >0 else 0)

# roaster['workhours']=(roaster['No. of Workdays']*8)-roaster['TOTAL ACTIVITIES']
# Radiolgistnames = pd.read_excel(r"D:\AAML\CCC\Hospitals data\ALL RADIOLOGOSITS MAPPED NAMES v2.xlsx")
# roaster2=pd.merge(roaster, Radiolgistnames,left_on=roaster['Name'].str.upper().apply(lambda x: x.replace(' ','')),right_on=Radiolgistnames['Final unified list'].astype(str).str.upper().apply(lambda x: x.replace(' ','')),how="left")

# roaster2=roaster2.iloc[: , :-9]
# educationhrs=56
# eduocationnormalize=.675
# monthworkdays=max(roaster2['No. of Workdays'])
# roaster2.loc[roaster2['Category']=="Consultant",'educations_hrs']=(roaster2['No. of Workdays']*educationhrs)/monthworkdays
# roaster2.loc[roaster2['Admin']==1,'admin_hrs']=roaster2['No. of Workdays']*8*.2
# roaster2.fillna(0,inplace=True)
# roaster2['net_report_hrs']=roaster2.workhours-roaster2.educations_hrs -roaster2.admin_hrs
# roaster2['required_report_point']=roaster2.net_report_hrs*4
# roaster2['required_eductio_point']=roaster2.educations_hrs *4*eduocationnormalize
# roaster2['total_required_point']=roaster2.required_report_point +roaster2.required_eductio_point

# roastermuath=roaster2.loc[roaster2['Name']=='Dr.Muath Zaher Alyami']
# wdlist=roastermuath['Weekend Reporting   (Friday-Saturday)'].str.split('     ',expand=True).stack().str.strip().reset_index(drop=True)
# wdlist=wdlist[wdlist!='']
# for elment in wdlist:
#     ris_point['SIGNER_Name2']

# wd_dates = [element.split('-')[0] for element in wdlist]
# wd_modality = [element.split('-')[1] for element in wdlist]

# wdlist.info= list(filter(lambda x: x!=" ", wdlist))
    
# ristes=pd.merge(ris, roaster,left_on=ris['SIGNER_Name2'],right_on=roaster['Name'],how="left")

# # roaster[['mod1','mode2']] = roaster["MODALITY"].str.split(",", n=1, expand=True)
# # roaster['Weekend Reporting']=pd.to_datetime(roaster['Weekend Reporting']).dt.date
# # cleaned1['PROCEDURE_END']=pd.to_datetime(cleaned1['PROCEDURE_END']).dt.date
# # cleaned1['REPORT_VERIFICATION_DATE']=pd.to_datetime(cleaned1['REPORT_VERIFICATION_DATE']).dt.date

# # cleaned1.to_excel(r'D:\AAML\CCC\Hospitals data\cleaned1'+datetime.today().strftime("%d %b, %Y")+'.xlsx', sheet_name = "All", index = False) 

# #test=ph_kf_yam_ar_dw_zu_mj[ph_kf_yam_ar_dw_zu_mj['PROCEDURE_KEY']=="AlDawadmi_PRCA000000173471"]







# ris_point.to_excel(r'D:\AAML\CCC\Hospitals data\Radiologist Productivity\Ris_point'+datetime.today().strftime("%d %b, %Y")+'.xlsx', sheet_name = "All", index = False) 


# cleaned1_roast=pd.merge(cleaned1, roaster,left_on=['SIGNER_Name2','PROCEDURE_END'],right_on=['Name','Weekend Reporting']  ,how="left")


# cleaned1_


# ph_kf_yam_ar_dw_zu_mj['WeekEndProd']=ph_kf_yam_ar_dw_zu_mj.loc[(ph_kf_yam_ar_dw_zu_mj[''])]


# roaster.columns=roaster.iloc[0]
# roaster=roaster.drop(index=[0,1])
# roaster.info()
# ro=roaster['Weekend Reporting'].str.split('-',expand=True)

# ph_kf_yam_ar_dw_zu_mj.loc[((ph_kf_yam_ar_dw_zu_mj['SIGNER_CODE'].isin(roaster['Name'])) & (ph_kf_yam_ar_dw_zu_mj['PROCEDURE_END'].isin(roaster['Weekend Reporting']))),"P_Type"]="Yes"
