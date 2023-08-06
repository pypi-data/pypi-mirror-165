-- Cohort creation for benchmarks
-- Inclusion criteria:
-- 1. Age at admission > 15 years
-- 2. ICU LOS > 4 hours
-- 3. First ICU stay
-- 4. Have at least one charted observation
-- 5. Not an organ donor account
--DROP TABLE IF EXISTS cohort; -- look into this for BigQuery, doesn't seem to work right now
with co_intime as
(
  select ie.stay_id, min(charttime) as intime, max(charttime) as outtime, count(ce.itemid) as item_count
  from `physionet-data.mimiciv_icu.icustays` ie
  left join `physionet-data.mimiciv_icu.chartevents` ce
    on ie.stay_id = ce.stay_id
    and ce.charttime between DATETIME_SUB(ie.intime, interval '12' HOUR) and DATETIME_ADD(ie.outtime, interval '12' HOUR)
  group by ie.stay_id
) 
, co as
(
    select  -- only keep subject_id as unique identifier
    ie.subject_id
    , ie.stay_id as episode_id
    , ie.intime as starttime
    , ie.outtime as endtime
    , ie.los as los

    -- Inclusion criteria
    , case 
       when pat.anchor_age >15 then 1
       else 0
      end as inclusion_age
    , case 
        when ie.los > 1/6 then 1 -- los is in fractional days so 1/6 is 4 hours
        else  0
      end as inclusion_icu_los
    , row_number() over (partition by ie.subject_id order by adm.admittime, coi.intime) as stay_num
    , case 
        when coi.item_count >= 1 then 1 
        else 0
      end as inclusion_chart_events
    from `physionet-data.mimiciv_icu.icustays` ie
    inner join co_intime coi
      on ie.stay_id = coi.stay_id
    inner join `physionet-data.mimiciv_hosp.patients` pat
      on  ie.subject_id = pat.subject_id
    inner join `physionet-data.mimiciv_icu.chartevents` ce
      on ie.stay_id = ce.stay_id
    inner join `physionet-data.mimiciv_hosp.admissions` adm
      on ie.hadm_id = adm.hadm_id
)
select co.*
from co
where inclusion_age = 1
  and inclusion_icu_los = 1
  and stay_num = 1 -- just include first stay in ICU
  and inclusion_chart_events = 1;