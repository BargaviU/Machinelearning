
# net_meet

A repository for learning LangChain by building a generative ai application.

This is a web applicaiton crawling Linkedin & Twitter data about a person an customize an ice breaker with them. 


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PYTHONPATH=/{YOUR_PATH_TO_PROJECT}/net_meet'

`OPENAI_API_KEY`

`PROXYCURL_API_KEY`

`SERPAPI_API_KEY`

`TWITTER_API_KEY`

`TWITTER_API_SECRET`

`TWITTER_ACCESS_TOKEN`

`TWITTER_ACCESS_SECRET`
## Run Locally

Clone the project

Go to the project directory

```bash
  cd net_meet
```

Install dependencies

```bash
  pipenv install
```

Start the flask server

```bash
  pipenv run app.py
```


## Running Tests

To run tests, run the following command

```bash
  pipenv run pytest .
```
