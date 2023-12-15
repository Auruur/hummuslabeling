import streamlit as st
import warnings
warnings.filterwarnings("ignore")
import ast
import re
import math
import numpy as np
import pandas as pd
from IPython.display import display

def save_label(df, ingredient, group, typo):
    index_to_update = df.loc[df['INGREDIENT'] == ingredient].index

    if not index_to_update.empty:
        df.at[index_to_update[0], 'GROUP'] = group
        df.at[index_to_update[0], 'TYPOLOGY'] = typo
    else:
        new_row = pd.DataFrame({'INGREDIENT': [ingredient], 'GROUP': [group], 'TYPOLOGY': [typo]})
        df = pd.concat([df, new_row], ignore_index=True)
    
    return df
    
sel_items = pd.read_csv('/Users/gionni/Desktop/Tirocinio/datasets/cfp_wfp_ingredients.csv', sep=';', header=0)
ingr_unique = pd.read_csv('/Users/gionni/Desktop/Tirocinio/datasets/output_unique_cleaned.csv', sep=',', header=0)
labels_df = pd.DataFrame(columns=["INGREDIENT", "GROUP", "TYPOLOGY"])

ingredients = ingr_unique['ingredient'][0:30]
sel_groups = ["AGRICULTURAL PROCESSED", "ANIMAL HUSBANDRY", "CROPS", "FISHING", "NONE"]

agricultural_typo = sel_items.loc[sel_items['FOOD COMMODITY GROUP'] == 'AGRICULTURAL PROCESSED', 'Food commodity TYPOLOGY'].unique().tolist()
animal_typo = sel_items.loc[sel_items['FOOD COMMODITY GROUP'] == 'ANIMAL HUSBANDRY', 'Food commodity TYPOLOGY'].unique().tolist()
crops_typo = sel_items.loc[sel_items['FOOD COMMODITY GROUP'] == 'CROPS', 'Food commodity TYPOLOGY'].unique().tolist()
fishing_typo = sel_items.loc[sel_items['FOOD COMMODITY GROUP'] == 'FISHING', 'Food commodity TYPOLOGY'].unique().tolist()

agricultural_typo.append('NONE')
animal_typo.append('NONE')
crops_typo.append('NONE')
fishing_typo.append('NONE')

st.title("INGREDIENT LABELING")
st.write("Group definition: wide category of food commodity.\n1) Agricultural processed: any kind of plant based processed food.\n2) Animal husbandry: products of terrestrial animal origin.\n3) Crops: plant based product, not processed. This group includes fresh plant products, seeds, dry fruit.\n4) Fishing: includes all the animals and weeds from fresh and salted waters.")
st.write("Typology definition: aggregated level of food commodity description. It is more generic than items and represent a groups of items having similar characteristics. For example the typology legumes includes peas, lentils, beans, soybeans etc.")
st.write("If a correct group or typology can't be found there is the possibility to select NONE.")
st.write("---")

for index, ingredient in enumerate(ingredients):
    st.write(f"{index+1}.\nIngredient name: {ingredient}")

    selected_group = st.selectbox("Select a group:", sel_groups, key=index)

    if selected_group == sel_groups[0]:
        selected_typo = st.selectbox("Select a typology:", agricultural_typo, key=f"{index}_agricultural")
    elif selected_group == sel_groups[1]:
        selected_typo = st.selectbox("Select a typology:", animal_typo, key=f"{index}_animal")
    elif selected_group == sel_groups[2]:
        selected_typo = st.selectbox("Select a typology:", crops_typo, key=f"{index}_crops")
    elif selected_group == sel_groups[3]:
        selected_typo = st.selectbox("Select a typology:", fishing_typo, key=f"{index}_fishing")
    elif selected_group == sel_groups[4]:
        selected_typo = "NONE"

    labels_df = save_label(labels_df, ingredient, selected_group, selected_typo)
    st.write("---")

st.write("This button displays the current state of the dataframe on the host terminal")
st.button("Display", on_click=display(labels_df))
