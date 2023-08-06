select co.subject_id, adm.hospital_expire_flag 
from `clinical-benchmarks.benchmarks.cohort` co
left join `physionet-data.mimiciv_icu.icustays` ic
  on co.episode_id = ic.stay_id
left join `physionet-data.mimiciv_hosp.admissions` adm
  on ic.hadm_id = adm.hadm_id;