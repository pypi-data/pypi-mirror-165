

#import csv 
#Age selection 

import pandas as pd
pd.set_option('display.max_columns', None)
path = '/Users/surasaksangkhathat/Desktop/THIP/thip_data.csv'

def thipimport(path):
    thip = pd.read_csv(path)
    return thip

#Age selection 
def set_age(thip, lower = 0, upper = 100):
    thip = thip.loc[(thip['age_y'] >= lower) & (thip['age_y'] <= upper)]
    return thip

##clean_up
#Format correction


def getTime(t):
    return t[:2] + ':' + t[2:]

def fillfour(d):
    j = []
    for i in d:
        if len(i) == 4:
            pass
        elif len(i) == 3:
            i = '0' + i
        elif len(i) == 2:
            i = '00' + i
        j.append(i)
    return j

def clean_datetime(thip):
    d = [str(x) for x in thip['timeadm']]
    thip['timeadm'] = [getTime(x) for x in fillfour(d)]
    e = [str(x) for x in thip['timedsc']]
    thip['timedsc'] = [getTime(x) for x in fillfour(e)]
    thip['dateadm'] = pd.to_datetime(thip['dateadm'], format='%Y%m%d', errors='coerce')
    thip['datedsc'] = pd.to_datetime(thip['datedsc'], format='%Y%m%d', errors='coerce')
    thip['marry_status'] = thip['marry_status'].dropna()
    thip['marry_status'] = thip.marry_status.astype('Int64')
    return thip

def los(thip):
    thip['los'] = thip['datedsc'] - thip['dateadm']
    print(thip['los'])
    print('Average length of stay(days) = ', thip['los'].mean())

#Library of diagnosis

q_esop = ['Q390','Q391','Q392','Q393']
q_duo = ['Q410']
q_small = ['Q411','Q412','Q418','Q419'] 
q_hscr = ['Q431']
q_arm = ['Q420', 'Q421', 'Q422', 'Q423', 'Q428', 'Q429']
q_omp = ['Q792']
q_gas = ['Q793']
q_cdh = ['Q790']
q_down = ['Q909']
q_intuss = ['K561']
q_appen = ['K350', 'K353', 'K358', 'K35', 'K352', 'K3520', 'K3521', 'K3530', 'K3531', 'K3532', 'K3533', 'K3580', 'K3589']

q_neop = ['Q390','Q391','Q392','Q393','Q410','Q411','Q412','Q418','Q419', 'Q431','Q421', 'Q422', 'Q423', 'Q428', 'Q429','Q790','Q792','Q793']
q_arm_420 = ['Q420']
q_arm_421 = ['Q421']
q_cardiac = ['Q200', 'Q201', 'Q202', 'Q203', 'Q204', 'Q205', 'Q206', 'Q207', 'Q208', 'Q209'
             'Q210', 'Q211', 'Q212', 'Q213', 'Q214', 'Q215', 'Q216', 'Q217', 'Q218', 'Q219'
             'Q220', 'Q221', 'Q222', 'Q223', 'Q224', 'Q225', 'Q226', 'Q227', 'Q228', 'Q229'
             'Q230', 'Q231', 'Q232', 'Q233', 'Q234', 'Q235', 'Q236', 'Q237', 'Q238', 'Q239'
             'Q240', 'Q241', 'Q242', 'Q243', 'Q244', 'Q245', 'Q246', 'Q247', 'Q248', 'Q249'
             'Q250', 'Q251', 'Q252', 'Q253', 'Q254', 'Q255', 'Q256', 'Q257', 'Q258', 'Q259'
             'Q260', 'Q261', 'Q262', 'Q263', 'Q264', 'Q265', 'Q266', 'Q267', 'Q268', 'Q269'
             'Q270', 'Q271', 'Q272', 'Q273', 'Q274', 'Q275', 'Q276', 'Q277', 'Q278', 'Q279'
             'Q280', 'Q281', 'Q282', 'Q283', 'Q284', 'Q285', 'Q286', 'Q287', 'Q288', 'Q289'
             ]

q_nec = ['P771', 'P772', 'P773', 'P779', 'K553', 'K5530']
q_ihps = ['Q400']
q_ba = ['Q442']
q_chol = ['Q444']
q_tongue = ['Q381']



#Diagnostic group selection

def select_Q(source, condition, dupdel = True):
    output = source.loc[source['pdx'].isin(condition)
    | source['sdx1'].isin(condition)
    | source['sdx2'].isin(condition)
    | source['sdx3'].isin(condition)
    | source['sdx4'].isin(condition)
    | source['sdx5'].isin(condition)
    | source['sdx6'].isin(condition)
    | source['sdx7'].isin(condition)
    | source['sdx8'].isin(condition)
    | source['sdx9'].isin(condition)
    | source['sdx10'].isin(condition)
    | source['sdx11'].isin(condition)
    | source['sdx12'].isin(condition)
    | source['sdx13'].isin(condition)
    | source['sdx14'].isin(condition)
    | source['sdx15'].isin(condition)
    | source['sdx16'].isin(condition)
    | source['sdx17'].isin(condition)
    | source['sdx18'].isin(condition)
    | source['sdx19'].isin(condition)
    | source['sdx20'].isin(condition)
    ]
    print('Number of selected records before duplication deletion are', len(output))
    if dupdel == True:
        output = output.drop_duplicates(subset=['pid'], keep='first')
    else:
        exit
    print('Number of selected records after duplication deletion are', len(output))
    return output

#Selected Df kept as 'anom'

def sex_ratio(anom):
    anom_sex = anom.groupby(['sex'])['sex'].count().to_list()
    anom_sex_ratio = anom_sex[0]/anom_sex[1]
    print(anom_sex_ratio)
    
#Count by groups

def count_by_year(anom):
    anom_year = anom.groupby(['g_year'])['g_year'].count().to_list()
    print('Case number in 2017 =', anom_year[0],
         'Case number in 2018 =', anom_year[1],
         'Case number in 2019 =', anom_year[2],
         'Case number in 2020 =', anom_year[3],
        )
    live_birth = [656571, 628450, 596736, 569338]
    list_inc = [i*10000 / j for i, j in zip(anom_year, live_birth)]
    print('Crude incidence in 2017 =', list_inc[0],
         'Crude incidence in 2018 =', list_inc[1],
         'Crude incidence in 2019 =', list_inc[2],
         'Crude incidence in 2020 =', list_inc[3],
        )

def count_by_month(anom):
    anom_month = anom.groupby(['mth'])['mth'].count()
    print(anom_month)
    anom_year_month = anom.groupby(['g_year','mth']).size()
    print(anom_year_month)

#Export to CSV

def export(anom, name):
    anom.to_csv(name+'.csv',index = False, sep=',', encoding='utf-8')



#Health region distribution

def count_by_region(anom):
    anom_region = anom.groupby(['health_region'])['health_region'].count().to_list()
    print('Case number in region 1 =', anom_region[0],
         'Case number in region 2 =', anom_region[1],
         'Case number in region 3 =', anom_region[2],
         'Case number in region 4 =', anom_region[3],
         'Case number in region 5 =', anom_region[4],
         'Case number in region 6 =', anom_region[5],
         'Case number in region 7 =', anom_region[6],
         'Case number in region 8 =', anom_region[7],
         'Case number in region 9 =', anom_region[8],
         'Case number in region 10 =', anom_region[9],
         'Case number in region 11 =', anom_region[10],
         'Case number in region 12 =', anom_region[11],
         'Case number in Bangkok =', anom_region[12]
        )
    return anom_region


def mortal(anom):
    anom_count = len(anom)
    anom_mortal = len(anom.loc[anom['death_date'].notnull()])
    anom_mortal_rate = 100*anom_mortal/anom_count
    print('total death cases =', anom_mortal,  'in', anom_count, 'cases')
    print('mortality rate =', anom_mortal_rate)

# Count proportion of associated anomalies

def count_down(diag):
    q_down = ['Q909']
    down = diag.loc[diag['pdx'].isin(q_down)
    | diag['sdx1'].isin(q_down)
    | diag['sdx2'].isin(q_down)
    | diag['sdx3'].isin(q_down)
    | diag['sdx4'].isin(q_down)
    | diag['sdx5'].isin(q_down)
    | diag['sdx6'].isin(q_down)
    | diag['sdx7'].isin(q_down)
    | diag['sdx8'].isin(q_down)
    | diag['sdx9'].isin(q_down)
    | diag['sdx10'].isin(q_down)
    | diag['sdx11'].isin(q_down)
    | diag['sdx12'].isin(q_down)
    | diag['sdx13'].isin(q_down)
    | diag['sdx14'].isin(q_down)
    | diag['sdx15'].isin(q_down)
    | diag['sdx16'].isin(q_down)
    | diag['sdx17'].isin(q_down)
    | diag['sdx18'].isin(q_down)
    | diag['sdx19'].isin(q_down)
    | diag['sdx20'].isin(q_down)
    ]
    print('Number of DS in this diagnosis = ', len(down))
    print('Ratio of DS in this diagnosis = ', len(down)/len(diag))
    
def count_heart(diag):
    heart = diag.loc[diag['pdx'].isin(q_cardiac)
    | diag['sdx1'].isin(q_cardiac)
    | diag['sdx2'].isin(q_cardiac)
    | diag['sdx3'].isin(q_cardiac)
    | diag['sdx4'].isin(q_cardiac)
    | diag['sdx5'].isin(q_cardiac)
    | diag['sdx6'].isin(q_cardiac)
    | diag['sdx7'].isin(q_cardiac)
    | diag['sdx8'].isin(q_cardiac)
    | diag['sdx9'].isin(q_cardiac)
    | diag['sdx10'].isin(q_cardiac)
    | diag['sdx11'].isin(q_cardiac)
    | diag['sdx12'].isin(q_cardiac)
    | diag['sdx13'].isin(q_cardiac)
    | diag['sdx14'].isin(q_cardiac)
    | diag['sdx15'].isin(q_cardiac)
    | diag['sdx16'].isin(q_cardiac)
    | diag['sdx17'].isin(q_cardiac)
    | diag['sdx18'].isin(q_cardiac)
    | diag['sdx19'].isin(q_cardiac)
    | diag['sdx20'].isin(q_cardiac)
    ]
    print('Number of congenital heart disesases in this diagnosis = ', len(heart))
    print('Ratio of congenital heart diseases in this diagnosis = ', len(heart)/len(diag))
    
def count_assoc(diag, condition):
    cond = diag.loc[diag['pdx'].isin(condition)
    | diag['sdx1'].isin(condition)
    | diag['sdx2'].isin(condition)
    | diag['sdx3'].isin(condition)
    | diag['sdx4'].isin(condition)
    | diag['sdx5'].isin(condition)
    | diag['sdx6'].isin(condition)
    | diag['sdx7'].isin(condition)
    | diag['sdx8'].isin(condition)
    | diag['sdx9'].isin(condition)
    | diag['sdx10'].isin(condition)
    | diag['sdx11'].isin(condition)
    | diag['sdx12'].isin(condition)
    | diag['sdx13'].isin(condition)
    | diag['sdx14'].isin(condition)
    | diag['sdx15'].isin(condition)
    | diag['sdx16'].isin(condition)
    | diag['sdx17'].isin(condition)
    | diag['sdx18'].isin(condition)
    | diag['sdx19'].isin(condition)
    | diag['sdx20'].isin(condition)
    ]
    print('Number of selected condition in this diagnosis = ', len(cond))
    print('Ratio of congenital heart diseases in this diagnosis = ', len(cond)/len(diag))

#count and sort procedure

def procdict(diag):
    proc_list = []
    procedure_dict = {}
    proc_list = diag['proc1'].to_list()
    proc_list = proc_list + diag['proc2'].to_list()
    proc_list = proc_list + diag['proc3'].to_list()
    proc_list = proc_list + diag['proc4'].to_list()
    proc_list = proc_list + diag['proc5'].to_list()
    proc_list = proc_list + diag['proc6'].to_list()
    proc_list = proc_list + diag['proc7'].to_list()
    proc_list = proc_list + diag['proc8'].to_list()
    proc_list = proc_list + diag['proc9'].to_list()
    proc_list = proc_list + diag['proc10'].to_list()
    proc_list = proc_list + diag['proc11'].to_list()
    proc_list = proc_list + diag['proc12'].to_list()
    proc_list = proc_list + diag['proc13'].to_list()
    proc_list = proc_list + diag['proc14'].to_list()
    proc_list = proc_list + diag['proc15'].to_list()
    proc_list = proc_list + diag['proc16'].to_list()
    proc_list = proc_list + diag['proc17'].to_list()
    proc_list = proc_list + diag['proc18'].to_list()
    proc_list = proc_list + diag['proc19'].to_list()
    proc_list = proc_list + diag['proc20'].to_list()
    proc_list = [item for item in proc_list if not(pd.isnull(item)) == True]
    for entry in proc_list:
        if entry in(procedure_dict):
            procedure_dict[entry] += 1
        else:
            procedure_dict[entry] = 1
    procedure_dict = {str(key): val for key, val in procedure_dict.items()}
    for key in sorted(procedure_dict.keys()):
        print(key , " :: " , procedure_dict[key])
        print('')
    print(sorted(procedure_dict.items(), key=lambda x: x[1], reverse = True))
    return procedure_dict

def filterdict(procedure_dict):
    fourdict = {k: v for k, v in procedure_dict.items() if k.startswith('4')}
    print(sorted(fourdict.items(), key=lambda x: x[1], reverse = True))
 
# Select by procedure
proc_eso = ['4251', '4252','4253','4254','4255','4256','4257','4258','4259']

def select_procedure(source, condition):
    output = source.loc[source['proc1'].isin(condition)
    | source['proc2'].isin(condition)
    | source['proc3'].isin(condition)
    | source['proc4'].isin(condition)
    | source['proc5'].isin(condition)
    | source['proc6'].isin(condition)
    | source['proc7'].isin(condition)
    | source['proc8'].isin(condition)
    | source['proc9'].isin(condition)
    | source['proc10'].isin(condition)
    | source['proc11'].isin(condition)
    | source['proc12'].isin(condition)
    | source['proc13'].isin(condition)
    | source['proc14'].isin(condition)
    | source['proc15'].isin(condition)
    | source['proc16'].isin(condition)
    | source['proc17'].isin(condition)
    | source['proc18'].isin(condition)
    | source['proc19'].isin(condition)
    | source['proc20'].isin(condition)
    ]
    print('Number of selected records are', len(output))
    return output




    
