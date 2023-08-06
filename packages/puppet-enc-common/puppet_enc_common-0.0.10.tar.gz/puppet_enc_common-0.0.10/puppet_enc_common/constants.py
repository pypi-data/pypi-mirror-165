# Flash Message Classes
FLASH_SUCCESS = "alert-success"
FLASH_ERROR = "alert-danger"
FLASH_WARNING = "alert-warning"

# Fact Types
PUPPETDB_FACT = 1
CUSTOM_FACT = 2

# Group Types
STATIC_GROUP = 1
DYNAMIC_GROUP = 2

# User Constants
LOCAL_USER = 1
AZURE_AD_USER = 2
API_USER = 3
USER_ENABLED = 1
USER_DISABLED = 0
MFA_ENABLED = 1
MFA_DISABLED = 0

PUPPETDB_FACT_LIST = [
    'osfamily',
    'os_name',
    'release_full',
    'release_major',
    'release_minor',
    'release_description',
    'kernelrelease',
    'kernelmajversion'
]

# Name of common role item in database
COMMON_ROLE = 'COMMON'

# Path to local configuration file
CONFIG_FILE = '/etc/puppetencconfig.yml'

# From API
groups_properties = ['id', 'name', 'type']
nodes_properties = ['id', 'name', 'environment', 'hostname', 'enabled']
roles_properties = ['id', 'name']
facts_properties = ['id', 'name', 'has_valid_values']
fact_values_properties = ['id', 'fact_id', 'value']
fact_node_value_properties = ['fact_name', 'fact_value', 'fact_type']
config_properties = ['name', 'kill_switch']
container_properties = ['name', 'last_status', 'last_runtime']
override_properties = ['hiera_variable', 'hiera_value']

# From API
TOKEN_DURATION = 120
