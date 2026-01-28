cancer_feat = 'CANCERDX'
cancer_mult = 'CANCERDX_mult'
cancer_types = ['CABLADDR', 'CABREAST', 'CACERVIX', 'CACOLON', 'CALUNG', 'CALYMPH', 'CAMELANO', 'CAOTHER', 'CAPROSTA', 'CASKINNM', 'CASKINDK', 'CAUTERUS']
cancer_bool_types = [f'{col}_bool' for col in cancer_types]
non_sex_dependent_cancer_types = ['CABLADDR', 'CACOLON', 'CALUNG', 'CALYMPH', 'CAMELANO', 'CAOTHER', 'CASKINNM', 'CASKINDK']
cancer_feat_type = 'CANCERDX_type'

cancer_type_names = ['Bladder', 'Breast', 'Cervical', 'Colon', 'Lung', 'Lymphoma', 'Skin\nMelanoma', 'Other', 'Prostate', 'Skin\nNon-melanoma', 'Skin\nUnknown type', 'Uterine']
non_sex_dependent_cancer_type_names = ['Bladder', 'Colon', 'Lung', 'Lymphoma', 'Skin\nMelanoma', 'Other', 'Skin\nNon-melanoma', 'Skin\nUnknown type']
mult_col = 'Multiple'

no_ans = '2. No'
yes_ans = '1. Yes'
mult_ans = '0. Multiple'
dk_refused_ans = '1. DK / Refused'
vals_to_drop = ['-1 INAPPLICABLE', '-15 CANNOT BE COMPUTED', '-8 DK', '-7 REFUSED']

no_raw_ans = '2 NO'
yes_raw_ans = '1 YES'

age_col = 'AGELAST'
age_col_cat = age_col + "_CAT"
sex_col = 'SEX'
race_col = 'RACEV1X'

dash_age_feat = 'Age'
dash_sex_feat = 'Sex'
dash_race_feat = 'Race'
dash_dem_feats_types = ['cont', 'cat', 'cat']

age_bins = [17, 39, 64, 86]
age_groups = ["1. Young adults (18-39)", "2. Middle-aged (40-64)", "3. Older adults (65-85)"]

dash_plot_height = 400

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

# Conclusions:
# 1 Distributions
# 2 Analysis:
concl_diag = {
    "Age": """Patients with a cancer diagnosis are **significantly older** than those without a reported cancer history (**median age 69 vs. 47**). This difference is statistically significant (**p < 0.001, α = 0.0085** via the MannWhitney test). This is expected, as the risk of developing cancer increases with age. This trend can be largely explained by the cumulative accumulation of genetic mutations over time ([Tomasetti & Vogelstein, 2015](https://doi.org/10.1126/science.1260825)), and prolonged exposure to modifiable lifestyle and environmental risk factors such as tobacco use, excess body weight, poor diet, and physical inactivity ([White et al., 2014](https://doi.org/10.1016/j.amepre.2013.10.029)). Additionally, individuals without a reported cancer history are, by definition, still at risk of developing cancer in the future, which partly explains why this group appears younger in the current cross‑sectional snapshot.""",
    "Sex": """A **statistically significant difference** is observed between males and females regarding cancer diagnosis (*p* = 0.001). **А slightly higher proportion of females** are diagnosed with cancer compared to males.

This is also explained by the presence of several sex-specific cancers in the dataset that occur only in women (such as cervical and uterine cancers), which naturally increases the overall number of female cancer cases.

This pattern **aligns with epidemiological data**:

- While **overall cancer mortality is higher in men**, **women are more frequently diagnosed** with certain types of cancer ([Siegel et al., 2022](https://acsjournals.onlinelibrary.wiley.com/doi/full/10.1002/cncr.35458)).

- **Health-seeking behavior may also play a role**-women are probably more likely to participate in routine screenings and preventive care, potentially leading to **higher diagnosis rates**""",
    "Race": """* A Chi-square test comparing cancer diagnosis (yes/no) across racial groups shows a statistically significant association (χ² p-value < 0.001, alpha threshold 0.0085), with a **Cramér’s V of 0.098**, suggesting a **weak but non-negligible relationship** between race and cancer diagnosis rates.

* This association is largely driven by **White** patients, who both constitute the majority of the sample and have a higher proportion of cancer diagnoses compared with all other racial groups combined (14% vs 7%; post-hoc level 1, **p < 0.001**, alpha threshold 0.00427). At the same time, cancer diagnosis rates among non-White groups (Black, Asian/Hawaiian, Indian/Alaskan, Multiple races) are relatively similar overall (7%, 4%, 7%, 8%), except for the notably lower rate in **Asian/Hawaiian**, so the global signal in the Chi-square test primarily reflects the contrast between White and non-White patients rather than strong heterogeneity within non-White groups.

* More detailed post-hoc analyses limited to non-White patients (post-hoc level 2, alpha threshold 0.00107) suggest that only some pairwise contrasts within non-White groups reach or approach conventional significance thresholds, but none survive the stricter family-wise error control. For example, Black vs all other non-White groups shows a modest difference (7% vs 5%, p = 0.005 > 0.00107), Asian/Hawaiian vs others shows lower cancer rates (4% vs 7%, **p < 0.001**), whereas Indian/Alaskan and Multiple-race groups do not differ meaningfully from the remaining non-White groups (p = 1.000 and p = 0.254, respectively), indicating that evidence for systematic differences within non-White groups is limited once multiple testing is controlled.

* This findings **reflect real-world disparities** documented in epidemiological literature. Studies consistently show that **White populations tend to have higher reported rates of cancer diagnosis**, partly due to **better access to screening and healthcare** services ([DeSantis et al., 2019](https://doi.org/10.3322/caac.21555); [Siegel et al., 2023](https://doi.org/10.3322/caac.21763)). In contrast, **underdiagnosis** or **delayed diagnosis** is more common in minority racial groups due to socioeconomic and structural barriers ([Williams & Mohammed, 2009](https://doi.org/10.1007/s10865-008-9185-0)).""",
}
consl_types = {
    "Age": """- **Strong Alignment**: Prostate, cervical, lung, and colon cancers match known age patterns.  
- **Red Flags**:  
  - Young bladder/uterine cases warrant scrutiny (*data errors or rare subtypes?*).  
  - Lymphoma’s broad range suggests unclassified subtypes.  
- **Screening Implications**:  
  - Breast cancer’s older median may reflect under-screening in younger groups.  
  - Cervical cancer’s young peak reinforces need for early HPV vaccination/screening.""",
    "Sex": """- As expected, **sex-specific cancers** (breast, cervical, prostate, uterine) show **associations with sex**:
        - **breast, cervical, and uterine cancers occur exclusively in females**,
        - and **prostate cancer exclusively in males**.  

    - With the Sidak-adjusted threshold (α = 0.0057), **bladder cancer** is the only nonsex-specific cancer type showing a statistically significant association with sex (p < 0.001, positive MCC), indicating a clear predominance among **men**.  

    - Women are exclusively affected by **cervical**, **uterine**, and [almost exclusively](https://medlineplus.gov/malebreastcancer.html) by **breast** cancers, which are either strictly or predominantly female diseases, contributing to a higher overall cancer burden among women in this dataset. **Breast cancer** is the **most common cancer in women worldwide** ([WHO  Cancer in Women](https://www.who.int/news-room/fact-sheets/detail/cancer)). 

    - **Сolon**, **lung**, **lymphoma**, **melanoma**, **"Other"**, **skin**, and **multiple** cancers do not show statistically significant sex-based differences after multiple-testing correction (p > 0.0057). Any observed imbalances in these groups should therefore be interpreted with caution as they may reflect random variation rather than true effects.​

    - This suggests that beyond biological sex-specific cancers, sex-related differences in diagnosis are generally modest for most cancer types in this dataset and may, in part, be influenced by behavioral or environmental factors rather than sex alone.""",
    "Race": """* A Fisher's exact test comparing **racial distributions across cancer types yields a statistically significant association** (p < 0.001, α_global ≈ 0.0085), with a Cramér's V of 0.158, suggesting a moderate relationship between race and cancer type.

* **Post-hoc analysis** (13 contrasts, α = 0.00066) reveals the association is **primarily driven by skin cancers** (melanoma, non-melanoma, unknown), where **White** patients show substantially higher rates compared to Black, Asian/Hawaiian, and Multiple-race patients. **Prostate** cancer shows higher rates in **Black** patients vs lower rates in Asian/Hawaiian and Multiple-race patients, while multiple cancers show higher rates in White patients vs lower rates in Black and Asian/Hawaiian patients. **Other cancer types show non-significant racial differences** at this threshold.""",
}
# 3. Filters
