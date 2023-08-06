""" AWS Available Instances """

from mcli.serverside.job.mcli_k8s_job_typing import MCLIK8sResourceRequirements
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.instance_type import InstanceType
from mcli.serverside.platforms.platform_instances import PlatformInstances
from mcli.utils.utils_kube_labels import label

a100_g8_instance = InstanceType(
    gpu_type=GPUType.A100_40GB,
    gpu_num=8,
    resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
        cpus=96,
        memory=1152,
        storage=80,
    ),
    selectors={
        label.kubernetes_node.INSTANCE_TYPE: label.legacy.AWS_A100_G8,
    },
)

v100_g8_instance = InstanceType(
    gpu_type=GPUType.V100_16GB,
    gpu_num=8,
    resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
        cpus=64,
        memory=488,
        storage=80,
    ),
    selectors={
        label.kubernetes_node.INSTANCE_TYPE: label.legacy.AWS_V100_G8,
    },
)

t4_g8_instance = InstanceType(
    gpu_type=GPUType.T4,
    gpu_num=8,
    resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
        cpus=96,
        memory=384,
        storage=80,
    ),
    selectors={
        label.kubernetes_node.INSTANCE_TYPE: label.legacy.AWS_T4_G8,
    },
)

AWS_ALLOWED_INSTANCES = PlatformInstances(instance_types=[a100_g8_instance, v100_g8_instance, t4_g8_instance])
