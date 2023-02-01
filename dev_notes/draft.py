import os  
import pandas as pd

def multiple_replace_vcf(a):
	b = {"chr": "",":":" ", "_": " . ","/":" "}
	for x,y in b.items():
			a = a.str.replace(x, y)
	return a


def process(filename, logfile):
	print(filename," is processing")
	with open(logfile,"w") as f:  
		cont=True
		try:
				data=pd.read_csv(filename, sep="\t")
				if len(data.columns)==1:
						data=pd.read_csv(filename)
		except:
				cont=False
				f.write(filename + " An exception occurred\n")
	
		if cont:
				data["vcf"]=multiple_replace_vcf(data["markerID"])
				with open("VEP/input/"+filename[:-4]+".VEP.input", "w") as f:
						for i in range(len(data.vcf.unique())):
								f.write(data.vcf.unique()[i]+"\n")

filenames = [f for f in os.listdir("Genebass/for_VEP_input/")]
for filename in filenames:
		process("Genebass/for_VEP_input/"+filename, "20230119-List_of_genebass_file_can_not_read_with_tab_separator.txt")