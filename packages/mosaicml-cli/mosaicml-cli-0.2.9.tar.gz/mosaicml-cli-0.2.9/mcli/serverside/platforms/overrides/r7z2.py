""" R7Z2 Platform Definition """
from typing import Dict, List, Optional

from mcli import config
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.instance_type import InstanceType
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.platform_instances import (LocalPlatformInstances, PlatformInstanceGPUConfiguration,
                                                          PlatformInstances)
from mcli.utils.utils_kube_labels import label

R7Z2_PRIORITY_CLASS_LABELS: Dict[str, str] = {
    'scavenge': 'mosaicml-internal-research-scavenge-priority',
    'standard': 'mosaicml-internal-research-standard-priority',
    'emergency': 'mosaicml-internal-research-emergency-priority'
}

a100_config = PlatformInstanceGPUConfiguration(
    gpu_type=GPUType.A100_40GB,
    gpu_nums=[1, 2, 4, 8, 16, 32, 64, 128],
    gpu_selectors={label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.OCI_GB4_8},
    cpus=128,
    cpus_per_gpu=16,
    memory=2048,
    memory_per_gpu=256,
    storage=8000,
    storage_per_gpu=1000,
    multinode_rdma_roce=1,
)

cpu_config = PlatformInstanceGPUConfiguration(
    gpu_type=GPUType.NONE,
    gpu_nums=[0],
)

R7Z2_INSTANCES = LocalPlatformInstances(gpu_configurations=[a100_config, cpu_config])


class R7Z2Platform(GenericK8sPlatform):
    """ R7Z2 Platform Overrides """

    allowed_instances: PlatformInstances = R7Z2_INSTANCES
    priority_class_labels = R7Z2_PRIORITY_CLASS_LABELS  # type: Dict[str, str]
    default_priority_class: str = 'standard'
    pod_group_scheduler: Optional[str] = 'scheduler-plugins-scheduler'

    def get_tolerations(self, instance_type: InstanceType) -> List[Dict[str, str]]:
        del instance_type
        tolerations = []
        mcli_config = config.MCLIConfig.load_config()
        if mcli_config.feature_enabled(feature=config.FeatureFlag.USE_DEMO_NODES):
            tolerations.append({
                'effect': 'NoSchedule',
                'key': label.mosaic.demo.DEMO_NODE,
                'operator': 'Equal',
                'value': 'true'
            })

        return tolerations

    def get_selectors(self, instance_type: InstanceType) -> Dict[str, str]:
        selectors = super().get_selectors(instance_type)
        mcli_config = config.MCLIConfig.load_config()
        if mcli_config.feature_enabled(feature=config.FeatureFlag.USE_DEMO_NODES):
            selectors[label.mosaic.demo.DEMO_NODE] = 'true'
        return selectors
