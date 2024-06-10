from config_types import DeploymentEnvEnum


kDeploymentEnvEnum: DeploymentEnvEnum = DeploymentEnvEnum.LOCAL
kIsHeadless: bool = True
kDelay: int = 3
kRevenueCrop: list= [1080,1115,620,800]

kParse: bool = False
kEnableHelium: bool = False
kEnablePrice: bool =  True

kRevenueWithParse: bool = True

kDataDir: str = "/Users/ardagulersoy/Downloads/siralanmis_ve_temizlenmis_parca3.xlsx.xlsx"
kRevenueColumn: str = "K"
kUsPriceColumn: str = "G"
kCaPriceColumn: str = "H"
kUsSaleColumn: str = "I"
kCaSaleColumn: str = "J"