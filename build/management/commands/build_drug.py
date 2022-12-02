# build_drug.py
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


from drug.models import Drug

from optparse import make_option
import logging
import csv
import os
import pandas as pd


class Command(BaseCommand):
    help = "Build Drug Data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--filename",
            action="append",
            dest="filename",
            help="Filename to import. Can be used multiple times",
        )

    logger = logging.getLogger(__name__)

    # source file directory
    drugdata_data_dir = os.sep.join([settings.DATA_DIR, "drug_data"])

    print("checkpoint1")

    def handle(self, *args, **options):
        if options["filename"]:
            filenames = options["filename"]
        else:
            filenames = False
        print("checkpoint 1.1, filenames = ", filenames)

        try:
            self.purge_drugs()
            self.create_drug_data(filenames)
        except Exception as msg:
            print(msg)
            self.logger.error(msg)

    def purge_drugs(self):
        print("checkpoint 1.2 inside purge_drugs function ")
        try:
            Drug.objects.all().delete()
        except Drug.DoesNotExist:
            self.logger.warning("Drugs mod not found: nothing to delete.")

        print("checkpoint 1.3 end of purge_drugs function ")

    def create_drug_data(self, filenames=False):
        print("checkpoint 1.4 start of create_drug_data function ")
        self.logger.info("CREATING DRUGDATA")

        # read source files
        if not filenames:
            filenames = [
                fn
                for fn in os.listdir(self.drugdata_data_dir)
                if fn.endswith("drug_data.csv")
            ]
            print("checkpoint2")
            print(filenames)

        for filename in filenames:

            filepath = os.sep.join([self.drugdata_data_dir, filename])

            data = pd.read_csv(filepath, low_memory=False,
                               encoding="ISO-8859-1", sep=";")

            for index, row in enumerate(data.iterrows()):

                drug_bankID = data[index: index + 1]["pk"].values[0]
                drugtype = data[index: index + 1]["drugtype"].values[0]
                name = data[index: index + 1]["name"].values[0]
                # drugalias = [
                #     "" if str(drugalias_raw) == "nan" else ", " +
                #     str(drugalias_raw)
                # ]
                # # trialadd = ['' if str(trialname) == drugname else ' ('+str(trialname)+')']
                # drugname = drugname + drugalias[0]
                groups = data[index: index + 1]["groups"].values[0]
                categories = data[index: index + 1]["categories"].values[0]
                description = data[index: index + 1]["description"].values[0]
                aliases = data[index: index + 1]["aliases"].values[0]
                kingdom = data[index: index + 1]["kingdom"].values[0]
                superclass = data[index: index + 1]["superclass"].values[0]
                classname = data[index: index + 1]["classname"].values[0]
                subclass = data[index: index + 1]["subclass"].values[0]
                direct_parent = data[index: index +
                                     1]["direct_parent"].values[0]
                indication = data[index: index + 1]["indication"].values[0]
                pharmacodynamics = data[index: index +
                                        1]["pharmacodynamics"].values[0]
                moa = data[index: index + 1]["moa"].values[0]
                absorption = data[index: index + 1]["absorption"].values[0]
                toxicity = data[index: index + 1]["toxicity"].values[0]
                halflife = data[index: index + 1]["halflife"].values[0]
                distribution_volume = data[index: index +
                                           1]["distribution_volume"].values[0]
                protein_binding = data[index: index +
                                       1]["protein_binding"].values[0]
                dosages = data[index: index + 1]["dosages"].values[0]
                properties = data[index: index + 1]["properties"].values[0]

                # # fetch protein
                # try:
                #     p = Protein.objects.get(entry_name=entry_name)
                # except Protein.DoesNotExist:

                #     self.logger.error(
                #         "Protein not found for entry_name {}".format(
                #             entry_name)
                #     )
                #     continue

                print("checkpoint 2.1 - start to fetch data to Drug table")
                drug, created = Drug.objects.get_or_create(
                    drug_bankID=drug_bankID,
                    drugtype=drugtype,
                    name=name,
                    groups=groups,
                    categories=categories,
                    description=description,
                    aliases=aliases,
                    kingdom=kingdom,
                    superclass=superclass,
                    classname=classname,
                    subclass=subclass,
                    direct_parent=direct_parent,
                    indication=indication,
                    pharmacodynamics=pharmacodynamics,
                    moa=moa,
                    absorption=absorption,
                    toxicity=toxicity,
                    halflife=halflife,
                    distribution_volume=distribution_volume,
                    protein_binding=protein_binding,

                    dosages=dosages,
                    properties=properties)
                drug.save()
                print("a record is saved")

                # target_list = drug.target.all()

        self.logger.info("COMPLETED CREATING DRUGDATA")
