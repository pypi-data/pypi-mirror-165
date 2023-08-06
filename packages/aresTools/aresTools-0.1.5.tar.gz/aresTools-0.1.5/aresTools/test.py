from transformers import smilesListToDataframe, calculateDescriptors, calculateFunctionalGroups, featureEngineering

smiles_list=['CCCCCP','CCCPP']
fg_list=['Alkene','Thiol']
descriptors_list=['nC','nP']
operations_dictionary={'nC':'"nC"','C+p/2p':'("nC"+"nP")/(2*"nC")','p/c':'"nP"/"nC"'}


df=smilesListToDataframe().transform(smiles_list)

print(df)
print('-----------------')

df2=calculateDescriptors().transform(df)
print(df2)
print('-----------------')

df3=calculateFunctionalGroups().transform(df2)
print(df3)
print('-----------------')

df4=featureEngineering(operations_dictionary).transform(df3)
print(df4)
print('-----------------')
