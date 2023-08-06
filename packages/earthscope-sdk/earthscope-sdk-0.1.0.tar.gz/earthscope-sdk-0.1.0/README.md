# EarthScope SDK

An SDK for authenticating with the EarthScope API

## Getting Started

### USAGE

1. (Optional) Suggest setting up and activating a python virtual environment so as not to clutter your system python

   ```shell
   python3 -m venv venv
   . venv/bin/activate
   ```

2. Install earthscope-sdk

   ```shell
   pip install earthscope-sdk
   ```
   For developers:
   ```bash
   pip -e install earthscope-sdk[dev]
   ```
   
3. Create required subclasses

   To use the **Device Authorization Flow** you will need to create a subclass of the DeviceCodeFlow class. Similarly, to use
   the **Machine-to-Machine Client Credentials Flow** you will need to create a subclass of the ClientCredientialFlow class.
   Implementing the following methods in the subclass is required:
   * `load_tokens` should implement the ability to load saved tokens
   * `save_tokens` should implement the ability to save tokens locally
   
   additionally for DeviceCodeFlow only:
   * `prompt_user` should provide the user with the SSO authorization uri

   You will need to instantiate your subclass with the following instance attributes:

   For DeviceCodeFlow:
   * `audience`, `domain`, `client_id`, and `scope`.

   For ClientCredentialsFlow:
   * `audience`, `client_credentials`, and `domain`.
   
      where client_credentials contains the machine-to-machine `client_id` and `client_secret`.

   These values are all obtained from [Auth0](https://manage.auth0.com/).
4. Use the SDK

   You can now use the subclasses to define actions such as logging in/out, retrieving or refreshing access tokens, etc...

   Additionally, once your subclasses have been instantiated, you can use your access token to retrieve
   your user information as well as anonymous user information using the earthscope_sdk.user.user functions.
   

To see an example of an application using this SDK, check out the [EarthScope CLI GitLab](https://gitlab.com/earthscope/public/earthscope-cli).
