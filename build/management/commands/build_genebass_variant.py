# build_genebass_variant.py
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from variant.models import GenebassVariant, Variant, VariantPhenocode, GenebassCategory
from gene.models import Gene

from optparse import make_option
import logging
import csv
import os
import pandas as pd


class Command(BaseCommand):
    help = "Build Genebass Variant Data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--filename",
            action="append",
            dest="filename",
            help="Filename to import. Can be used multiple times",
        )

    logger = logging.getLogger(__name__)

    # source file directory
    genebassvariantdata_data_dir = os.sep.join(
        [settings.DATA_DIR, "genebass_variant_data/input_07_sep"])


    def handle(self, *args, **options):
        if options["filename"]:
            filenames = options["filename"]
        else:
            filenames = False
        # print("checkpoint 1.1, filenames = ", filenames)

        try:
            # self.purge_GB_Variant()
            self.create_GB_Variant_data(filenames)
        except Exception as msg:
            print(msg)
            self.logger.error(msg)

    def purge_GB_Variant(self):
        # print("checkpoint 1.2 inside purge_GB_Variant function ")
        try:
            GenebassVariant.objects.all().delete()
        except GenebassVariant.DoesNotExist:
            self.logger.warning(
                "GenebassVariant mod not found: nothing to delete.")

        # print("checkpoint 1.3 end of purge_GB_Variant function ")

    def create_GB_Variant_data(self, filenames=False):
        print("checkpoint 1.4 start of create_GB_Variant_data function ")
        self.logger.info("CREATING GENEBASS VARIANT DATA")

        # print("checkpoint1")
        list_of_done=['F2','LTA','SLC22A6','TH','DBH','TGM5','SLC25A6','DGKG','AKR1C2','TAAR1','CHRNA3','CHRNB4','CES1','TYMP','CD55','GP9',
                'GJA1','POU2F2','FXN','CLU','WAS','XIAP','DAO','SREBF1','VCP','EPCAM','CAMK2G','NCOA5','PSMA1','PSMB6','RPS17','DCLK3',
                'IRAK3','MAP3K15','FBXO41','USP14']

        # read source files
        if not filenames:
            filenames = [
                fn
                for fn in os.listdir(self.genebassvariantdata_data_dir)
                if (fn.endswith("_REDUCE.csv") and fn[:-11] not in list_of_done)
            ]

        # print("checkpoint2")
        print("total files : ",len(filenames))

        for filename in filenames:

            filepath = os.sep.join(
                [self.genebassvariantdata_data_dir, filename])

            data = pd.read_csv(filepath, low_memory=False,
                               encoding="ISO-8859-1", sep=";")
            print(f"{filename} is processing, total records {len(data)}")

            # Create settings.VEP_VARIANT_ITEMS_PER_IMPORT objects at a time
            data_length = len(data)
            times = int(data_length / settings.GB_VARIANT_ITEMS_PER_IMPORT)
            for i in range(times):
                print(f"Bulk creating {i * settings.GB_VARIANT_ITEMS_PER_IMPORT} to {(i + 1) * settings.VEP_VARIANT_ITEMS_PER_IMPORT}")
                self.__bulk_create_GB_variant_records(data[i * settings.GB_VARIANT_ITEMS_PER_IMPORT: (i + 1) * settings.VEP_VARIANT_ITEMS_PER_IMPORT])
            self.__bulk_create_GB_variant_records(data[times * settings.GB_VARIANT_ITEMS_PER_IMPORT: data_length])

        print("End of GB Variant data import")

    @staticmethod
    def __bulk_create_GB_variant_records(data):
        objects = []

        for index, row in enumerate(data.iterrows()):
            markerID = data[index: index + 1]["markerID"].values[0]
            if markerID.startswith("chr1:"):
                markerID = data[index: index + 1]["markerID"].values[0][5:]
            n_cases = data[index: index + 1]["n_cases"].values[0]
            n_controls = data[index: index + 1]["n_controls"].values[0]
            phenocode = data[index: index + 1]["phenocode"].values[0]

            n_cases_defined = data[index: index +
                                            1]["n_cases_defined"].values[0]
            n_cases_both_sexes = data[index: index +
                                                1]["n_cases_both_sexes"].values[0]
            n_cases_females = data[index: index +
                                            1]["n_cases_females"].values[0]
            n_cases_males = data[index: index +
                                        1]["n_cases_males"].values[0]
            category = data[index: index + 1]["category"].values[0] # refer to id of GenebassCategory model
            AC = data[index: index + 1]["AC"].values[0]
            AF = data[index: index + 1]["AF"].values[0]
            BETA = data[index: index + 1]["BETA"].values[0]
            SE = data[index: index + 1]["SE"].values[0]
            AF_Cases = data[index: index + 1]["AF_Cases"].values[0]
            AF_Controls = data[index: index + 1]["AF_Controls"].values[0]
            Pvalue = data[index: index + 1]["Pvalue"].values[0]
            genename = data[index: index + 1]["gene"].values[0]

            try:
                # print(filename, " , markerID = ", markerID)
                v = Variant.objects.get(VariantMarker=markerID)
            except Exception as e:
                # self.logger.error(
                #     "Error retrieving variant for entry with VariantMarker ID {markerID}: {error}".format(
                #         markerID=markerID, error=str(e)
                #     )
                # )
                continue

            # fetch variant phenocode
            try:
                # print(filename, ", phenocode = ", phenocode)
                p = VariantPhenocode.objects.get(phenocode=str(phenocode).title())
            except VariantPhenocode.DoesNotExist:

                # self.logger.error(
                #     "VariantPhenocode not found for entry with phenocode {}".format(
                #         phenocode
                #     )
                # )
                continue

            # fetch GenebassCategory
            try:
                # print(filename, ", category = ", category)
                cate = GenebassCategory.objects.get(category_code=category)
            except GenebassCategory.DoesNotExist:

                # self.logger.error(
                #     "VariantPhenocode not found for entry with phenocode {}".format(
                #         phenocode
                #     )
                # )
                continue

            # fetch Gene
            try:
                # print(filename, ", gene_id = ", gene_id)
                g = Gene.objects.get(genename=genename)
            except Gene.DoesNotExist:
                print("Gene not found for entry with genename = ", genename)
                continue

            objects.append
            (
                GenebassVariant(
                markerID=v,
                n_cases=n_cases,
                n_controls=n_controls,
                phenocode=p,
                n_cases_defined=n_cases_defined,
                n_cases_both_sexes=n_cases_both_sexes,
                n_cases_females=n_cases_females,
                n_cases_males=n_cases_males,
                # coding_description=coding_description,
                category=cate,
                AC=AC,
                AF=AF,
                BETA=BETA,
                SE=SE,
                AF_Cases=AF_Cases,
                AF_Controls=AF_Controls,
                Pvalue=Pvalue,
                gene_id=g,
                )
            )
        GenebassVariant.objects.bulk_create(objects)


