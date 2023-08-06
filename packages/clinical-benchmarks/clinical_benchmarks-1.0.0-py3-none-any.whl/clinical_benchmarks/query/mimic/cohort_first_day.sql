select 
    -- Take all lab work (includes subject_id and stay_id)
   lb.*

   -- Get cohort demographics and outcomes
   , co.anchor_age, co.gender, co.ethnicity, co.hospital_expire_flag, co.icu_los
  

   -- Grab vitals that do not overlap with lab work
   , vi.heart_rate_max, vi.heart_rate_mean, vi.heart_rate_min, vi.sbp_max, vi.sbp_mean, vi.sbp_min
   , vi.dbp_max, vi.dbp_mean, vi.dbp_min, vi.mbp_max, vi.mbp_mean, vi.mbp_min
   , vi.resp_rate_max, vi.resp_rate_mean, vi.resp_rate_min
   , vi.temperature_max, vi.temperature_mean, vi.temperature_min
   , vi.spo2_max, vi.spo2_mean, vi.spo2_min, vi.glucose_mean

   -- Grab BG art data if it doesn't overlap with lab and vitals
   , bg.lactate_max, bg.lactate_min, bg.ph_max, bg.ph_min
   , bg.so2_max, bg.so2_min, bg.po2_max, bg.po2_min
   , bg.pco2_max, bg.pco2_min, bg.aado2_max, bg.aado2_min
   , bg.aado2_calc_max, bg.aado2_calc_min, bg.pao2fio2ratio_max, bg.pao2fio2ratio_min
   , bg.baseexcess_max, bg.baseexcess_min, bg.totalco2_max, bg.totalco2_min
   , bg.carboxyhemoglobin_max, bg.carboxyhemoglobin_min
   , bg.methemoglobin_max, bg.methemoglobin_min

   -- Grab GCS data
   , gc.gcs_eyes, gc.gcs_min, gc.gcs_motor, gc.gcs_unable, gc.gcs_verbal

   -- Grab Weight
   , we.weight

from `clinical-benchmarks.benchmarks.cohort` co
left join `physionet-data.mimiciv_derived.first_day_lab` lb
  on co.stay_id = lb.stay_id
left join `physionet-data.mimiciv_derived.first_day_vitalsign` vi
  on co.stay_id = vi.stay_id
left join `physionet-data.mimiciv_derived.first_day_bg_art` bg
  on co.stay_id = bg.stay_id
left join `physionet-data.mimiciv_derived.first_day_gcs` gc
  on co.stay_id = gc.stay_id
left join `physionet-data.mimiciv_derived.first_day_weight` we
  on co.stay_id = we.stay_id
--where icu_los > 1 -- icu_los measured in fractional days, so this is 24 hours
order by co.stay_id