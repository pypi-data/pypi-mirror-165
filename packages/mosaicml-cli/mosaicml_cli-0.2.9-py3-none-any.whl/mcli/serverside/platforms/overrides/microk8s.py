""" Microk8s Platform Definition """
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.instance_type import InstanceType
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.platform_instances import LocalPlatformInstances, PlatformInstances

MICROK8S_INSTANCES = LocalPlatformInstances(instance_types=[InstanceType(
    gpu_type=GPUType.NONE,
    gpu_num=0,
)])


class Microk8sPlatform(GenericK8sPlatform):
    """ Microk8s Platform Overrides """

    allowed_instances: PlatformInstances = MICROK8S_INSTANCES
