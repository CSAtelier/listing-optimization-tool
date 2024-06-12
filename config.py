from config_types import DeploymentEnvEnum


kDeploymentEnvEnum: DeploymentEnvEnum = DeploymentEnvEnum.LOCAL
kIsHeadless: bool = True
kDelay: int = 8
kRevenueCrop: list= [583,599,234,309]

kParse: bool = False
kEnableHelium: bool = False
kEnablePrice: bool =  True

kRevenueWithParse: bool = True

kDataDir: str = "persistance/siralanmis_ve_temizlenmis_parca3.xlsx.xlsx"
kRevenueColumn: str = "K"
kUsPriceColumn: str = "G"
kCaPriceColumn: str = "H"
kUsSaleColumn: str = "I"
kCaSaleColumn: str = "J"
