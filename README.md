# API Documents

## Server IP:https://125.229.111.81
## 中英混雜是因為我沒空懶得翻譯了,之後再改回中文
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

### /api/commodity/my_commodity/

<details><summary>click me</summary>

- function
  - 取得這個帳號的所有商品,需使用jwt
- method
  - GET
- Request header
```json
None
```
- Response body
```json
#Return one or multiple user data in the form of an array.
{
    "id": your id(integer),
    "Account": "who launched this commodity",
    "Launched": launch state(boolean),
    "Name": "commodity's name",
    "Description": "commodity's description",
    "Price": "commodity's price",
    "Amount": "commodity's amount",
    "Position": "where is the commodity",
    "Image": [
      "an array of picture name",
      "maxmium is 5 picture",
      "at least 1"
    ]
}
```
</details>

### /api/commodity/launch/

<details><summary>click me</summary>

- function
  - 更改商品上下架狀態,需使用jwt,並且在網址列加上目標商品的id,格式為"/api/commodity/launch/?id={商品id}"
- method
  - POST
- Request header
```json
Authorization:your jwt token
```
- Request body
```json
{
  "launched": launch state
}
```
- Response body
```json
#成功
{
  "success": true,
  "message": "ok"
}
```
```json
#找不到商品
{
  "success": false,
  "message": "can't find commodity with this id"
}
```
```json
#非商品擁有者
{
  "success": false,
  "message": "this commodity is not yours"
}
```
</details>

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
    "Account": "who launched this commodity",
    "Launched": launch state(boolean),
    "Name": "commodity's name",
    "Description": "commodity's description",
    "Price": "commodity's price",
    "Amount": "commodity's amount",
    "Position": "where is the commodity",
    "Image": [
      "an array of picture name",
      "maxmium is 5 picture",
      "at least 1"
    ]
}
```

</details>

### /api/commodity/commodity_CRUD/

<details><summary>click me</summary>

- function
  - 這支api用來對商品做CRUD,header內必須加上jwt token.
  - 請注意,搜尋和主頁大量獲取商品資訊勿使用此api
  - RUD都需在網址列加上id的參數,格式為"/api/commodity/commodity_CRUD/?id="
- method
  - GET,POST,PUT,DELETE
#### GET
- Request header
```json
Authorization:your jwt token
```
- Response body
```json
#正常情況.
{
    "id": your id(integer),
    "Account": "who launched this commodity",
    "Launched": launch state(boolean),
    "Name": "commodity's name",
    "Description": "commodity's description",
    "Price": "commodity's price",
    "Amount": "commodity's amount",
    "Position": "where is the commodity",
    "Image": [
      "an array of picture name",
      "maxmium is 5 picture",
      "at least 1"
    ]
}
```
```json
#如果沒有在網址加上id.
{
  "success": false,
  "message": "Please add parameters to the URL."
}
```
```json
#如果無法透過這個id找到商品.
{
  "success": false,
  "message": "can't find commodity with this id"
}
```
```json
#如果這個商品不是你的.
{
  "success": false,
  "message": "this commodity is not yours"
}
```
#### POST
- Request header
```json
Authorization:your jwt token
```
- Request body
```json
{
    "name":"your commodity name",
    "launched":"launched state",
    "description":"description",
    "price":"your price",
    "amount":"commodity amount",
    "position":"where is your commodity",
    "image":["至少一張圖片","可選","可選","可選","最多五張圖片"]
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
#如果POST的資料有缺漏.
{
    "success": false,
    "message": "缺少必要資料"
}
```
#### PUT
- 網址列的id就是要變更的商品
- Request header
```json
Authorization:your jwt token
```
- Request body
```json
{
    "name":"your commodity name",
    "launched":"launched state",
    "description":"description",
    "price":"your price",
    "amount":"commodity amount",
    "position":"where is your commodity",
    "remain_image":["要留下的圖片名稱,請注意不要輸入不存在的檔名","image和remain_image最多總和只能五張圖片","多餘的會從remain_image的最後面開始刪掉"],
    "image":["至少一張圖片","可選","可選","可選","最多五張圖片"]
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
#如果POST的資料有缺漏.
{
    "success": false,
    "message": "缺少必要資料"
}
```
```json
#如果這個商品不是你的.
{
  "success": false,
  "message": "this commodity is not yours"
}
```
#### DELETE
- 網址列的id就是要刪除的商品
- Request header
```json
Authorization:your jwt token
```
- Request body
```json
None
```
- Response body
```json
#If there are no issues
{
    "success": true
}
```
```json
#如果無法根據id找到商品.
{
    "success": false,
    "message": "can't find commodity with this id"
}
```
```json
#如果這個商品不是你的.
{
  "success": false,
  "message": "this commodity is not yours"
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