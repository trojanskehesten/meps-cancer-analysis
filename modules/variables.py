cancer_feat = 'CANCERDX'
cancer_mult = 'CANCERDX_mult'
cancer_types = ['CABLADDR', 'CABREAST', 'CACERVIX', 'CACOLON', 'CALUNG', 'CALYMPH', 'CAMELANO', 'CAOTHER', 'CAPROSTA', 'CASKINNM', 'CASKINDK', 'CAUTERUS']
cancer_bool_types = [f'{col}_bool' for col in cancer_types]
non_sex_dependent_cancer_types = ['CABLADDR', 'CACOLON', 'CALUNG', 'CALYMPH', 'CAMELANO', 'CAOTHER', 'CASKINNM', 'CASKINDK']
cancer_feat_type = 'CANCERDX_type'

# cancer_type_names = ['BLADDER', 'BREAST', 'CERVICAL', 'COLON', 'LUNG', 'LYMPHOMA', 'SKIN MELANOMA', 'OTHER', 'PROSTATE', 'SKIN-NONMELANO', 'SKIN-UNKNOWN TYPE', 'UTERINE']
# cancer_type_names = ['BLADDER', 'BREAST', 'CERVICAL', 'COLON', 'LUNG', 'LYMPHOMA', 'SKIN', 'OTHER', 'PROSTATE', 'SKIN', 'SKIN', 'UTERINE']
cancer_type_names = ['Bladder', 'Breast', 'Cervical', 'Colon', 'Lung', 'Lymphoma', 'Skin\nMelanoma', 'Other', 'Prostate', 'Skin\nNon-melanoma', 'Skin\nUnknown type', 'Uterine']
non_sex_dependent_cancer_type_names = ['Bladder', 'Colon', 'Lung', 'Lymphoma', 'Skin\nMelanoma', 'Other', 'Skin\nNon-melanoma', 'Skin\nUnknown type']
mult_col = 'Multiple'

no_ans = '2. No'
yes_ans = '1. Yes'
mult_ans = '0. Multiple'
dk_refused_ans = '1. DK / Refused'
vals_to_drop = ['-1 INAPPLICABLE', '-15 CANNOT BE COMPUTED', '-8 DK', '-7 REFUSED']

age_col = 'AGELAST'
sex_col = 'SEX'
race_col = 'RACEV1X'

cancer_colors = {no_ans: "lightgreen", yes_ans: "lightcoral"}
cancer_type_colors = {
    # No cancer
    no_ans: "#E0E6EA",  # light-gray

    # Multiple cancers
    mult_ans: "#616161",  # dark-gray

    # Reproductive cancers
    "1. Breast": "#C97BA7",  # purple
    "1. Cervical": "#C97BA7",
    "1. Uterine": "#C97BA7",
    "1. Prostate": "#C97BA7",

    # Digestive & urinary
    "1. Bladder": "#4CAF50",  # green
    "1. Colon": "#4CAF50",

    # Lung
    "1. Lung": "#42A5F5",  # sky blue

    # Skin cancers
    '1. Skin\nMelanoma': "#FFA726",  # orange
    "1. Skin\nNon-melanoma": "#FFA726",
    '1. Skin\nUnknown type': "#FFA726",

    # Lymphoma
    "1. Lymphoma": "#7E57C2",  # violet

    # Other
    "1. Other": "#9E9E9E",  # medium-gray
    "1. DK / Refused": "#9E9E9E",
}

cancer_type_order = ['2. No', '0. Multiple', '1. DK / Refused', '1. Other', '1. Breast', '1. Cervical', '1. Uterine', '1. Prostate',
 '1. Bladder', '1. Colon', '1. Lung', '1. Skin\nMelanoma', '1. Skin\nNon-melanoma',
 '1. Skin\nUnknown type', '1. Lymphoma']

no_filter = 'NO FILTER'
