from config_types import DeploymentEnvEnum


kDeploymentEnvEnum: DeploymentEnvEnum = DeploymentEnvEnum.LOCAL
kIsHeadless: bool = True
kDelay: int = 7
kRevenueCrop: list= [645,664,320,398]
kStop: int = 4

kParse: bool = True
kEnableHelium: bool = True
kEnablePrice: bool =  True

kRevenueWithParse: bool = False

kDataDir: str = "persistance/siralanmis_ve_temizlenmis_parca1.xlsx.xlsx"
kRevenueColumn: str = "K"
kUsPriceColumn: str = "G"
kCaPriceColumn: str = "H"
kUsSaleColumn: str = "I"
kCaSaleColumn: str = "J"
