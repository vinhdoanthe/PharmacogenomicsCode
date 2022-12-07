# build_genebass_variant.py
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


from vep.models import Vep
from variantmarker.models import VariantMarker


from optparse import make_option
import logging
import csv
import os
import pandas as pd


class Command(BaseCommand):
    help = "Build Genebass VEP Data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--filename",
            action="append",
            dest="filename",
            help="Filename to import. Can be used multiple times",
        )

    logger = logging.getLogger(__name__)

    # source file directory
    genebassvepdata_data_dir = os.sep.join(
        [settings.DATA_DIR, "vep_Genebass_data"])

    print("checkpoint1")

    def handle(self, *args, **options):
        if options["filename"]:
            filenames = options["filename"]
        else:
            filenames = False
        print("checkpoint 1.1, filenames = ", filenames)

        try:
            self.purge_genebass_vep()
            self.create_genebass_vep_data(filenames)
        except Exception as msg:
            print(msg)
            self.logger.error(msg)

    def purge_genebass_vep(self):
        print("checkpoint 1.2 inside purge_variant_marker function ")
        try:
            Vep.objects.all().delete()
        except Vep.DoesNotExist:
            self.logger.warning(
                "Vep mod not found: nothing to delete.")

        print("checkpoint 1.3 end of purge_genebass_vep function ")

    def create_genebass_vep_data(self, filenames=False):
        print("checkpoint 1.4 ")
        self.logger.info("CREATING GENEBASS VEP DATA")

        # read source files
        if not filenames:
            filenames = [
                fn
                for fn in os.listdir(self.genebassvepdata_data_dir)
                if fn.endswith("GenebassVEP.csv")
            ]
            print("checkpoint2")
            print(filenames)

        for filename in filenames:

            filepath = os.sep.join(
                [self.genebassvepdata_data_dir, filename])

            data = pd.read_csv(filepath, low_memory=False,
                               encoding="ISO-8859-1", sep=";")

            print("data length = ", len(data))
            print("data column = ", data.columns)
            for index, row in enumerate(data.iterrows()):
                # print("inside enumerate , index = ")

                variantmarker = data[index: index + 1]["MarkerID"].values[0]
                # print("inside enumerate 2, index = ", index)
                impact = data[index: index + 1]["IMPACT"].values[0]
                strand = data[index: index + 1]["STRAND"].values[0]
                consequence = data[index: index + 1]["Consequence"].values[0]
                cDNA_position = data[index: index +
                                     1]["cDNA_position"].values[0]
                CDS_position = data[index: index + 1]["CDS_position"].values[0]
                protein_position = data[index: index +
                                        1]["Protein_position"].values[0]
                amino_acids = data[index: index + 1]["Amino_acids"].values[0]
                codons = data[index: index + 1]["Codons"].values[0]
                existing_variation = data[index: index +
                                          1]["Existing_variation"].values[0]
                BayesDel_addAF_score = data[index: index +
                                            1]["BayesDel_addAF_score"].values[0]
                BayesDel_noAF_score = data[index: index +
                                           1]["BayesDel_noAF_score"].values[0]
                ClinPred_score = data[index: index +
                                      1]["ClinPred_score"].values[0]
                DANN_score = data[index: index + 1]["DANN_score"].values[0]
                DEOGEN2_score = data[index: index +
                                     1]["DEOGEN2_score_mean"].values[0]
                DEOGEN2_score_std = data[index: index +
                                         1]["DEOGEN2_score_std"].values[0]
                Eigen_PC_phred_coding = data[index: index +
                                             1]["Eigen-PC-phred_coding"].values[0]
                Eigen_PC_raw_coding = data[index: index +
                                           1]["Eigen-PC-raw_coding"].values[0]
                Eigen_phred_coding = data[index: index +
                                          1]["Eigen-phred_coding"].values[0]
                Eigen_raw_coding = data[index: index +
                                        1]["Eigen-raw_coding"].values[0]
                FATHMM_score = data[index: index +
                                    1]["FATHMM_score_mean"].values[0]
                FATHMM_score_std = data[index: index +
                                        1]["FATHMM_score_std"].values[0]
                GM12878_fitCons_score = data[index: index +
                                             1]["GM12878_fitCons_score"].values[0]
                GenoCanyon_score = data[index: index +
                                        1]["GenoCanyon_score"].values[0]
                H1_hESC_fitCons_score = data[index: index +
                                             1]["H1-hESC_fitCons_score"].values[0]
                LIST_S2_score = data[index: index +
                                     1]["LIST-S2_score_mean"].values[0]
                LIST_S2_score_std = data[index: index +
                                         1]["LIST-S2_score_std"].values[0]

                LRT_Omega = data[index: index + 1]["LRT_Omega"].values[0]
                LRT_pred = data[index: index + 1]["LRT_pred"].values[0]
                LRT_score = data[index: index + 1]["LRT_score"].values[0]
                M_CAP_score = data[index: index + 1]["M-CAP_score"].values[0]
                MVP_score = data[index: index + 1]["MVP_score_mean"].values[0]
                MVP_score_std = data[index: index +
                                     1]["MVP_score_std"].values[0]
                MetaLR_score = data[index: index + 1]["MetaLR_score"].values[0]
                MetaRNN_score = data[index: index +
                                     1]["MetaRNN_score_mean"].values[0]
                MetaRNN_score_std = data[index: index +
                                         1]["MetaRNN_score_std"].values[0]
                MutPred_score = data[index: index +
                                     1]["MutPred_score"].values[0]
                MutationAssessor_rankscore = data[index: index +
                                                  1]["MutationAssessor_rankscore"].values[0]
                # MutationTaster_AAE = data[index: index +
                #                           1]["MutationTaster_AAE"].values[0]
                MutationTaster_pred = data[index: index +
                                           1]["MutationTaster_pred"].values[0]
                MutationTaster_score = data[index: index +
                                            1]["MutationTaster_score"].values[0]
                PROVEAN_converted_rankscore = data[index: index +
                                                   1]["PROVEAN_converted_rankscore"].values[0]
                Polyphen2_HDIV_score = data[index: index +
                                            1]["Polyphen2_HDIV_score_mean"].values[0]
                Polyphen2_HDIV_score_std = data[index: index +
                                                1]["Polyphen2_HDIV_score_std"].values[0]
                Polyphen2_HVAR_score = data[index: index +
                                            1]["Polyphen2_HVAR_score_mean"].values[0]
                Polyphen2_HVAR_score_std = data[index: index +
                                                1]["Polyphen2_HVAR_score_std"].values[0]

                REVEL_score = data[index: index + 1]["REVEL_score"].values[0]
                SIFT4G_score = data[index: index +
                                    1]["SIFT4G_score_mean"].values[0]
                SIFT4G_score_std = data[index: index +
                                        1]["SIFT4G_score_std"].values[0]
                SIFT_score = data[index: index +
                                  1]["SIFT_score_mean"].values[0]
                SIFT_score_std = data[index: index +
                                      1]["SIFT_score_std"].values[0]
                VEST4_score = data[index: index +
                                   1]["VEST4_score_mean"].values[0]
                VEST4_score_std = data[index: index +
                                       1]["VEST4_score_std"].values[0]
                integrated_fitCons_score = data[index: index +
                                                1]["integrated_fitCons_score"].values[0]
                phastCons30way_mammalian = data[index: index +
                                                1]["phastCons30way_mammalian"].values[0]

                # fetch variant marker
                print("Check point - before fetching ")
                try:
                    print("variantmarker from data file: ", variantmarker)
                    vm = VariantMarker.objects.get(
                        markerID=variantmarker)
                    print("variantmarker after get from primary key : ", vm)
                except VariantMarker.DoesNotExist:

                    self.logger.error(
                        "VariantMarker not found for entry with VariantMarker ID {}".format(
                            variantmarker)
                    )
                    continue

                print(
                    "checkpoint 2.1 - start to fetch data to genebass variant table")
                print("type of vm : ", type(vm))
                vep, created = Vep.objects.get_or_create(
                    markerID=vm,
                    impact=impact,
                    strand=strand,
                    consequence=consequence,
                    cDNA_position=cDNA_position,
                    CDS_position=CDS_position,
                    protein_position=protein_position,
                    amino_acids=amino_acids,
                    codons=codons,
                    existing_variation=existing_variation,
                    BayesDel_addAF_score=BayesDel_addAF_score,
                    BayesDel_noAF_score=BayesDel_noAF_score,
                    ClinPred_score=ClinPred_score,
                    DANN_score=DANN_score,
                    DEOGEN2_score=DEOGEN2_score,
                    DEOGEN2_score_std=DEOGEN2_score_std,
                    Eigen_PC_phred_coding=Eigen_PC_phred_coding,
                    Eigen_PC_raw_coding=Eigen_PC_raw_coding,
                    Eigen_phred_coding=Eigen_phred_coding,
                    Eigen_raw_coding=Eigen_raw_coding,
                    FATHMM_score=FATHMM_score,
                    FATHMM_score_std=FATHMM_score_std,
                    GM12878_fitCons_score=GM12878_fitCons_score,
                    GenoCanyon_score=GenoCanyon_score,
                    H1_hESC_fitCons_score=H1_hESC_fitCons_score,
                    LIST_S2_score=LIST_S2_score,
                    LIST_S2_score_std=LIST_S2_score_std,
                    LRT_Omega=LRT_Omega,
                    LRT_pred=LRT_pred,
                    LRT_score=LRT_score,
                    M_CAP_score=M_CAP_score,
                    MVP_score=MVP_score,
                    MVP_score_std=MVP_score_std,
                    MetaLR_score=MetaLR_score,
                    MetaRNN_score=MetaRNN_score,
                    MetaRNN_score_std=MetaRNN_score_std,
                    MutPred_score=MutPred_score,
                    MutationAssessor_rankscore=MutationAssessor_rankscore,
                    # MutationTaster_AAE=MutationTaster_AAE,
                    MutationTaster_pred=MutationTaster_pred,
                    MutationTaster_score=MutationTaster_score,
                    PROVEAN_converted_rankscore=PROVEAN_converted_rankscore,
                    Polyphen2_HDIV_score=Polyphen2_HDIV_score,
                    Polyphen2_HDIV_score_std=Polyphen2_HDIV_score_std,
                    Polyphen2_HVAR_score=Polyphen2_HVAR_score,
                    Polyphen2_HVAR_score_std=Polyphen2_HVAR_score_std,
                    REVEL_score=REVEL_score,
                    SIFT4G_score=SIFT4G_score,
                    SIFT4G_score_std=SIFT4G_score_std,
                    SIFT_score=SIFT_score,
                    SIFT_score_std=SIFT_score_std,
                    VEST4_score=VEST4_score,
                    VEST4_score_std=VEST4_score_std,
                    integrated_fitCons_score=integrated_fitCons_score,
                    phastCons30way_mammalian=phastCons30way_mammalian

                )
                print("checkpoint")
                vep.save()
                print("a record is saved")

        self.logger.info("COMPLETED CREATING VEP DATA")
