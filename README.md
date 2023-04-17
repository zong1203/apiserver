# API Documents

## Server IP:https://125.229.111.81

### /api/login/

<details><summary>click me</summary>

- function
  - to get jwt token.
- method
  - POST
- Request body
```json
{
    "account" : "your account",
    "password" : "your password"
}
```
- Response body
```json
#if login success
{
    "success": true,
    "message": "your jwt token",
    "account": "your account"
}
```
```json
#if account doesn't exist
{
    "success": false,
    "message": "尚未註冊",
    "account": "your account"
}
```
```json
#If the password is incorrect
{
    "success": false,
    "message": "登入失敗",
    "account": "your account"
}
```

</details>

### /api/signup/

<details><summary>click me</summary>

- function
  - to sign up.
- method
  - POST
- Request body
```json
{
    "account":"your account",
    "password":"your password",
    "nickname":"your nickname",
    "mail":"your email address",
    "phone":"your phone number"
}
```
- Response body
```json
#If the registration is successful.
{
    "success": true,
    "message": "註冊成功"
}
```
```json
#If the account has already been registered.
{
    "success": false,
    "message": "帳號已經被註冊"
}
```
```json
#If there is missing information in the requested body.
{
    "success": false,
    "message": "註冊失敗"
}
```

</details>

### /api/signup/

<details><summary>click me</summary>

- function
  - Verify the legality of the JWT token, with a validity period of 10 days. As the verification has been performed during acquisition, the existence of the account and password will not be verified here.
- method
  - GET
- Request header
```json
Authorization:your jwt token
```
- Response body
```json
#If the JWT token is within its validity period of 10 days.
{
    "success": true,
    "account": "your account"
}
```
```json
#If the JWT token has expired or the 'Authorization' field cannot be obtained from the header.
{
    "success": false,
    "account": "your account"
}
```

</details>