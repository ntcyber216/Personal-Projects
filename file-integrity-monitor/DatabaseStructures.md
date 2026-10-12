| column_name | data_type | purpose |
|-------------|-----------|---------|
| id          | INTEGER   | unique identifier |
| filepath    | TEXT      | path of monitored file |
| hash        | TEXT      | SHA-256 hash value |
| timestamp   | TEXT      | when it was hashed |
| status      | TEXT      | active or inactive |

| column_name | data_type | purpose |
|-------------|-----------|---------|
| id          | INTEGER   | unique identifier |
| timestamp   | TEXT      | when the log was entered |
| message     | TEXT      | the actual log |
| event       | TEXT      | the type of event (file modification, scan, baseline creation, etc) |

| column_name | data_type | purpose |
|-------------|-----------|---------|
| id          | INTEGER   | unique identifier |
| interval    | TEXT      | the user defined time interval of checks |
| timestamp   | TEXT      | when this config was created |
| filepath    | TEXT      | the path the user wishes to monitor|
