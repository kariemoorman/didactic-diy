
/* --- Create Group Roles ---- */ 

CREATE ROLE administrator SUPERUSER;
CREATE ROLE dba;
CREATE ROLE reader;
CREATE ROLE dev_api CONNECTION LIMIT <integer>;
CREATE ROLE api CONNECTION LIMIT <integer>;

/* --- Create User Roles ---- */ 

CREATE ROLE <username_a> inherit LOGIN PASSWORD '<password>' VALID UNTIL 'timestamp';
CREATE ROLE <username_b> inherit LOGIN PASSWORD '<password>' VALID UNTIL 'timestamp';
CREATE ROLE <username_c> inherit LOGIN PASSWORD '<password>' VALID UNTIL 'timestamp';
CREATE ROLE <username_d> inherit LOGIN PASSWORD '<password>' VALID UNTIL 'timestamp';
CREATE ROLE <username_e> inherit LOGIN PASSWORD '<password>' VALID UNTIL 'timestamp';

/* --- GRANT permissions on Database Schema & Tables to Groups & User(s) --- */ 

GRANT ALL ON reddit.* TO administrator;
GRANT CREATEDB ON reddit.* TO dba;
GRANT SELECT ON reddit.* TO reader;
GRANT INSERT, UPDATE, DELETE, SELECT ON reddit.* TO dev_api;
GRANT INSERT, SELECT ON reddit.* TO api;

/* --- Assign User(s) to Group(s) --- */

GRANT administrator TO <username_a>;
GRANT dba TO <username_b>;
GRANT reader TO <username_c>;
GRANT dev_api TO <username_d>;
GRANT api TO <username_e>;
