import os
# print(os.listdir())

required_genename_list=[]
required_geneid_list=[]
with open("20221025-All_Drug_Target_Concerned_GeneID_Genename_For_Genebass.csv", "r") as f:
  lines = f.readlines()
  for line in lines:
    geneid=line[:-1].split(",")[0]
    genename=line[:-1].split(",")[1]
    required_genename_list.append(genename)
    required_geneid_list.append(geneid)
print("required_genename_list: ",len(required_genename_list))

gb_retrieved_list=[]
with open("2022-All_drug_target_genelist_filter_from_genebass.txt", "r") as f:
  lines = f.readlines()
  for line in lines:
    genename=line[:line.find(".csv")]
    gb_retrieved_list.append(genename)
print("gb_retrieved_list: ",len(gb_retrieved_list))

gb_no_need_list=[name for name in gb_retrieved_list if name not in required_genename_list]
print("gb_no_need_list: ",len(gb_no_need_list))

gb_missing_list=[name for name in required_genename_list  if name not in gb_retrieved_list ]
# print(gb_missing_list)
print("gb_missing_list: ",len(gb_missing_list))


vep_gnomad_retrieved_list=[]
with open("20220110-Vep_genelist_from_gnomad.txt", "r") as f:
  lines = f.readlines()
  for line in lines:
    geneID=line[:line.find(".txt")]
    vep_gnomad_retrieved_list.append(geneID)
print("vep_gnomad_retrieved_list: ",len(vep_gnomad_retrieved_list))

vep_gnomad_no_need_list=[name for name in vep_gnomad_retrieved_list  if name not in  required_geneid_list ]
print("vep_gnomad_no_need_list: ",len(vep_gnomad_no_need_list))

vep_gnomad_missing_list=[name for name in required_geneid_list  if name not in vep_gnomad_retrieved_list ]
print("vep_gnomad_missing_list: ",len(vep_gnomad_missing_list))