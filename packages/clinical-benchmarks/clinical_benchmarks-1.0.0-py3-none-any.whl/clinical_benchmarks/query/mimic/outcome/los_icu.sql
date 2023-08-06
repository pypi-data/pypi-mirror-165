select co.subject_id, icu.los_icu 
from `clinical-benchmarks.benchmarks.cohort` co
left join `physionet-data.mimiciv_derived.icustay_detail` icu
  on co.episode_id = icu.stay_id;