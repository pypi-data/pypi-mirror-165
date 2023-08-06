WAIT_TIME = 1

READY_SESSION_STATUS = "READY"
PROVISIONING_SESSION_STATUS = "PROVISIONING"
NOT_FOUND_SESSION_STATUS = "NOT_FOUND"
FAILED_SESSION_STATUS = "FAILED"
UNHEALTHY_SESSION_STATUS = [NOT_FOUND_SESSION_STATUS, FAILED_SESSION_STATUS]

ERROR_STATEMENT_STATUS = "ERROR"
CANCELLED_STATEMENT_STATUS = "CANCELLED"
AVAILABLE_STATEMENT_STATUS = "AVAILABLE"
FINAL_STATEMENT_STATUS = [ERROR_STATEMENT_STATUS, CANCELLED_STATEMENT_STATUS, AVAILABLE_STATEMENT_STATUS]
SQL_CELL_MAGIC = "%%sql"

CELL_MAGICS = {"%%configure", "%%sql"}

VALID_GLUE_VERSIONS = {"2.0","3.0"}

CHINA_REGIONS = {"cn-north-1", "cn-northwest-1"}

HELP_TEXT = f'''
Available Magic Commands

## Sessions Magics
%help | Return a list of descriptions and input types for all magic commands. 
%profile | String | Specify a profile in your aws configuration to use as the credentials provider.
%region | String | Specify the AWS region in which to initialize a session | Default from ~/.aws/configure
%idle_timeout | Int | The number of minutes of inactivity after which a session will timeout. The default idle timeout value is 2880 minutes (48 hours).
%session_id | Returns the session ID for the running session. 
%session_id_prefix | String | Define a String that will precede all session IDs in the format [session_id_prefix]-[session_id]. If a session ID is not provided, a random UUID will be generated.
%status | Returns the status of the current Glue session including its duration, configuration and executing user / role.
%list_sessions | Lists all currently running sessions by name and ID.
%stop_session | Stops the current session.
%glue_version | String | The version of Glue to be used by this session. Currently, the only valid options are 2.0 and 3.0. The default value is 2.0.
%streaming | String | Changes the session type to Glue Streaming. 
%etl | String | Changes the session type to Glue ETL. 

## Glue Config Magics
%%configure | Dictionary | A json-formatted dictionary consisting of all configuration parameters for a session. Each parameter can be specified here or through individual magics.
%iam_role | String | Specify an IAM role ARN to execute your session with. | Default from ~/.aws/configure
%number_of_workers | int | The number of workers of a defined worker_type that are allocated when a job runs. worker_type must be set too. The default number_of_workers is 5.
%worker_type | String | Standard, G.1X, or G.2X. number_of_workers must be set too. The default worker_type is G.1X.
%security_config | String | Define a Security Configuration to be used with this session. 
%connections | List | Specify a comma separated list of connections to use in the session.
%additional_python_modules | List | Comma separated list of additional Python modules to include in your cluster (can be from Pypi or S3).
%extra_py_files | List | Comma separated list of additional Python files From S3.
%extra_jars | List | Comma separated list of additional Jars to include in the cluster.
%spark_conf | String | Specify custom spark configurations for your session. E.g. %spark_conf spark.serializer=org.apache.spark.serializer.KryoSerializer

## Action Magics
%%sql | String | Run SQL code. All lines after the initial %%sql magic will be passed as part of the SQL code. 
'''

OWNER_TAG = "owner"
GLUE_STUDIO_NOTEBOOK_IDENTIFIER = "GlueStudioNotebook"

# GlueStudio Env Variables
REQUEST_ORIGIN = "request_origin"
REGION = "region"
SESSION_ID = "session_id"
GLUE_ROLE_ARN = "glue_role_arn"
GLUE_VERSION = "glue_version"
USER_ID = "userId"
