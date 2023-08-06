with a2 as(
    select subject_id, count(hadm_id) as donors
    from `physionet-data.mimiciv_hosp.admissions` a1
    where deathtime is not null 
    group by subject_id
    having count(hadm_id) > 1
)
select a2.subject_id, a1.hadm_id, a1.deathtime, a1.admittime, a1.hospital_expire_flag, ic.los
from `physionet-data.mimiciv_hosp.admissions` a1
left join a2 
  on a1.subject_id = a2.subject_id
left join `physionet-data.mimiciv_icu.icustays` ic
  on a1.hadm_id = ic.hadm_id
where a2.subject_id is not null and ic.los is null
order by a2.subject_id