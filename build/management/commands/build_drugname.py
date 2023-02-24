# build_drug.py
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


from drug.models import DrugName

from optparse import make_option
import logging
import csv
import os
import pandas as pd


class Command(BaseCommand):
    help = "Build Drugname Data"

    # source file directory
    drugdata_data_dir = os.sep.join([settings.DATA_DIR, "drug_data"])

    def add_arguments(self, parser):
        parser.add_argument(
            "--filename",
            action="append",
            dest="filename",
            help="Filename to import. Can be used multiple times",
        )
    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        if options["filename"]:
            filenames = options["filename"]
        else:
            filenames = False
        print("checkpoint 1.1, filenames = ", filenames)

        try:
            self.purge_drugnames()
            self.create_drugname_data(filenames)
        except Exception as msg:
            print(msg)
            self.logger.error(msg)

    def purge_drugnames(self):
        try:
            DrugName.objects.all().delete()
        except DrugName.DoesNotExist:
            self.logger.warning("Drugnames mod not found: nothing to delete.")

    def create_drugname_data(self, filenames=False):
        self.logger.info("CREATING DRUGNAMEDATA")

        # read source files
        if not filenames:
            filenames = [
                fn
                for fn in os.listdir(self.drugdata_data_dir)
                if fn.endswith("encoded_drug_data.txt")
            ]
            print(filenames)
        
        for filename in filenames:
            filepath = os.sep.join([self.drugdata_data_dir, filename])
            with open(filepath, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line[0]=="1":
                        values=line[:-1].split(":")
                        drugname = values[0].split("-")[1]
                        name_detail = values[1]


                        name, created = DrugName.objects.get_or_create(
                            drugname=drugname,
                            name_detail=name_detail,
                            )
                        name.save()
                        print("a record is saved")

        self.logger.info("COMPLETED CREATING DRUGNAME DATA")
