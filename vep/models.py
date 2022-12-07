from django.db import models

# Create your models here.

from variantmarker.models import VariantMarker
# Create your models here.


class Vep(models.Model):
    markerID = models.ForeignKey(
        "variantmarker.VariantMarker", on_delete=models.CASCADE, default="None"
    )
    impact = models.CharField(max_length=20)
    strand = models.IntegerField()
    consequence = models.CharField(max_length=200)
    cDNA_position = models.CharField(max_length=50)
    CDS_position = models.CharField(max_length=50)
    protein_position = models.CharField(max_length=50)
    amino_acids = models.CharField(max_length=10)
    codons = models.CharField(max_length=50)
    existing_variation = models.CharField(max_length=50)
    BayesDel_addAF_score = models.FloatField()
    BayesDel_noAF_score = models.FloatField()
    ClinPred_score = models.FloatField()
    DANN_score = models.FloatField()
    DEOGEN2_score = models.FloatField()
    Eigen_PC_phred_coding = models.FloatField()
    Eigen_PC_raw_coding = models.FloatField()
    Eigen_phred_coding = models.FloatField()
    Eigen_raw_coding = models.FloatField()
    FATHMM_score = models.FloatField()
    GM12878_fitCons_score = models.FloatField()
    GenoCanyon_score = models.FloatField()
    H1_hESC_fitCons_score = models.FloatField()
    LIST_S2_score = models.FloatField()
    LRT_Omega = models.FloatField()
    LRT_pred = models.CharField(max_length=10)
    LRT_score = models.FloatField()
    M_CAP_score = models.FloatField()
    MVP_score = models.FloatField()
    MetaLR_score = models.FloatField()
    MetaRNN_score = models.FloatField()
    MutPred_score = models.FloatField()
    MutationAssessor_rankscore = models.FloatField()
    # MutationTaster_AAE = models.FloatField()
    MutationTaster_pred = models.CharField(max_length=10)
    MutationTaster_score = models.FloatField()
    PROVEAN_converted_rankscore = models.FloatField()
    Polyphen2_HDIV_score = models.FloatField()
    Polyphen2_HVAR_score = models.FloatField()
    REVEL_score = models.FloatField()
    SIFT4G_score = models.FloatField()
    SIFT_score = models.FloatField()
    VEST4_score = models.FloatField()
    integrated_fitCons_score = models.FloatField()
    phastCons30way_mammalian = models.FloatField()
    DEOGEN2_score_std = models.FloatField(default=None)
    FATHMM_score_std = models.FloatField(default=None)
    LIST_S2_score_std = models.FloatField(default=None)
    MVP_score_std = models.FloatField(default=None)
    MetaRNN_score_std = models.FloatField(default=None)
    Polyphen2_HDIV_score_std = models.FloatField(default=None)
    Polyphen2_HVAR_score_std = models.FloatField(default=None)
    SIFT4G_score_std = models.FloatField(default=None)
    SIFT_score_std = models.FloatField(default=None)
    VEST4_score_std = models.FloatField(default=None)

    def __str__(self):
        return "VEP for markerID: " + self.markerID.markerID + " of geneID: " + self.markerID.geneID.gene_id + " with gene name: " + self.markerID.geneID.genename
