SET search_path TO :"cell_schema", public;
SELECT plan(18);
SET ROLE :"role_name";
SELECT has_user(:'role_name');
SELECT has_schema(:'cell_schema');
SELECT has_table('encounter_mapping');
SELECT has_table('patient_mapping');
SELECT has_table('visit_dimension');
SELECT has_table('observation_fact');
SELECT has_table('patient_dimension');
SELECT has_sequence('observation_fact_text_search_index_seq');
RESET ROLE;


-- encounter_mapping
SELECT count(*) as encounter_mapping_count_query
FROM :"cell_schema".encounter_mapping
WHERE EXISTS(
  SELECT 1
  FROM :"cell_schema".observation_fact of
  WHERE of.encounter_num = encounter_mapping.encounter_num
    AND of.provider_id = ANY(regexp_split_to_array(:'provider_filter', '\s*,\s*'))
)
\gset

SELECT COUNT(*) as encounter_mapping_count_total
FROM :"cell_schema".encounter_mapping;
\gset

-- patient_mapping
SELECT count(*) as patient_mapping_count_query
FROM :"cell_schema".patient_mapping
WHERE EXISTS(
    SELECT 1
    FROM :"cell_schema".observation_fact of
    WHERE of.patient_num = patient_mapping.patient_num
      AND of.provider_id = ANY(regexp_split_to_array(:'provider_filter', '\s*,\s*'))
  )
\gset


SELECT COUNT(*) as patient_mapping_count_total
FROM :"cell_schema".patient_mapping;
\gset

-- visit_dimension
SELECT count(*) as visit_dimension_count_query
FROM :"cell_schema".visit_dimension
WHERE EXISTS(
    SELECT 1
    FROM :"cell_schema".observation_fact of
    WHERE of.encounter_num = visit_dimension.encounter_num
      AND of.provider_id = ANY(regexp_split_to_array(:'provider_filter', '\s*,\s*'))
  )
\gset

SELECT COUNT(*) as visit_dimension_count_total
FROM :"cell_schema".visit_dimension;
\gset

-- observation_fact
SELECT count(*) as observation_fact_count_query
FROM :"cell_schema".observation_fact
WHERE provider_id = ANY(regexp_split_to_array(:'provider_filter', '\s*,\s*'));
\gset

SELECT COUNT(*) as observation_fact_count_total
FROM :"cell_schema".observation_fact;
\gset

-- patient_dimension
SELECT count(*) as patient_dimension_count_query
FROM :"cell_schema".patient_dimension
WHERE EXISTS(
    SELECT 1
    FROM :"cell_schema".observation_fact of
    WHERE of.patient_num = patient_dimension.patient_num
      AND of.provider_id = ANY(regexp_split_to_array(:'provider_filter', '\s*,\s*'))
  )
\gset

SELECT COUNT(*) as patient_dimension_count_total
FROM :"cell_schema".patient_dimension;
\gset


-- with RLS
SET ROLE :"role_name";

-- encounter_mapping
SELECT COUNT(*) as encounter_mapping_count_rls
FROM :"cell_schema".encounter_mapping
\gset

-- patient_mapping
SELECT COUNT(*) as patient_mapping_count_rls
FROM :"cell_schema".patient_mapping
\gset

-- visit_dimension
SELECT COUNT(*) as visit_dimension_count_rls
FROM :"cell_schema".visit_dimension
\gset

-- observation_fact
SELECT COUNT(*) as observation_fact_count_rls
FROM :"cell_schema".observation_fact
\gset

-- patient_dimension
SELECT COUNT(*) as patient_dimension_count_rls
FROM :"cell_schema".patient_dimension
\gset

RESET ROLE;


-- pgTap checks
-- encounter_mapping
select is(:encounter_mapping_count_rls, :encounter_mapping_count_query);
select isnt(:encounter_mapping_count_total, :encounter_mapping_count_query);

-- patient_mapping
select is(:patient_mapping_count_rls, :patient_mapping_count_query);
select isnt(:patient_mapping_count_total, :patient_mapping_count_query);

-- visit_dimension
select is(:visit_dimension_count_rls, :visit_dimension_count_query);
select isnt(:visit_dimension_count_total, :visit_dimension_count_query);

-- observation_fact
select is(:observation_fact_count_rls, :observation_fact_count_query);
select isnt(:observation_fact_count_total, :observation_fact_count_query);

-- patient_dimension
\echo :patient_dimension_count_rls
\echo :patient_dimension_count_query
select is(:patient_dimension_count_rls, :patient_dimension_count_query);
select isnt(:patient_dimension_count_total, :patient_dimension_count_query);
