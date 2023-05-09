# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'accounts_customuser'


class AccountsCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_customuser_groups'
        unique_together = (('customuser', 'group'),)


class AccountsCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class AtcAnatomicalGroup(models.Model):
    id = models.CharField(primary_key=True, max_length=1)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'atc_anatomical_group'


class AtcChemicalGroup(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('AtcPharmacologicalGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atc_chemical_group'


class AtcChemicalSubstance(models.Model):
    id = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(AtcChemicalGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atc_chemical_substance'


class AtcPharmacologicalGroup(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('AtcTherapeuticGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atc_pharmacological_group'


class AtcTherapeuticGroup(models.Model):
    id = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(AtcAnatomicalGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atc_therapeutic_group'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DrugAtcAssociation(models.Model):
    association_id = models.AutoField(primary_key=True)
    atc_id = models.ForeignKey(AtcChemicalSubstance, models.DO_NOTHING)
    drug_id = models.ForeignKey('DrugDrug', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'drug_atc_association'


class DrugDrug(models.Model):
    drug_bankid = models.CharField(db_column='drug_bankID', primary_key=True, max_length=20)  # Field name made lowercase.
    name = models.TextField()
    description = models.TextField()
    aliases = models.TextField()
    indication = models.TextField()
    pharmacodynamics = models.TextField()
    moa = models.TextField()
    absorption = models.TextField()
    toxicity = models.TextField()
    halflife = models.TextField()
    distribution_volume = models.TextField()
    protein_binding = models.TextField()
    dosages = models.TextField()
    properties = models.TextField()
    categories = models.ForeignKey('Drugcategory', models.DO_NOTHING)
    chembl = models.ForeignKey('Drugchembl', models.DO_NOTHING, db_column='chEMBL_id')  # Field name made lowercase.
    classname = models.ForeignKey('Drugclass', models.DO_NOTHING)
    direct_parent = models.ForeignKey('Drugparent', models.DO_NOTHING)
    drugtype = models.ForeignKey('Drugtype', models.DO_NOTHING)
    groups = models.ForeignKey('Druggroup', models.DO_NOTHING)
    pubchemcompound = models.ForeignKey('Drugpubchemcompound', models.DO_NOTHING, db_column='pubChemCompound_id')  # Field name made lowercase.
    pubchemsubstance = models.ForeignKey('Drugpubchemblsubstance', models.DO_NOTHING, db_column='pubChemSubstance_id')  # Field name made lowercase.
    subclass = models.ForeignKey('Drugsubclass', models.DO_NOTHING)
    superclass = models.ForeignKey('Drugsuperclass', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'drug_drug'


class Drugcategory(models.Model):
    drugcategory = models.CharField(primary_key=True, max_length=50)
    category_detail = models.TextField()

    class Meta:
        managed = False
        db_table = 'drugcategory'


class Drugchembl(models.Model):
    drugchembl = models.CharField(primary_key=True, max_length=50)
    chembl_detail = models.TextField()

    class Meta:
        managed = False
        db_table = 'drugchembl'


class Drugclass(models.Model):
    drugclass = models.CharField(primary_key=True, max_length=50)
    class_detail = models.TextField()

    class Meta:
        managed = False
        db_table = 'drugclass'


class Druggroup(models.Model):
    druggroup = models.CharField(primary_key=True, max_length=50)
    group_detail = models.TextField()

    class Meta:
        managed = False
        db_table = 'druggroup'


class Drugparent(models.Model):
    drugparent = models.CharField(primary_key=True, max_length=50)
    parent_detail = models.TextField()

    class Meta:
        managed = False
        db_table = 'drugparent'


class Drugpubchemblsubstance(models.Model):
    drugpubchemblsubstance = models.CharField(primary_key=True, max_length=50)
    pubchemblsubstance_detail = models.TextField()

    class Meta:
        managed = False
        db_table = 'drugpubchemblsubstance'


class Drugpubchemcompound(models.Model):
    compound = models.CharField(primary_key=True, max_length=50)
    compound_detail = models.TextField()

    class Meta:
        managed = False
        db_table = 'drugpubchemcompound'


class Drugsubclass(models.Model):
    drugsubclass = models.CharField(primary_key=True, max_length=50)
    subclass_detail = models.TextField()

    class Meta:
        managed = False
        db_table = 'drugsubclass'


class Drugsuperclass(models.Model):
    drugsuperclass = models.CharField(primary_key=True, max_length=50)
    superclass_detail = models.TextField()

    class Meta:
        managed = False
        db_table = 'drugsuperclass'


class Drugtype(models.Model):
    drugtype = models.IntegerField(primary_key=True)
    type_detail = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'drugtype'


class GeneGene(models.Model):
    gene_id = models.CharField(primary_key=True, max_length=50)
    genename = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'gene_gene'


class InteractionInteraction(models.Model):
    interaction_id = models.AutoField(primary_key=True)
    actions = models.TextField()
    known_action = models.TextField()
    interaction_type = models.CharField(max_length=100)
    pubmed_ids = models.TextField()
    drug_bankid = models.ForeignKey(DrugDrug, models.DO_NOTHING, db_column='drug_bankID_id')  # Field name made lowercase.
    uniprot_id = models.ForeignKey('ProteinProtein', models.DO_NOTHING, db_column='uniprot_ID_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'interaction_interaction'


class ProteinProtein(models.Model):
    uniprot_id = models.CharField(db_column='uniprot_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    genename = models.TextField()
    geneid = models.CharField(db_column='geneID', max_length=50)  # Field name made lowercase.
    entry_name = models.TextField()
    protein_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'protein_protein'


class Species(models.Model):
    id = models.BigAutoField(primary_key=True)
    latin_name = models.CharField(unique=True, max_length=100)
    common_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'species'


class TempAuthor(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'temp_author'


class TempBook(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    author = models.ForeignKey(TempAuthor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'temp_book'


class TempReview(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    rating = models.IntegerField()
    book = models.OneToOneField(TempBook, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'temp_review'


class VariantGenebassvariant(models.Model):
    gb_id = models.AutoField(primary_key=True)
    n_cases = models.FloatField()
    n_controls = models.FloatField()
    n_cases_defined = models.FloatField()
    n_cases_both_sexes = models.FloatField()
    n_cases_females = models.FloatField()
    n_cases_males = models.FloatField()
    category = models.CharField(max_length=10)
    ac = models.FloatField(db_column='AC')  # Field name made lowercase.
    af = models.FloatField(db_column='AF')  # Field name made lowercase.
    beta = models.FloatField(db_column='BETA')  # Field name made lowercase.
    se = models.FloatField(db_column='SE')  # Field name made lowercase.
    af_cases = models.FloatField(db_column='AF_Cases')  # Field name made lowercase.
    af_controls = models.FloatField(db_column='AF_Controls')  # Field name made lowercase.
    pvalue = models.FloatField(db_column='Pvalue')  # Field name made lowercase.
    markerid = models.ForeignKey('VariantVariant', models.DO_NOTHING, db_column='markerID_id')  # Field name made lowercase.
    phenocode = models.ForeignKey('VariantVariantphenocode', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'variant_genebassvariant'


class VariantVariant(models.Model):
    variantmarker = models.CharField(db_column='VariantMarker', primary_key=True, max_length=255)  # Field name made lowercase.
    gene_id = models.ForeignKey(GeneGene, models.DO_NOTHING, db_column='Gene_ID_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'variant_variant'


class VariantVariantphenocode(models.Model):
    phenocode = models.CharField(primary_key=True, max_length=200)
    pheno_sex = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    description_more = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'variant_variantphenocode'


class VariantVepvariant(models.Model):
    vep_id = models.AutoField(primary_key=True)
    transcript_id = models.CharField(db_column='Transcript_ID', max_length=255)  # Field name made lowercase.
    consequence = models.CharField(db_column='Consequence', max_length=255)  # Field name made lowercase.
    cdna_position = models.CharField(db_column='cDNA_position', max_length=255)  # Field name made lowercase.
    cds_position = models.CharField(db_column='CDS_position', max_length=255)  # Field name made lowercase.
    protein_position = models.CharField(db_column='Protein_position', max_length=255)  # Field name made lowercase.
    amino_acids = models.CharField(db_column='Amino_acids', max_length=255)  # Field name made lowercase.
    codons = models.CharField(db_column='Codons', max_length=255)  # Field name made lowercase.
    impact = models.CharField(db_column='Impact', max_length=50)  # Field name made lowercase.
    strand = models.IntegerField(db_column='Strand')  # Field name made lowercase.
    bayesdel_addaf_rankscore = models.FloatField(db_column='BayesDel_addAF_rankscore')  # Field name made lowercase.
    bayesdel_noaf_rankscore = models.FloatField(db_column='BayesDel_noAF_rankscore')  # Field name made lowercase.
    cadd_raw_rankscore = models.FloatField(db_column='CADD_raw_rankscore')  # Field name made lowercase.
    clinpred_rankscore = models.FloatField(db_column='ClinPred_rankscore')  # Field name made lowercase.
    dann_rankscore = models.FloatField(db_column='DANN_rankscore')  # Field name made lowercase.
    deogen2_rankscore = models.FloatField(db_column='DEOGEN2_rankscore')  # Field name made lowercase.
    eigen_pc_raw_coding_rankscore = models.FloatField(db_column='Eigen_PC_raw_coding_rankscore')  # Field name made lowercase.
    eigen_raw_coding_rankscore = models.FloatField(db_column='Eigen_raw_coding_rankscore')  # Field name made lowercase.
    fathmm_converted_rankscore = models.FloatField(db_column='FATHMM_converted_rankscore')  # Field name made lowercase.
    gerp_rs_rankscore = models.FloatField(db_column='GERP_RS_rankscore')  # Field name made lowercase.
    gm12878_fitcons_rankscore = models.FloatField(db_column='GM12878_fitCons_rankscore')  # Field name made lowercase.
    genocanyon_rankscore = models.FloatField(db_column='GenoCanyon_rankscore')  # Field name made lowercase.
    h1_hesc_fitcons_rankscore = models.FloatField(db_column='H1_hESC_fitCons_rankscore')  # Field name made lowercase.
    huvec_fitcons_rankscore = models.FloatField(db_column='HUVEC_fitCons_rankscore')  # Field name made lowercase.
    list_s2_rankscore = models.FloatField(db_column='LIST_S2_rankscore')  # Field name made lowercase.
    lrt_converted_rankscore = models.FloatField(db_column='LRT_converted_rankscore')  # Field name made lowercase.
    m_cap_rankscore = models.FloatField(db_column='M_CAP_rankscore')  # Field name made lowercase.
    mpc_rankscore = models.FloatField(db_column='MPC_rankscore')  # Field name made lowercase.
    mvp_rankscore = models.FloatField(db_column='MVP_rankscore')  # Field name made lowercase.
    metalr_rankscore = models.FloatField(db_column='MetaLR_rankscore')  # Field name made lowercase.
    metarnn_rankscore = models.FloatField(db_column='MetaRNN_rankscore')  # Field name made lowercase.
    metasvm_rankscore = models.FloatField(db_column='MetaSVM_rankscore')  # Field name made lowercase.
    mutpred_rankscore = models.FloatField(db_column='MutPred_rankscore')  # Field name made lowercase.
    mutationassessor_rankscore = models.FloatField(db_column='MutationAssessor_rankscore')  # Field name made lowercase.
    mutationtaster_converted_rankscore = models.FloatField(db_column='MutationTaster_converted_rankscore')  # Field name made lowercase.
    provean_converted_rankscore = models.FloatField(db_column='PROVEAN_converted_rankscore')  # Field name made lowercase.
    polyphen2_hdiv_rankscore = models.FloatField(db_column='Polyphen2_HDIV_rankscore')  # Field name made lowercase.
    polyphen2_hvar_rankscore = models.FloatField(db_column='Polyphen2_HVAR_rankscore')  # Field name made lowercase.
    primateai_rankscore = models.FloatField(db_column='PrimateAI_rankscore')  # Field name made lowercase.
    revel_rankscore = models.FloatField(db_column='REVEL_rankscore')  # Field name made lowercase.
    sift4g_converted_rankscore = models.FloatField(db_column='SIFT4G_converted_rankscore')  # Field name made lowercase.
    sift_converted_rankscore = models.FloatField(db_column='SIFT_converted_rankscore')  # Field name made lowercase.
    siphy_29way_logodds_rankscore = models.FloatField(db_column='SiPhy_29way_logOdds_rankscore')  # Field name made lowercase.
    vest4_rankscore = models.FloatField(db_column='VEST4_rankscore')  # Field name made lowercase.
    bstatistic_converted_rankscore = models.FloatField(db_column='bStatistic_converted_rankscore')  # Field name made lowercase.
    fathmm_mkl_coding_rankscore = models.FloatField(db_column='Fathmm_MKL_coding_rankscore')  # Field name made lowercase.
    fathmm_xf_coding_rankscore = models.FloatField(db_column='Fathmm_XF_coding_rankscore')  # Field name made lowercase.
    integrated_fitcons_rankscore = models.FloatField(db_column='Integrated_fitCons_rankscore')  # Field name made lowercase.
    phastcons30way_mammalian_rankscore = models.FloatField(db_column='PhastCons30way_mammalian_rankscore')  # Field name made lowercase.
    phylop30way_mammalian_rankscore = models.FloatField(db_column='PhyloP30way_mammalian_rankscore')  # Field name made lowercase.
    linsight_rankscore = models.FloatField(db_column='LINSIGHT_rankscore')  # Field name made lowercase.
    variant_marker = models.ForeignKey(VariantVariant, models.DO_NOTHING, db_column='Variant_marker_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'variant_vepvariant'
