from config_types import DeploymentEnvEnum


kDeploymentEnvEnum: DeploymentEnvEnum = DeploymentEnvEnum.LOCAL
kIsHeadless: bool = False
kDelay: int = 6
kRevenueCrop: list= [645,664,320,398]

kParse: bool = True
kEnableHelium: bool = True
kEnablePrice: bool =  True

kRevenueWithParse: bool = False

kDataDir: str = "persistance/siralanmis_ve_temizlenmis_parca3.xlsx.xlsx"
kRevenueColumn: str = "K"
kUsPriceColumn: str = "G"
kCaPriceColumn: str = "H"
kUsSaleColumn: str = "I"
kCaSaleColumn: str = "J"
