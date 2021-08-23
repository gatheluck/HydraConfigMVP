# Hydra Config MVP

In this repo, two different types of Hydra config managing are shown.
(If you do not know about Hydra, please take a look at [origial docs page](https://hydra.cc/).) 

- Type 1: This type is config management which is used by [official Hydra tutorial](https://hydra.cc/docs/tutorials/intro).
- Type 2: This type is config management which is used by [VISSL](https://github.com/facebookresearch/vissl) (which is OSS lib for self-supervised learning).

## How to setup
To run the codes in this repo, Python 3.8 or later and [poetry](https://python-poetry.org/) are required. To prevent to break your local environment, using virtual environment like pyenv, conda, virtualenv is recommended.


Here, some example codes to setup are shown.
```
# please start from root dir of this repo

$ cd type1
$ pyenv local 3.9.2  # use pyenv to set up virtual environment
$ pip3 install poetry  # install poerty
$ poetry install  # poetry setting up all about type1

$ cd ../type2
$ pyenv local 3.9.2  # use pyenv to set up virtual environment
$ pip3 install poetry  # install poerty
$ poetry install  # poetry setting up all about type2
```

## Run the code
If you successfully finish setup, you can try the code like bellow.

```
$ cd type1
$ poetry run python src/train.py  # all loaded config values are shown.
$ poetry run python src/train.py --help  # hydra will show list of overwritable configs. 

$ cd type2
$ poetry run python src/train.py  # all loaded config values are shown.
$ poetry run python src/train.py --help  # hydra will show list of overwritable configs. 
``` 

## Situation
In this MVP, considering to specify only configs about `optimizer` and `scheduler` like bellow.

- optimizer
    - sgd
        - lr
        - momentum
        - weight_decay
        - dampening
        - nesterov

- scheduler
    - cosine_annealing_lr
        - T_max
        - eta_min
        - last_epoch
    - reduce_lr_on_plateau
        - mode
        - factor
        - patience
        - threshold
        - threshold_mode
        - cooldown
        - min_lr
        - eps

For all items, default values are set. And some config values are overwritten from default value by `my_train_config.yaml`. For fair comparison, both types describe exactly same situation (They overwrite exactly same config items).

## Comparison

### Default config values
In this section, compare the differece of how to store the default config values.

#### Type 1
Default config values are stored as hierarchical multiple yaml files under `type1/config/`.
```
config
├──optimizer
│	└──sgd.yaml
└──scheduler
	├──cosine_annealing_lr.yaml
	└──reduce_lr_on_plateau.yaml
``` 
#### Type 2
Default config values are stored in single yaml file `type2/config/train.yaml`.
```
config
└──train.yaml
``` 

### Overwrite config values
In this section, compare the differece of how to overwrite the some config values from defaults.

#### Type 1
If you want to overwrite some config values, add additional sigle yaml file (`my_train_config.yaml`) under `config` directory.
```
config
├──my_train_config.yaml
├──optimizer
│	└──sgd.yaml
└──scheduler
	├──cosine_annealing_lr.yaml
	└──reduce_lr_on_plateau.yaml
``` 

In the `my_train_config.yaml`, write the values which you want to overwrite and top level config values (just name of optimizer and scheduler in the following example.).
```
defaults:
  - optimizer: sgd
  - scheduler: reduce_lr_on_plateau
  - _self_


optimizer:
  momentum: 0.8

scheduler:
  mode: max
  factor: 0.2
```

#### Type 2
If you want to overwrite some config values, add additional sigle yaml file (`my_train_config.yaml`) under `config/train_config` directory.
```
config
├──train_config
│	└──my_train_config.yaml
└──train.yaml
``` 

In the `my_train_config.yaml`, write the values which you want to overwrite.
```
optimizer:
    sgd:
        momentum: 0.8

scheduler:
    name: "reduce_lr_on_plateau"

    reduce_lr_on_plateau:
        mode: max
        factor: 0.2
```


### Config visualization
Configs loaded by hydra is used as [Omegaconf](https://omegaconf.readthedocs.io/en/2.1_branch/#) inside of the code. And Omegaconf has useful function `OmegaConf.to_yaml` to show thier values. 
In this repo, I just print the result of `OmegaConf.to_yaml` inside of `train.py`.

#### Type 1
Because type 1 only loads configs which is specified at top level, the result of `OmegaConf.to_yaml` becomes simple. (The config values related to `cosine_annealing_lr` are not loaded.)

```
$ cd type1
$ poetry run python src/train.py


optimizer:
  name: sgd
  lr: 0.1
  momentum: 0.8
  weight_decay: 0.0005
  dampening: 0.0
  nesterov: true
scheduler:
  name: reduce_lr_on_plateau
  mode: max
  factor: 0.2
  patience: 10
  threshold: 0.0001
  threshold_mode: rel
  cooldown: 0
  min_lr: 0
  eps: 1.0e-08
``` 
#### Type 2
Because type 2 loads all configs, the result of `OmegaConf.to_yaml` becomes longer. (The config values related to `cosine_annealing_lr` are loaded even it won't be used.)
```
$ cd type2
$ poetry run python src/train.py


train_config:
  optimizer:
    name: sgd
    sgd:
      lr: 0.1
      momentum: 0.9
      weight_decay: 0.0005
      dampening: 0.0
      nesterov: true
  scheduler:
    name: cosine_annealing_lr
    cosine_annealing_lr:
      T_max: 90
      eta_min: 0
      last_epoch: -1
    reduce_lr_on_plateau:
      mode: min
      factor: 0.1
      patience: 10
      threshold: 0.0001
      threshold_mode: rel
      cooldown: 0
      min_lr: 0
      eps: 1.0e-08
``` 

## Remarks
- If you apply type check to loaded config value by [hydra schema](https://hydra.cc/docs/tutorials/structured_config/schema), type 1 is needed.