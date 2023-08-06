SELECT
	ic.subject_id,
	wd.starttime,
	wd.endtime,
	wd.weight
FROM `physionet-data.mimiciv_icu.icustays` ic
LEFT JOIN `physionet-data.mimiciv_derived.weight_durations` wd
	ON wd.stay_id = ic.stay_id