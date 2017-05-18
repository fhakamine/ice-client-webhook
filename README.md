# ice-client-webhook

This [Api.ai Webhook](https://docs.api.ai/docs/webhook) makes Ice customers happy.

![Ice Icon](img/IceIcon_120px.png)

## Run this Webhook

### Pre-reqs
1. Deploy the ice-resource-server: https://github.com/fhakamine/ice-resource-server

### Option 1: Heroku

1. Click [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
2. Login or create your Heroku account.
3. After deployment, go to settings.
4. Update the **PROMOS_API** with the URL for the Promos API. -- for example, https://ice-rs-fredericohakamine.herokuapp.com.

### Option 2: In my house

1. Install `git` and `python` in your computer.
2. Clone this repo:
    `$ git clone git@github.com/fhakamine/ice-client-webhook.git`

3. Install Node dependencies:
    `heroku local`

4. Use a solution to expose this url on the internet, such as `ngrok.io`.
