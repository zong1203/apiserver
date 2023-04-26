# API Documents

## Server IP:https://125.229.111.81

___

## Account

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

### /api/token_verify/

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

### /api/userfile/search_by_account/

<details><summary>click me</summary>

- function
  - This API is used to return specified parameters. The query format is "?account={your account name}". If no parameters are provided, it will return all accounts when directly GET "api/userfile/search_by_account". This is for testing purposes only. After formal deployment, access will be restricted to local GET requests only.
- method
  - GET
- Request header
```json
None
```
- Response body
```json
#Return one or multiple user data in the form of an array depending on whether parameters are added.Format as follows.
{
    "id": your id(integer),
    "Account": "your account",
    "Password": "your password(SHA-256)",
    "Name": "your name",
    "Email": "your email",
    "Phonenumber": "your phone number",
    "StudentID": "your StudentID",
    "Introduction": "your Introduction",
    "Favorite": "your Favorite",
    "Profliephoto": "The file path of your personal profilephoto."
}
```

</details>

___

## Commodity

### /api/commodity/search_by_commodity/

<details><summary>click me</summary>

- function
  - The usage of this API is the same as "api/userfile/search_by_account".The query format is "?commodity={your commodity name}"
- method
  - GET
- Request header
```json
None
```
- Response body
```json
#Return one or multiple user data in the form of an array depending on whether parameters are added.Format as follows.
{
    "id": your id(integer),
    "Launched": launch status,
    "Img1": "name of image(Cannot be NULL)",
    "Img2": "name of image(Can be NULL)",
    "Img3": "name of image(Can be NULL)",
    "Img4": "name of image(Can be NULL)",
    "Img5": "name of image(Can be NULL)",
    "Name": "name of commodity",
    "Deacription": "Deacription",
    "Price": "Price",
    "Amount": "Amount",
    "Position": "Location of the commodity",
    "Account": "Who uploaded this product"
}
```

</details>

### /commodity/upload/

<details><summary>click me</summary>

- function
  - This API is used to upload product information. The request body must include the "Img1" field, and "Img2" to "Img5" are optional. In addition, the "Authorization" header must be included in the request header to store your JWT token.
  - Because this API's implementation is different from the previous search function, it is not possible to add "api/" at the beginning of the URL. We are currently looking for a solution to this issue.
- method
  - POST
- Request header
```json
Authorization:your jwt token
```
- Request body
```json
{
    "name":"your commodity name",
    "description":"description",
    "price":"your price",
    "amount":"commodity amount",
    "position":"where is your commodity",
    "img1":"the field is necessary (use base64 to store)",
    "img2":"optional",
    "img3":"optional",
    "img4":"optional",
    "img5":"optional"
}
```
- Response body
```json
#If there are no issues with the uploaded data.
{
    "success": true,
    "message": "成功上傳商品"
}
```
```json
#If there are no issues with the uploaded data.
{
    "success": false,
    "message": "缺少必要資料"
}
```
</details>

___

## Picture

### /image/get/

<details><summary>click me</summary>

- function
  - This API is used to retrieve images.The query format is "?picture_name={your picture name}".
- method
  - GET
- Request header
```json
None
```
- HttpResponse
```json
#If your image exists, it will return your image. Otherwise, it will report an error.
```
</details>