SELECT
  dh.subject_id,
  dh.charttime,
  dh.height
FROM `physionet-data.mimiciv_icu.icustays` ic
LEFT JOIN `physionet-data.mimiciv_derived.height` dh
  ON dh.stay_id = ic.stay_id
