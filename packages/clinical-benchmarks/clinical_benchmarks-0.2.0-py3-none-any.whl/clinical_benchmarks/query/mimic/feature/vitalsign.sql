SELECT
    dvi.subject_id,
    dvi.charttime,
    dvi.heart_rate,
    dvi.sbp,
    dvi.dbp,
    dvi.mbp,
    dvi.resp_rate,
    dvi.temperature,
    dvi.spo2,
    dvi.glucose
FROM `physionet-data.mimiciv_icu.icustays` ic
LEFT JOIN `physionet-data.mimiciv_derived.vitalsign` dvi
    ON ic.stay_id = dvi.stay_id