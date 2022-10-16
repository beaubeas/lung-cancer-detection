# Welcome to the MindsDB Manual QA Testing for Databricks Handler

> **Please submit your PR in the following format after the underline below `Results` section. Don't forget to add an underline after adding your changes i.e., at the end of your `Results` section.**

## Testing Databricks Handler with [Dataset Name](URL to the Dataset)

**1. Testing CREATE DATABASE**

```
CREATE DATABASE databricks_datasource
WITH ENGINE='databricks',
PARAMETERS={
  "server_hostname": "adb-2739211854327427.7.azuredatabricks.net",
  "http_path": "sql/protocolv1/o/2739211854327427/1008-130317-9mq6rcp6",
  "access_token": "dapib9c127dc406d9ddb9d42a4f170f398df-3"
};
```

![CREATE_DATABASE]()

**2. Testing CREATE PREDICTOR**

```
COMMAND THAT YOU RAN TO CREATE PREDICTOR.
```

![CREATE_PREDICTOR](Image URL of the screenshot)

**3. Testing SELECT FROM PREDICTOR**

```
COMMAND THAT YOU RAN TO DO A SELECT FROM.
```

![SELECT_FROM](Image URL of the screenshot)

### Results

Drop a remark based on your observation.
- [ ] Works Great 💚 (This means that all the steps were executed successfuly and the expected outputs were returned.)
- [ ] There's a Bug 🪲 [Issue Title](URL To the Issue you created) ( This means you encountered a Bug. Please open an issue with all the relevant details with the Bug Issue Template)

---