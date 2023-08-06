SELECT 
    le.subject_id,
    le.charttime,
    le.valuenum AS vancomycin_level
FROM `clinical-benchmarks.benchmarks.vancomycin_cohort` vco
LEFT JOIN `physionet-data.mimiciv_hosp.labevents` le
    ON vco.subject_id = le.subject_id
WHERE le.itemid = 51009 
    AND le.charttime BETWEEN vco.starttime AND vco.endtime