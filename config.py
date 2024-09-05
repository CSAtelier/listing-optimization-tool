from config_types import DeploymentEnvEnum


kDeploymentEnvEnum: DeploymentEnvEnum = DeploymentEnvEnum.LOCAL
kIsHeadless: bool = False
kDelay: int = 6
kRevenueCrop: list= [226,266,624,787]
kStop: int = -1
# [226,266,624,787][624,787,226,266]

kParse: bool = False
kEnableHelium: bool = False
kEnablePrice: bool =  False

kRevenueWithParse: bool = True

kDataDir: str = "/Users/ardagulersoy/Downloads/Serhat_list.xlsx"
kRevenueColumn: str = "J"
kUsPriceColumn: str = "K"
kCaPriceColumn: str = "L"
kUsSaleColumn: str = "M"
kCaSaleColumn: str = "N"
