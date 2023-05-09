import subprocess

subprocess.run(['python', 'manage.py', 'build_atc_anatomic_group'])
subprocess.run(['python', 'manage.py', 'build_atc_therapeutic_group'])
subprocess.run(['python', 'manage.py', 'build_atc_pharmacological_group'])
subprocess.run(['python', 'manage.py', 'build_atc_chemical_group'])
subprocess.run(['python', 'manage.py', 'build_atc_chemical_substance'])

subprocess.run(['python', 'manage.py', 'build_drugcategory'])
subprocess.run(['python', 'manage.py', 'build_drugclass'])
subprocess.run(['python', 'manage.py', 'build_drugsubclass'])
subprocess.run(['python', 'manage.py', 'build_drugparent'])
subprocess.run(['python', 'manage.py', 'build_drugsuperclass'])
subprocess.run(['python', 'manage.py', 'build_druggroup'])
subprocess.run(['python', 'manage.py', 'build_drugcompound'])
subprocess.run(['python', 'manage.py', 'build_drugtype'])
subprocess.run(['python', 'manage.py', 'build_drugchembl'])
subprocess.run(['python', 'manage.py', 'build_drugpubchemsubstance'])

subprocess.run(['python', 'manage.py', 'build_drug'])
subprocess.run(['python', 'manage.py', 'build_drug_atc'])
subprocess.run(['python', 'manage.py', 'build_gene'])
subprocess.run(['python', 'manage.py', 'build_protein'])
subprocess.run(['python', 'manage.py', 'build_interaction'])
subprocess.run(['python', 'manage.py', 'build_variant_phenocode'])
subprocess.run(['python', 'manage.py', 'build_variant_marker'])
subprocess.run(['python', 'manage.py', 'build_genebass_variant'])
subprocess.run(['python', 'manage.py', 'build_vep_variant'])