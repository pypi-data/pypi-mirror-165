with dia_a as (
    select stay_id
          , 1 as dialysis_active
    from `physionet-data.mimiciv_derived.rrt`
    where dialysis_active = 1
    group by stay_id
    
), dia_p as (
    select stay_id
          , min(charttime) as min_charttime
          , 1 as dialysis_present
    from `physionet-data.mimiciv_derived.rrt`
    where dialysis_present = 1
    group by stay_id
    
)
select co.episode_id
      , coalesce(dia_a.dialysis_active, 0) as dialysis_active 
      , coalesce(dia_p.dialysis_present, 0) as dialysis_present 
      , coalesce(DATETIME_DIFF(dia_p.min_charttime, co.starttime, HOUR),0) as dialysis_start_time
from `clinical-benchmarks.benchmarks.cohort` as co
left join dia_a 
  on co.episode_id = dia_a.stay_id
left join dia_p
  on co.episode_id = dia_p.stay_id;