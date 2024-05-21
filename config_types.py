from enum import Enum

class DeploymentEnvEnum(Enum):
    LOCAL = 1
    CLOUD = 2

    def to_string(self):
            if self == DeploymentEnvEnum.LOCAL:
                return "Local"
            elif self == DeploymentEnvEnum.CLOUD:
                return "Cloud"
            else:
                raise ValueError(f"Unknown DeploymentEnvironment: {self}")