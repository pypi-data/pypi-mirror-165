## Package "dep-spec"
Package for define service specifications.

#### Service options
Name | Default  | Description
--- | --- |---
SERVICE_NAME | "Service" | Verbose service name
SERVICE_HOST | "0.0.0.0" | Service host
SERVICE_PORT | 6969 | Service port
SERVICE_ENTRYPOINT | "main:app" | App entrypoint
SERVICE_SCHEME_SECURE | "https" | Default secure proto
SERVICE_SCHEME_INSECURE | "http" | Default insecure proto

#### Maintenance options
Name | Default  | Description
--- | --- |---
DEBUG | false | Is debug
ENV_FILE | ".env" | Default dot env file name in app_dir
ENVIRONMENT | "unknown" | Environment [testing, develop, production ... ] 
LOG_LEVEL | "debug" | Log level [debug, warning, error, ... ]
LOG_CONFIG_PATH | null | Overload log config path
SENTRY_DSN | null | Auto-skip for dev or testing environment
DIR_ASSETS | {app_dir}/assets | Assets service path

#### Policy options
Name | Default  | Description
--- | --- |---
POLICY_SERVICE_WORKERS | 1 | Service workers
POLICY_REQUEST_TIMEOUT | 60 | Request timeout default
POLICY_REQUEST_RETRY_MAX | 3 | Request retry max default
POLICY_SCHEDULER_ENABLED | false | Scheduler enabled
POLICY_SCHEDULER_PERSISTENT | false | Scheduler persistent or in-memory
POLICY_SCHEDULER_WORKERS | 1 | Scheduler workers
POLICY_SCHEDULER_INSTANCES | 5 | Scheduler max instances
POLICY_SCHEDULER_HOST | "localhost" | Scheduler storage redis host
POLICY_SCHEDULER_PORT | 6379 | Scheduler storage redis port
POLICY_SCHEDULER_DB | 9 | Scheduler storage redis db
POLICY_SCHEDULER_COALESCE | false | Scheduler coalesce

#### I18N Options
Name | Default  | Description
--- | --- |---
I18N_LANG | "en" | default language
I18N_SUPPORT | "ru" | support languages by default
I18N_LOCALES | "en_US ru_RU" | all locales
