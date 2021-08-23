import hydra
from omegaconf import OmegaConf

@hydra.main(config_path="./config", config_name="train")
def train(cfg) -> None:
    """train classifer.
    Args:
        cfg: Configs whose type is checked by schema.
    """
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    train()