-- extract coagulation feature for all admissions
SELECT
    coa.subject_id,
    charttime,
    inr,
    pt,
    ptt
FROM `physionet-data.mimiciv_derived.coagulation` coa  
INNER JOIN `physionet-data.mimiciv_hosp.admissions` adm
    ON coa.hadm_id = adm.hadm_id