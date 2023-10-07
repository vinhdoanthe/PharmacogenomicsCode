
from django.core.management.base import BaseCommand
from variant.models import VepVariant
from django.conf import settings
import os
import logging

class Command(BaseCommand):
    help = 'Add canonical primary transcript'

    # source file directory
    transcript_data_dir = os.sep.join([settings.DATA_DIR, "vep-primary-transcript"])

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

        # read source files
        if not filenames:
            filenames = [
                fn
                for fn in os.listdir(self.transcript_data_dir)
                if fn.endswith("primary_transcript.csv")
            ]
            print(filenames)
        count=0
        for filename in filenames:
            filepath = os.sep.join([self.transcript_data_dir, filename])
            with open(filepath, "r") as f:
                lines = f.readlines()
                for line in lines[1:]:
                    values=line[:-1].split(",")
                    transcript_id = values[3]

                    # Code to add values to the new field
                    objs = VepVariant.objects.filter(Transcript_ID=transcript_id)
                    for obj in objs:
                        obj.Is_primary_ts = 1
                        obj.save()
                    print(transcript_id, " is canonical and is saved")


