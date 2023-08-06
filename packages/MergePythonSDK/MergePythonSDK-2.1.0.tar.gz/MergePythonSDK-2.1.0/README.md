# Merge-SDK-Python

The Python SDK for accessing various Merge Unified APIs. We use the following dependencies:

* urllib3 for http communication
* pytest for tests
* NO logging, aside from some `print` in tests

## Build

You can find the latest published pypi package [here]()

## Usage

For all examples, you can refer to the [BasicTest class](/test/basic_test.py) in this
repository.

### Plain call

```python
from MergePythonSDK.accounting.api.invoices_api import InvoicesApi
from MergePythonSDK.shared import Configuration, ApiClient

# Swap YOUR_API_KEY below with your production key from:
# https://app.merge.dev/configuration/keys
configuration = Configuration()
configuration.access_token = "YOUR_API_KEY"
configuration.api_key_prefix['tokenAuth'] = 'Bearer'
# Swap YOUR-X-ACCOUNT-TOKEN below with your production key from:
# https://app.merge.dev/linked-accounts/account/{ACCOUNT_ID}/overview
configuration.api_key['accountTokenAuth'] = 'YOUR-X-ACCOUNT-TOKEN'

with ApiClient(configuration) as api_client:
    accounting_invoices_api_instance = InvoicesApi(api_client)
    api_response = accounting_invoices_api_instance.invoices_list()
```

### Remote Fields

Merge attempts to map as many enum values as possible from integrations into a single normalized set of enum values.
However, there will always be edge cases where the default mapping does not suit our callers. In order to get the raw
value, you can pass in the name of the enum parameter into the remoteFields request property:

```python
from MergePythonSDK.hris.api.employees_api import EmployeesApi
from MergePythonSDK.shared import Configuration, ApiClient

# Swap YOUR_API_KEY below with your production key from:
# https://app.merge.dev/configuration/keys
configuration = Configuration()
configuration.access_token = "YOUR_API_KEY"
configuration.api_key_prefix['tokenAuth'] = 'Bearer'
# Swap YOUR-X-ACCOUNT-TOKEN below with your production key from:
# https://app.merge.dev/linked-accounts/account/{ACCOUNT_ID}/overview
configuration.api_key['accountTokenAuth'] = 'YOUR-X-ACCOUNT-TOKEN'

with ApiClient(configuration) as api_client:
    hris_employees_api_instance = EmployeesApi(api_client)
    _id = "EMPLOYEE ID HERE"
    employee_remote_field = hris_employees_api_instance.employees_retrieve(
        _id, remote_fields="gender")
```

### Expand

The expand parameter can be used during GET requests to fetch the related objects in your response body.
For example, if you sent a request for GET /employees, you can use the expand parameter on Teams. This 
will fetch the associated Team data for each given employee. The Employee objects will be returned with
the corresponding Teams objects instead of the default List<UUID>. In the below example, we expand the 
employments property of HRIS Employee.

```python
from MergePythonSDK.shared import Configuration, ApiClient
from MergePythonSDK.hris.api.employees_api import EmployeesApi

configuration = Configuration()
configuration.access_token = "YOUR_API_KEY_HERE"
configuration.api_key_prefix['tokenAuth'] = 'Bearer'
configuration.api_key['accountTokenAuth'] = 'YOUR_X_ACCOUNT_TOKEN_HERE'
with ApiClient(configuration) as api_client:
    hris_employees_api_instance = EmployeesApi(api_client)
    try:
        # Test expands
        _id = "YOUR_EMPLOYEE_ID_HERE"
        employee_expands = hris_employees_api_instance.employees_retrieve(
          _id, expand="employments"
        )
        assert employee_expands.employments.employee == employee_expands.id
```