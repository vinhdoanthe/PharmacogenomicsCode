# build_genebass_variant.py
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


from variant.models import GenebassVariant, Variant, VariantPhenocode


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
        [settings.DATA_DIR, "genebass_variant_data"])

    # print("checkpoint1")

    def handle(self, *args, **options):
        if options["filename"]:
            filenames = options["filename"]
        else:
            filenames = False
        # print("checkpoint 1.1, filenames = ", filenames)

        try:
            self.purge_GB_Variant()
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

        # read source files
        if not filenames:
            filenames = [
                fn
                for fn in os.listdir(self.genebassvariantdata_data_dir)
                if fn.endswith(".csv")
            ]
            # print("checkpoint2")
            print(filenames)

        for filename in filenames:

            filepath = os.sep.join(
                [self.genebassvariantdata_data_dir, filename])

            data = pd.read_csv(filepath, low_memory=False,
                               encoding="ISO-8859-1", sep=";")

            print("filename ", filename, " is processing ")
            for index, row in enumerate(data.iterrows()):
                print(f"index {index} is processing")
                markerID = data[index: index + 1]["markerID"].values[0]
                
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
                category = data[index: index + 1]["category"].values[0]
                AC = data[index: index + 1]["AC"].values[0]
                AF = data[index: index + 1]["AF"].values[0]
                BETA = data[index: index + 1]["BETA"].values[0]
                SE = data[index: index + 1]["SE"].values[0]

                # breakpoint()
                AF_Cases = data[index: index + 1]["AF.Cases"].values[0]
                AF_Controls = data[index: index + 1]["AF.Controls"].values[0]
                Pvalue = data[index: index + 1]["Pvalue"].values[0]

                try:
                    print(filename, " , markerID = " , markerID)
                    v = Variant.objects.get(VariantMarker=markerID)
                except Exception as e:
                    self.logger.error(
                        "Error retrieving variant for entry with VariantMarker ID {markerID}: {error}".format(
                            markerID=markerID, error=str(e)
                        )
                    )
                    continue

                # fetch variant phenocode
                try:
                    print(filename, ", phenocode = " , phenocode)
                    p = VariantPhenocode.objects.get(phenocode=phenocode.title())
                except VariantPhenocode.DoesNotExist:

                    self.logger.error(
                        "VariantPhenocode not found for entry with phenocode {phenocode}".format(
                        )
                    )
                    continue
                # print("we are here too")

                # print("checkpoint 2.1 - start to fetch data to genebass variant table")
                gb_variant, created = GenebassVariant.objects.get_or_create(
                    markerID=v,
                    n_cases=n_cases,
                    n_controls=n_controls,
                    phenocode=p,
                    n_cases_defined=n_cases_defined,
                    n_cases_both_sexes=n_cases_both_sexes,
                    n_cases_females=n_cases_females,
                    n_cases_males=n_cases_males,
                    # coding_description=coding_description,
                    category=category,
                    AC=AC,
                    AF=AF,
                    BETA=BETA,
                    SE=SE,
                    AF_Cases=AF_Cases,
                    AF_Controls=AF_Controls,
                    Pvalue=Pvalue,
                )
                gb_variant.save()
                print(filename, " a record is saved")

        self.logger.info("COMPLETED CREATING GENEBASS VARIANT DATA")
