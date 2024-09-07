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
            
class AsinProviderEnum(Enum):
    EXCEL = 1
    REDIS = 2

    def to_string(self):
            if self == AsinProviderEnum.EXCEL:
                return "Excel"
            elif self == AsinProviderEnum.REDIS:
                return "Redis"
            else:
                raise ValueError(f"Unknown {self.__class__.__name__}: {self}")
            
