# Capt’n python client 2022.8.0rc0

## Docs

Full documentation can be found at the following link:

- <a href="https://docs.captn.ai" target="_blank">https://docs.captn.ai/</a>


## How to install

If you don't have the captn library already installed, please install it using pip.


```console
pip install captn-client
```

## How to use

To access the captn service, you must create a developer account. Please fill out the signup form below to get one:

- [https://bit.ly/3I4cNuv](https://bit.ly/3I4cNuv)

Upon successful verification, you will receive the username/password for the developer account in an email. 

Finally, you need an application token to access all the APIs in captn service. Please call the `Client.get_token` method with the username/password to get one. 

You can either pass the username, password, and server address as parameters to the `Client.get_token` method or store the same in the **CAPTN_SERVICE_USERNAME**, **CAPTN_SERVICE_PASSWORD**, and **CAPTN_SERVER_URL** environment variables.

After successful authentication, the captn services will be available to access.

As an extra layer of security, we also support Multi-Factor Authentication (MFA) for generating tokens.

Multi-Factor Authentication (MFA) can be used to help protect your account from unauthorized access by requiring you to enter an additional code when you request a new token. 

Once authenticated successfully, activating MFA for your account is a simple two step process:

1. Enable MFA for your account by calling `User.enable_mfa` method which will generate a QR code. You can then use an authenticator app, such as Google Authenticator to scan the QR code.

2. Activate the MFA by calling `User.activate_mfa` method and passing the dynamically generated six-digit verification code from the authenticator app.

Once MFA is successfully activated, you need to pass the dynamically generated six-digit verification code along with the username/password to `Client.get_token` method for generating new tokens.

You can also disable MFA for you account anytime by calling `User.disable_mfa` method.

For more information, please check:

- [Tutorial](https://docs.captn.ai/Tutorial/) with more elaborate example, and

- [API](https://docs.captn.ai/API/client/Client/) with reference documentation.


Below is a minimal example explaining how to load the data, train a model and make predictions using captn services. 

!!! info

	In the below example, the username, password, and server address are stored in **CAPTN_SERVICE_USERNAME**, **CAPTN_SERVICE_PASSWORD**, and **CAPTN_SERVER_URL** environment variables.


### 0. Get token


```
from captn.client import Client, DataBlob, DataSource

Client.get_token()
```

### 1. Connect and preprocess data

In our example, we will be using the captn APIs to load and preprocess a sample CSV file stored in an AWS S3 bucket. 


```
data_blob = DataBlob.from_s3(
    uri="s3://test-airt-service/sample_gaming_130k/"
)
data_blob.progress_bar()

```

The sample data we used in this example doesn't have the header rows and their data types defined. 

The following code creates the necessary headers along with their data types and reads only a subset of columns that are required for modeling:



```
prefix = ["revenue", "ad_revenue", "conversion", "retention"]
days = list(range(30)) + list(range(30, 361, 30))
dtype = {
    "date": "str",
    "game_name": "str",
    "platform": "str",
    "user_type": "str",
    "network": "str",
    "campaign": "str",
    "adgroup": "str",
    "installs": "int32",
    "spend": "float32",
}
dtype.update({f"{p}_{d}": "float32" for p in prefix for d in days})
names = list(dtype.keys())

kwargs = {"delimiter": "|", "names": names, "parse_dates": ["date"], "usecols": names[:42], "dtype": dtype}
```

Finally, the above variables are passed to the `DataBlob.from_csv` method which preprocesses the data and stores it in captn server.


```
data_source = data_blob.from_csv(
    index_column="game_name",
    sort_by="date",
    **kwargs
)

data_source.progress_bar()
```


```
print(data_source.head())
```

### 2. Training


```
# Todo
```
