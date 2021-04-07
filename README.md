# Cloud Stories

Telling stories about the future by watching clouds.

![](https://data.whicdn.com/images/208932206/original.gif)

## Running
Run the main programme:
```
  $ pipenv run cli main
```

List all available options:
```
  $ pipenv run cli
```

## Install
Uses [pipenv](https://pipenv.pypa.io/en/latest/)

```
  $ pipenv --python 3.8
  $ pipenv install
  $ pipenv install --dev
```


## Dataset
https://www.dropbox.com/s/ff65gd4n4deslem/cloud-stories.zip?dl=0

## Convert TensorFlow checkpoints to PyTorch model
```
  transformers-cli convert \
    --model_type gpt2 \
    --tf_checkpoint ./data \ 
    --pytorch_dump_output ./data
```
