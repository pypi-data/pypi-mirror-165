-- extract blood_count feature for all admissions
SELECT
    bc.subject_id,
    charttime,
    hemoglobin,
    platelet,
    rbc,
    wbc
FROM `physionet-data.mimiciv_derived.complete_blood_count` bc
INNER JOIN `physionet-data.mimiciv_hosp.admissions` adm
    ON bc.hadm_id = adm.hadm_id