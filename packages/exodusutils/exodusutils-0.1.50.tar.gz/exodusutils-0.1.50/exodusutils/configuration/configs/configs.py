import os

from pydantic.main import BaseModel
from minio import Minio

from exodusutils.configuration.configs.minio import MinioConfigs
from exodusutils.configuration.configs.mongodb import MongoDBConfigs
from exodusutils.configuration.configs.utils import get_configs
from exodusutils.configuration.mongo_instance import MongoInstance


class Configs(BaseModel):
    mongodb_configs: MongoDBConfigs
    minio_configs: MinioConfigs
    cores: int

    @classmethod
    def get(cls, name: str):
        mongodb_configs = MongoDBConfigs.get()
        minio_configs = MinioConfigs.get()
        configs = get_configs()
        if configs is None:
            cores_key = f"EXODUS_{name.upper()}_CORES"
            cpus = os.cpu_count()
            default_values = {cores_key: 1 if cpus is None else cpus}
            cores = int(os.environ.get(cores_key, default_values[cores_key]))
        else:
            configs = configs["exodus"]
            cores = int(configs["cores"])
        return cls(
            mongodb_configs=mongodb_configs, minio_configs=minio_configs, cores=cores
        )

    @property
    def mongo_instance(self) -> MongoInstance:
        return MongoInstance(self.mongodb_configs)

    @property
    def minio_instance(self) -> Minio:
        return self.minio_configs.get_client()
