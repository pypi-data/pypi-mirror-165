-- Language: psql scripting language (not to be confused with plpgsql!)
BEGIN;

-- Include init script
\ir init.sql

-- Set policy names from variables
\set em_policy :role_name'_em_policy'
\set pm_policy :role_name'_pm_policy'
\set vd_policy :role_name'_vd_policy'
\set of_policy :role_name'_of_policy'
\set pd_policy :role_name'_pd_policy'

-- drop resources before creating them
\ir drop.sql
-- run RLS script
\ir rls.sql
-- create savepoint before PgTAP tests
SAVEPOINT before_tests;
-- run tests
\ir test.sql

-- Get test summary from PgTAP's finish function
-- Returns NULL if all tests pass, else something like:
-- '# Looks like you failed 1 test of 28'
SELECT * FROM finish();

-- Evaluate failure/success to bool into variable 'failure'
SELECT COUNT(*) > 0 AS failure FROM finish()
-- Store previous query output in psql client
\gset

-- rollback anything from test.sql anyway (temp tables etc.)
ROLLBACK TO before_tests;
-- If errors occured in tests
\if :failure
    \echo ERROR: Tests have failed!
    -- Rollback everything
    ROLLBACK;
\else
    \echo NOTICE: All tests passed, committing!
    -- Commit (execute) transactions
    COMMIT;
\endif
