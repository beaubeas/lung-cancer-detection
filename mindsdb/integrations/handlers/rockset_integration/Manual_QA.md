# Welcome to the MindsDB Manual QA Testing for Rockset Handler

> **Please submit your PR in the following format after the underline below `Results` section. Don't forget to add an underline after adding your changes i.e., at the end of your `Results` section.**

**1. Testing CREATE DATABASE**

```
CREATE DATABASE rockset_db;
```
WITH ENGINE = "rockset",

```
PARAMETERS = {
      "host":"https://api.use1a1.rockset.com",
      "port":"3306",
      "user":"<user>",
      "password":"<password>",
      "database":"test"
    };
```

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
- [ ] Works Great 💚 (This means that all the steps were executed successfully and the expected outputs were returned.)
- [ ] There's a Bug 🪲 [Issue Title](URL To the Issue you created) ( This means you encountered a Bug. Please open an issue with all the relevant details with the Bug Issue Template)
