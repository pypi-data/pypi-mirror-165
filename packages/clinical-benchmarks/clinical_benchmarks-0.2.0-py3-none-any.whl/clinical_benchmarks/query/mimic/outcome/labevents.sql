-- extract the lab values from labevents table for different tasks purposes
-- extract on top of the cohort
WITH labevent AS
(
    SELECT le.subject_id
        , le.specimen_id
        , le.charttime
        , le.storetime
        , le.itemid
        , dl.fluid
        , dl.category
        , dl.label
        , le.value
        , le.valuenum
        , le.valueuom
        , le.ref_range_lower, le.ref_range_upper
        , le.priority
        , le.comments
    FROM `physionet-data.mimiciv_hosp.labevents` le
    INNER JOIN `physionet-data.mimiciv_hosp.d_labitems` dl
        ON le.itemid = dl.itemid
    -- the label now works for heparin case, can add more later for other task.
    WHERE label IN ('PT', 'INR(PT)', 'PTT')
)
SELECT
    le.*
FROM `clinical-benchmarks.benchmarks.cohort` co
LEFT JOIN labevent le
    ON co.subject_id = le.subject_id