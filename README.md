# Wool-gather

Teaching my computer to daydream.

![](https://data.whicdn.com/images/208932206/original.gif)

## Running
Run the main programme Electron app:
```
  $ pipenv run websockets
  $ yarn start
```

There's also a CLI for the core app:
```
  $ pipenv run cli
```

## Install
Uses [pipenv](https://pipenv.pypa.io/en/latest/)

```
  $ pipenv --python 3.8
  $ pipenv install
  $ pipenv install --dev
  $ yarn install
```

## Dataset
https://www.dropbox.com/s/ff65gd4n4deslem/wool-gather.zip?dl=0

## Convert TensorFlow checkpoints to PyTorch model
```
  transformers-cli convert \
    --model_type gpt2 \
    --tf_checkpoint ./data \ 
    --pytorch_dump_output ./data
```
