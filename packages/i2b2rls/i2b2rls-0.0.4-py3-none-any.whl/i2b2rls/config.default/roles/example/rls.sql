-- Create role and alter search path
\set em_policy :role_name'_em_policy'
\set pm_policy :role_name'_pm_policy'
\set vd_policy :role_name'_vd_policy'
\set of_policy :role_name'_of_policy'
\set pd_policy :role_name'_pd_policy'


CREATE ROLE :"role_name" WITH NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN PASSWORD :'role_pass';
ALTER ROLE :"role_name" IN DATABASE :"db" SET search_path TO :"cell_schema";

-- Table permissions
GRANT USAGE ON SCHEMA :"cell_schema" TO :"role_name";
GRANT SELECT ON ALL TABLES IN SCHEMA :"cell_schema" TO :"role_name";
GRANT ALL ON ALL TABLES IN SCHEMA :"cell_schema" TO :"role_name";
GRANT ALL ON ALL SEQUENCES IN SCHEMA :"cell_schema" TO :"role_name";

-- Enable Row Level Security on tables
alter table :"cell_schema".encounter_mapping enable row level security;
alter table :"cell_schema".patient_mapping enable row level security;
alter table :"cell_schema".visit_dimension enable row level security;
alter table :"cell_schema".observation_fact enable row level security;
alter table :"cell_schema".patient_dimension enable row level security;

-- Create RLS policies
CREATE POLICY :"of_policy" ON :"cell_schema".observation_fact FOR SELECT TO :"role_name" USING (
  provider_id = ANY(regexp_split_to_array(:'provider_filter', '\s*,\s*'))
);
CREATE POLICY :"em_policy" ON :"cell_schema".encounter_mapping FOR SELECT TO :"role_name" USING (
  EXISTS(
    SELECT 1
    FROM :"cell_schema".observation_fact of
    WHERE of.encounter_num = encounter_mapping.encounter_num
      AND of.provider_id = ANY(regexp_split_to_array(:'provider_filter', '\s*,\s*'))
  )
);
CREATE POLICY :"pm_policy" ON :"cell_schema".patient_mapping FOR SELECT TO :"role_name" USING (
  EXISTS(
    SELECT 1
    FROM :"cell_schema".observation_fact of
    WHERE of.patient_num = patient_mapping.patient_num
      AND of.provider_id = ANY(regexp_split_to_array(:'provider_filter', '\s*,\s*'))
  )
);
CREATE POLICY :"vd_policy" ON :"cell_schema".visit_dimension FOR SELECT TO :"role_name" USING (
  EXISTS(
    SELECT 1
    FROM :"cell_schema".observation_fact of
    WHERE of.encounter_num = visit_dimension.encounter_num
      AND of.provider_id = ANY(regexp_split_to_array(:'provider_filter', '\s*,\s*'))
  )
);
CREATE POLICY :"pd_policy" ON :"cell_schema".patient_dimension FOR SELECT TO :"role_name" USING (
  EXISTS(
    SELECT 1
    FROM :"cell_schema".observation_fact of
    WHERE of.patient_num = patient_dimension.patient_num
      AND of.provider_id = ANY(regexp_split_to_array(:'provider_filter', '\s*,\s*'))
  )
);

-- Set individual sequence permissions
GRANT ALL ON SEQUENCE
    :"cell_schema".observation_fact_text_search_index_seq,
    :"cell_schema".upload_status_upload_id_seq
TO :"role_name";
