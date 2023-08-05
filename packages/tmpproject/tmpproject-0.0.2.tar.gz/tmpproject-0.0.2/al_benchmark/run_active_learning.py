import os
import hydra
from omegaconf import OmegaConf
from pathlib import Path
import json
import copy

from ..al4nlp.utils.general import log_config
from ..al4nlp.utils.main_decorator import main_decorator
from ..al4nlp.utils.embeddings import (
    load_embeddings_with_text,
    check_models,
)

import logging

log = logging.getLogger()


OmegaConf.register_new_resolver(
    "to_string", lambda x: x.replace("/", "_").replace("-", "_"), replace=True
)
OmegaConf.register_new_resolver(
    "get_patience_value", lambda dev_size: 1000 if dev_size == 0 else 5, replace=True
)


@main_decorator
def run_active_learning(config, work_dir):
    # Imports inside function to set environment variables before imports
    from .simulated_active_learning import (
        al_loop,
        initial_split,
    )
    from ..al4nlp.utils.data.load_data import load_data
    from ..al4nlp.utils.transformers_dataset import TransformersDataset

    # Log config so that it is visible from the console
    log_config(log, config)
    log.info("Loading data...")
    cache_dir = config.cache_dir if config.cache_model_and_dataset else None
    train_instances, dev_instances, test_instances, labels_or_id2label = load_data(
        config.data, config.acquisition_model.type, config.framework.name, cache_dir,
    )
    embeddings, word2idx = None, None
    embeddings_path, embeddings_cache_dir = check_models(config)
    if embeddings_path is not None:
        # load embeddings
        from datasets import concatenate_datasets

        try:
            all_data = concatenate_datasets(
                [train_instances, dev_instances, test_instances]
            )
        except:
            # in case of TransformersDataset
            all_data = copy.deepcopy(train_instances)
            all_data.add(dev_instances)
            all_data.add(test_instances)
        embeddings, word2idx = load_embeddings_with_text(
            all_data,
            embeddings_path,
            embeddings_cache_dir,
            text_name=config.data.text_name,
            n_vectors=config.data.get("n_vector", None),
        )
    # Make the initial split of the data onto labeled and unlabeled
    initial_data, unlabeled_data = initial_split(
        train_instances,
        config.al,
        config.acquisition_model.type,
        work_dir,
        tokens_column_name=config.data.text_name,
        labels_column_name=config.data.label_name,
        seed=config.seed,
    )
    log.info("Done.")

    # TODO: update all the code & configs for it
    # whether deep ensemble will be used
    use_de = "deep_ensemble" in config.al and config.al.deep_ensemble is not None
    id_first_iteration = 0

    try:
        if (
            config.get("from_checkpoint", None) is not None
            and config["from_checkpoint"]["path"] is not None
        ):

            from datasets import concatenate_datasets
            import numpy as np

            work_dir = Path(config["from_checkpoint"]["path"])
            last_iter = config["from_checkpoint"].get("last_iteration", None)

            text_column = config.data.text_name
            ids_paths = sorted(
                [x for x in os.listdir(work_dir) if x.startswith("ids_data_query_")]
            )
            if last_iter is not None:
                ids_paths = ids_paths[: last_iter + 1]
            id_first_iteration = len(ids_paths) - 1
            log.info(
                f"Resuming active learning from iteration {id_first_iteration + 1}..."
            )

            for i in range(len(ids_paths)):
                ids_data_query_path = f"ids_data_query_{i}.json"
                with open(work_dir / ids_data_query_path) as f:
                    query_ids = json.load(f)
                if ids_data_query_path == "ids_data_query_0.json":
                    query = train_instances.select(query_ids)
                    assert (
                        query[text_column] == initial_data[text_column]
                    ), "Initial iteration results differ!"
                else:
                    query = unlabeled_data.select(query_ids)
                    if isinstance(initial_data, TransformersDataset):
                        initial_data.add(query)
                    else:
                        initial_data = concatenate_datasets([initial_data, query])
                    unlabeled_data = unlabeled_data.select(
                        np.setdiff1d(range(len(unlabeled_data)), query_ids)
                    )
            log.info(
                f"Query ids up to iteration {id_first_iteration} inclusive successfully loaded."
            )

        else:
            log.info("Starting active learning...")

        models = al_loop(
            config,
            work_dir,
            initial_data=initial_data,
            dev_data=dev_instances,
            test_data=test_instances,
            unlabeled_data=unlabeled_data,
            labels_or_id2label=labels_or_id2label,
            id_first_iteration=id_first_iteration,
            embeddings=embeddings,
            word2idx=word2idx,
        )
        log.info("Done with active learning...")
        return models
    except Exception as e:
        log.error(e, exc_info=True)


@hydra.main(
    config_path=os.environ.get("HYDRA_CONFIG_PATH", "al_benchmark/configs"),
    config_name=os.environ.get("HYDRA_CONFIG_NAME", "al_cls"),
)
def main(config):
    run_active_learning(config)


if __name__ == "__main__":
    main()
