# build_genebass_variant.py
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from variant.models import Variant
from gene.models import Gene
from optparse import make_option
import logging
import csv
import os
import pandas as pd


class Command(BaseCommand):
    help = "Build Variant Marker Data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--filename",
            action="append",
            dest="filename",
            help="Filename to import. Can be used multiple times",
        )

    logger = logging.getLogger(__name__)

    # source file directory
    variantmarkerdata_data_dir = os.sep.join(
        [settings.DATA_DIR, "variantmarker_data"])

    print("checkpoint1")

    def handle(self, *args, **options):
        if options["filename"]:
            filenames = options["filename"]
        else:
            filenames = False
        print("checkpoint 1.1, filenames = ", filenames)

        try:
            self.purge_variant_marker()
            self.create_variant_marker_data(filenames)
        except Exception as msg:
            print(msg)
            self.logger.error(msg)

    def purge_variant_marker(self):
        print("checkpoint 1.2 inside purge_variant_marker function ")
        try:
            Variant.objects.all().delete()
        except Variant.DoesNotExist:
            self.logger.warning(
                "VariantMarker mod not found: nothing to delete.")

        print("checkpoint 1.3 end of purge_variant_marker function ")

    def create_variant_marker_data(self, filenames=False):
        print("checkpoint 1.4 start of create_GB_Variant_data function ")
        self.logger.info("CREATING VARIANT MARKER DATA")

        # read source files
        if not filenames:
            filenames = [
                fn
                for fn in os.listdir(self.variantmarkerdata_data_dir)
                if fn.endswith("variant_marker_data.csv")
            ]
            print("checkpoint2")
            print(filenames)

        for filename in filenames:

            filepath = os.sep.join(
                [self.variantmarkerdata_data_dir, filename])

            data = pd.read_csv(filepath, low_memory=False,
                               encoding="ISO-8859-1", sep=";")
            data.drop_duplicates(subset=["VariantMarker"], inplace=True)

            print("data length = ", len(data))
            print("data column = ", data.columns)

            # count_items = data.count()
            # # Create 10000 items at a time
            # for i in range(0, len(data), 10000):
            #     print("checkpoint 2.1 - start to fetch data to variant table")
            #     Variant.objects.bulk_create([
            #         Variant(
            #             Gene_ID_id=data["GeneID"][i],
            #             VariantMarker=data["VariantMarker"][i],
            #         )
            #         for i in range(i, i + 10000)
            #     ])

            for index, row in enumerate(data.iterrows()):
                geneID = data[index: index + 1]["GeneID"].values[0]
                markerID = data[index: index + 1]["VariantMarker"].values[0]

                # fetch gene
                # try:
                #     g = Gene.objects.get(gene_id=geneID)
                # except Gene.DoesNotExist:
                #
                #     self.logger.error(
                #         "Gene not found for entry with gene ID {}".format(
                #             geneID)
                #     )
                #     continue

                # print("checkpoint 2.1 - start to fetch data to genebass variant table")
                marker, created = Variant.objects.get_or_create(
                    Gene_ID_id=geneID,
                    VariantMarker=markerID,
                )
                marker.save()
                print(index, "th record is saved")

        self.logger.info("COMPLETED CREATING VARIANT MARKER DATA")
