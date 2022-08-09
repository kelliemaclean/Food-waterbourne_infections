import pandas as pd
from IPython.core.display import display, HTML, Javascript
from string import Template
import json, random
import IPython.display
infections_data = pd.ExcelFile('Food and waterborne infections.xlsx')

def data_clean(data = infections_data):

    '''
    clean data, 
    split Serotype or Genotype, 
    only confirmed etiology data
    '''

    infect_df = pd.read_excel(data)
    desired_columns=['Etiology', 'Serotype or Genotype', 'Illnesses','Etiology Status']
    infect_df.drop(infect_df.columns.difference(desired_columns), axis=1, inplace=True)
    infect_df = infect_df.dropna(subset=['Etiology'])

    infect_df[['pathogen_1', 'pathogen_2','pathogen_3','pathogen_4']] = infect_df['Etiology'].str.split(',|;',3, expand=True)
    infect_df[['geno_1', 'geno_2','geno_3','geno_4']] = infect_df['Serotype or Genotype'].str.split(',|;|:|-',3, expand=True)
    infect_df = infect_df[(infect_df['Etiology Status'] == 'Confirmed')]

    return infect_df

def sub_type(pathology_data):

    '''
    sub type infections based on substring prefex
    create a generalized column for classification
    '''

    pathology_data['Path_type'] = pathology_data['pathogen_1'].astype(str).str[0:4]

    Virus = ['Noro','Rota','Sapo','Hepa', 'Astr', 'Aden']
    Bacteria = ['Clos','Camp','Baci','Salm','Esch', 'Stap','Shig','Pseu','Ente','Bruc',
                'List', 'Legi','Vibr','Micr','Para', 'Stre', 'Pant', 'Lept','Naeg','Prov']
    Parasite = ['Cryp','Cycl','Giar','Avia','Yers', 'Tric','Anis','Acan','Toxo','Ples','Enta']
    Toxin = ['Myco','Cigu','Cyan','Plan','Amne','Neur','Puff','Scom','Hist']
    Chemical = ['Chlo','Pest','Sodi', 'Copp','Heav','Mono','Nitr','Fluo','Sele',
                'Alka','Oil','Ethy','Brom','Soap', 'Hydr','Arse','herb','Morp','Chro','ethy','Phen']
    Unknown = ['Unkn','Othe']


    pathology_data.Path_type.replace(Virus, "Virus", inplace = True)
    pathology_data.Path_type.replace(Bacteria, "Bacteria", inplace = True)
    pathology_data.Path_type.replace(Parasite, "Parasite", inplace = True)
    pathology_data.Path_type.replace(Toxin, "Toxin", inplace = True)
    pathology_data.Path_type.replace(Chemical, "Chemical", inplace = True)
    pathology_data.Path_type.replace(Unknown, "Unknown", inplace = True)
    pathology_data['value'] = pathology_data['value'] = 1 
    pathology_data.to_csv(r'/Users/kelliemaclean/Desktop/food_illness5.csv', index = None, header=True)
    return pathology_data



def bacterial_sero_geno(pathology_data):

    '''
    inspect bacterial infections
    create count for most common causes of illness due to subtype of bacterial infections
    '''

    bacteria_df = pathology_data.loc[(pathology_data.Path_type == 'Bacteria')]

    vcounts = bacteria_df['pathogen_1'].value_counts()
    df_geno = bacteria_df.loc[(bacteria_df.pathogen_1 == 'Salmonella enterica')| 
                          (bacteria_df.pathogen_1 == 'Shigella sonnei') | 
                          (bacteria_df.pathogen_1 == 'Escherichia coli')| 
                          (bacteria_df.pathogen_1 == 'Clostridium perfringens')| 
                          (bacteria_df.pathogen_1 == 'Campylobacter jejuni')| 
                          (bacteria_df.pathogen_1 == 'Legionella pneumophila')| 
                          (bacteria_df.pathogen_1 == 'Staphylococcus aureus')|
                          (bacteria_df.pathogen_1 == 'Vibrio parahaemolyticus')| 
                          (bacteria_df.pathogen_1 == 'Campylobacter unknown')| 
                          (bacteria_df.pathogen_1 == 'Listeria monocytogenes')| 
                          (bacteria_df.pathogen_1 == 'Bacillus cereus')| 
                          (bacteria_df.pathogen_1 == 'Pseudomonas unknown')| 
                          (bacteria_df.pathogen_1 == 'Clostridium botulinum')| 
                          (bacteria_df.pathogen_1 == 'Clostridium difficile')| 
                          (bacteria_df.pathogen_1 == 'Pseudomonas aeruginosa')| 
                          (bacteria_df.pathogen_1 == 'Shigella flexneri')| 
                          (bacteria_df.pathogen_1 == 'Shigella unknown')| 
                          (bacteria_df.pathogen_1 == 'Shigella')| 
                          (bacteria_df.pathogen_1 == 'Streptococcus Group A')]


    geno_count = df_geno.groupby(["pathogen_1", "geno_1"]).count().reset_index()
    desired_columns=['pathogen_1', 'geno_1', 'value']
    geno_count.drop(geno_count.columns.difference(desired_columns), axis=1, inplace=True)

    geno_count.to_csv(r'/Users/kelliemaclean/Desktop/geno.csv', index = None, header=True)

def main():
    infect_df = data_clean(infections_data)
    pathology_data = sub_type(pathology_data=infect_df)
    bacterial_sero_geno(pathology_data=pathology_data)
main()