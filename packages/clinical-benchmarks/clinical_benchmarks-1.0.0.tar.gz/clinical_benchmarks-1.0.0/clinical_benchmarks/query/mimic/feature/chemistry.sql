-- extract chemistry feature for all admissions

SELECT
    chem.subject_id,
    charttime,
    albumin,
    bun,
    creatinine,
    potassium,
    sodium,
    glucose
FROM `physionet-data.mimiciv_derived.chemistry` chem
INNER JOIN `physionet-data.mimiciv_hosp.admissions` adm
    ON chem.hadm_id = adm.hadm_id