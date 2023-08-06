with ve as(
    select ic.subject_id, 1 as inv_vent_flag
    from `physionet-data.mimiciv_derived.ventilation` vent
    inner join `physionet-data.mimiciv_icu.icustays` ic
        ON vent.stay_id = ic.stay_id
    where ventilation_status in(
        'InvasiveVent',
        'Trach'
    )
    group by subject_id
)
select co.subject_id
       , coalesce(ve.inv_vent_flag, 0) as inv_vent_flag       
from `clinical-benchmarks.benchmarks.cohort` co
left join ve
  on co.subject_id = ve.subject_id
