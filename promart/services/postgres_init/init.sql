-- productdb üçün icazələr
ALTER SCHEMA public OWNER TO productuser;
GRANT ALL PRIVILEGES ON DATABASE productdb TO productuser;
GRANT CREATE ON SCHEMA public TO productuser;
GRANT ALL ON SCHEMA public TO productuser;
GRANT ALL ON ALL TABLES IN SCHEMA public TO productuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO productuser;

-- userdb yaradın və icazələri təyin edin
CREATE DATABASE userdb OWNER productuser;
\c userdb
ALTER SCHEMA public OWNER TO productuser;
GRANT ALL PRIVILEGES ON DATABASE userdb TO productuser;
GRANT CREATE ON SCHEMA public TO productuser;
GRANT ALL ON SCHEMA public TO productuser;
GRANT ALL ON ALL TABLES IN SCHEMA public TO productuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO productuser;