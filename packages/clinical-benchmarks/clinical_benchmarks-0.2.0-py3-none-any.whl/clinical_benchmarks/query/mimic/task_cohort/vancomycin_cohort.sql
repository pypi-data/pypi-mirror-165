-- extract the subjects from initial cohort where subject has Vancomycin prescription during ICU
SELECT DISTINCT
    co.subject_id,
    co.episode_id,
    co.starttime,
    co.endtime,
    co.los
FROM `clinical-benchmarks.benchmarks.cohort` co
LEFT JOIN `physionet-data.mimiciv_hosp.emar` em
    ON co.subject_id = em.subject_id
WHERE  em.medication = 'Vancomycin'
    AND em.charttime BETWEEN co.starttime AND co.endtime