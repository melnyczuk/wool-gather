# Wool-gather

Teaching my computer to daydream.

![](https://data.whicdn.com/images/208932206/original.gif)

This project is an electron app that spawns a python app. 

The two communicate to via websockets.

It uses yarn for frontend dependencies and [pipenv](https://pipenv.pypa.io/en/latest/) for python dependencies. 

If you're using npm, replace `yarn` with `npm` in the commands below.

## Running
Run the main programme Electron app:
```
  $ yarn start
```
This will also spawn the python websockets server

There's also a CLI for the python app:
```
  $ pipenv run cli
```

## Development
You need to install the dev dependencies to run the pipenv commands format, lint and typecheck:
```
  $ pipenv install --dev
```

You can run the server and front end separately. 

Simple run the python server in a seperate terminal before starting the Electron app:
```
  $ pipenv run server
  $ yarn start
```

This is useful for development that the frontend loads much faster because the backend models don't need to be reloaded.

It also means that the server log messages are visible.

## Install
```
  $ yarn install
```

This also installs the pipenv dependencies.

## Dataset
```
wget -O wool-gather.zip \
"https://www.dropbox.com/s/ff65gd4n4deslem/wool-gather.zip?dl=0" 
```

## Convert TensorFlow checkpoints to PyTorch model
```
  transformers-cli convert \
    --model_type gpt2 \
    --tf_checkpoint ./data \ 
    --pytorch_dump_output ./data
```
