from iniUts import IniUts

# Initialize with encryption key
ini = IniUts('App/config/init/prod.ini', encryption_key="encryption_code")

@ini.link('CAMINHOS')
class Local():
    caminho : str