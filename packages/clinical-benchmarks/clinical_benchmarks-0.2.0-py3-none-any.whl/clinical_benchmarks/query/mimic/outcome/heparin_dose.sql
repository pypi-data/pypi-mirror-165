SELECT DISTINCT
    e.subject_id
    , ROW_NUMBER() OVER (PARTITION BY e.subject_id ORDER BY charttime) AS dose_num
    , e.charttime
    , e_det.administration_type
    , e_det.dose_due
    , e_det.dose_due_unit
    , e_det.dose_given
    , e_det.dose_given_unit
    , e.medication
    , e.event_txt
FROM `physionet-data.mimiciv_hosp.emar` e
INNER JOIN `clinical-benchmarks.benchmarks.heparin_cohort` hco
    ON e.subject_id = hco.subject_id
INNER JOIN `physionet-data.mimiciv_hosp.emar_detail` e_det
    ON e.emar_id = e_det.emar_id
WHERE e.medication IN ('Heparin') 
    AND e.charttime BETWEEN hco.starttime AND hco.endtime
    AND e_det.parent_field_ordinal IS NULL -- only take the parent field
                                            -- avoid count the same dose multiple times
    AND e.event_txt NOT IN ('Not Confirmed', 'Not Given', 'Not Started', 
                        'Not Started per Sliding Scale', 'Not Stopped', 'Not Stopped per Sliding Scale')