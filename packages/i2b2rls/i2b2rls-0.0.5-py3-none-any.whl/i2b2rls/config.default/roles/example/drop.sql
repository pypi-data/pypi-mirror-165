SELECT count(*) > 0 as user_exists FROM pg_roles WHERE rolname = :'role_name' \gset
\if :user_exists
    \echo Removing user :role_name
    REVOKE ALL ON DATABASE i2b2 FROM :"role_name";
    DROP OWNED BY :"role_name";
    DROP ROLE IF EXISTS :"role_name";
\endif

\set em_policy :role_name'_em_policy'
\set pm_policy :role_name'_pm_policy'
\set vd_policy :role_name'_vd_policy'
\set of_policy :role_name'_of_policy'
\set pd_policy :role_name'_pd_policy'

DROP POLICY IF EXISTS :"em_policy" on :"cell_schema".encounter_mapping;
DROP POLICY IF EXISTS :"pm_policy" on :"cell_schema".patient_mapping;
DROP POLICY IF EXISTS :"vd_policy" on :"cell_schema".visit_dimension;
DROP POLICY IF EXISTS :"of_policy" on :"cell_schema".observation_fact;
DROP POLICY IF EXISTS :"pd_policy" on :"cell_schema".patient_dimension;
