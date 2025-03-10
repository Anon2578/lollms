from pathlib import Path
import shutil
from lollms.helpers import ASCIIColors
from lollms.config import BaseConfig
import subprocess

lollms_path = Path(__file__).parent
lollms_default_cfg_path = lollms_path / "configs/config.yaml"
lollms_bindings_zoo_path = lollms_path / "bindings_zoo"
lollms_personalities_zoo_path = lollms_path / "personalities_zoo"


personalities_zoo_repo = "https://github.com/ParisNeo/lollms_personalities_zoo.git"
bindings_zoo_repo = "https://github.com/ParisNeo/lollms_bindings_zoo.git"

# Now we speify the personal folders
class LollmsPaths:
    def __init__(self, global_paths_cfg_path=None, lollms_path=None, personal_path=None, custom_default_cfg_path=None, tool_prefix=""):
        self.global_paths_cfg_path  = global_paths_cfg_path
        self.tool_prefix            = tool_prefix
        if lollms_path is None:
            lollms_path             = Path(__file__).parent
        else:
            lollms_path             = Path(lollms_path)
        if personal_path is None:
            personal_path           = Path.home() / "Documents/lollms"
        else:
            personal_path           = Path(personal_path)
        
        if custom_default_cfg_path is not None:
            self.default_cfg_path   = Path(custom_default_cfg_path)
        else:
            self.default_cfg_path   = lollms_path / "configs/config.yaml"

        self.personal_path                  = personal_path
        self.personal_configuration_path    = personal_path / "configs"
        self.personal_data_path             = personal_path / "data"
        self.personal_databases_path        = personal_path / "databases"
        self.personal_models_path           = personal_path / "models"
        self.personal_uploads_path          = lollms_path / "uploads"
        self.personal_log_path              = lollms_path / "logs"


        self.bindings_zoo_path              = personal_path / "bindings_zoo"
        self.personalities_zoo_path         = personal_path / "personalities_zoo"


        self.create_directories()
        self.copy_default_config()

    def __str__(self) -> str:
        directories = {
            "Global paths configuration Path": self.global_paths_cfg_path,
            "Personal Configuration Path": self.personal_configuration_path,
            "Personal Data Path": self.personal_data_path,
            "Personal Databases Path": self.personal_databases_path,
            "Personal Models Path": self.personal_models_path,
            "Personal Uploads Path": self.personal_uploads_path,
            "Personal Log Path": self.personal_log_path,
            "Bindings Zoo Path": self.bindings_zoo_path,
            "Personalities Zoo Path": self.personalities_zoo_path
        }
        return "\n".join([f"{category}: {path}" for category, path in directories.items()])

    def change_personal_path(self, path):
        self.personal_path = path

    def create_directories(self):
        self.personal_path.mkdir(parents=True, exist_ok=True)
        self.personal_configuration_path.mkdir(parents=True, exist_ok=True)
        self.personal_models_path.mkdir(parents=True, exist_ok=True)
        self.personal_data_path.mkdir(parents=True, exist_ok=True)
        self.personal_databases_path.mkdir(parents=True, exist_ok=True)
        self.personal_log_path.mkdir(parents=True, exist_ok=True)
        self.personal_uploads_path.mkdir(parents=True, exist_ok=True)

        if not self.personalities_zoo_path.exists():
            # Clone the repository to the target path
            ASCIIColors.info("No personalities found in your personal space.\nCloning the personalities zoo")
            subprocess.run(["git", "clone", personalities_zoo_repo, self.personalities_zoo_path])
        else:
            # Pull the repository if it already exists
            ASCIIColors.info("Personalities zoo found in your personal space.\nPulling last personalities zoo")
            subprocess.run(["git", "-C", self.personalities_zoo_path, "pull"])            

        if not self.bindings_zoo_path.exists():
            # Clone the repository to the target path
            ASCIIColors.info("No personalities found in your personal space.\nCloning the personalities zoo")
            subprocess.run(["git", "clone", bindings_zoo_repo, self.bindings_zoo_path])
        else:
            # Pull the repository if it already exists
            ASCIIColors.info("Personalities zoo found in your personal space.\nPulling last personalities zoo")
            subprocess.run(["git", "-C", self.bindings_zoo_path, "pull"])            


    def copy_default_config(self):
        local_config_path = self.personal_configuration_path / f"{self.tool_prefix}local_config.yaml"
        if not local_config_path.exists():
            shutil.copy(self.default_cfg_path, str(local_config_path))

    def resetPaths(self, force_local=None):
        global_paths_cfg_path = Path(f"./{self.tool_prefix}global_paths_cfg.yaml")
        
        if force_local is None:
            if global_paths_cfg_path.exists():
                force_local = True
            else:
                force_local = False
        print(f"To make it clear where your data are stored, we now give the user the choice where to put its data.")
        print(f"This allows you to mutualize models which are heavy, between multiple lollms compatible apps.")
        print(f"You can change this at any tome using the lollms-settings script or by simply change the content of the global_paths_cfg.yaml file.")
        found = False
        while not found:
            print(f"Please provide a folder to store your configurations files, your models and your personal data (database, custom personalities etc).")
            cfg = BaseConfig(config={
                "lollms_path":str(Path(__file__).parent),
                "lollms_personal_path":str(Path.home()/"Documents/lollms")
            })

            cfg.lollms_personal_path = input(f"Folder path: ({cfg.lollms_personal_path}):")
            if cfg.lollms_personal_path=="":
                cfg.lollms_personal_path = str(Path.home()/"Documents/lollms")

            print(f"Selected: {cfg.lollms_personal_path}")
            pp= Path(cfg.lollms_personal_path)
            if not pp.exists():
                try:
                    pp.mkdir(parents=True)
                except:
                    print(f"{ASCIIColors.color_red}It seams there is an error in the path you rovided{ASCIIColors.color_reset}")
                    continue
            if force_local:
                global_paths_cfg_path = Path(f"./{self.tool_prefix}global_paths_cfg.yaml")
            else:
                global_paths_cfg_path = Path.home()/f"{self.tool_prefix}global_paths_cfg.yaml"
            cfg.save_config(global_paths_cfg_path)
            found = True
        
        return LollmsPaths(global_paths_cfg_path, cfg.lollms_path, cfg.lollms_personal_path, custom_default_cfg_path=custom_default_cfg_path)        

    @staticmethod
    def find_paths(force_local=False, custom_default_cfg_path=None, tool_prefix=""):
        lollms_path = Path(__file__).parent
        global_paths_cfg_path = Path(f"./{tool_prefix}global_paths_cfg.yaml")
        if global_paths_cfg_path.exists():
            try:
                cfg = BaseConfig()
                cfg.load_config(global_paths_cfg_path)
                lollms_path = cfg.lollms_path
                lollms_personal_path = cfg.lollms_personal_path
                return LollmsPaths(global_paths_cfg_path, lollms_path, lollms_personal_path, custom_default_cfg_path=custom_default_cfg_path, tool_prefix=tool_prefix)
            except Exception as ex:
                print(f"{ASCIIColors.color_red}Global paths configuration file found but seems to be corrupted{ASCIIColors.color_reset}")
                print("Couldn't find your personal data path!")
                cfg.lollms_path = str(Path(__file__).parent)
                cfg["lollms_personal_path"] = str(Path.home()/"Documents/lollms")
                print("Please specify the folder where your configuration files, your models and your custom personalities need to be stored:")
                lollms_personal_path = input(f"Folder path: ({cfg.lollms_personal_path}):")
                if lollms_personal_path!="":
                    cfg.lollms_personal_path=lollms_personal_path
                cfg.save_config(global_paths_cfg_path)
                lollms_path = cfg.lollms_path
                lollms_personal_path = cfg.lollms_personal_path
                return LollmsPaths(global_paths_cfg_path, lollms_path, lollms_personal_path, custom_default_cfg_path=custom_default_cfg_path, tool_prefix=tool_prefix)
        else:
            # if the app is not forcing a specific path, then try to find out if the default installed library has specified a default path
            global_paths_cfg_path = Path.home()/f"{tool_prefix}global_paths_cfg.yaml"
            if global_paths_cfg_path.exists():
                cfg = BaseConfig()
                cfg.load_config(global_paths_cfg_path)
                try:
                    lollms_path = cfg.lollms_path
                    lollms_personal_path = cfg.lollms_personal_path
                    return LollmsPaths(global_paths_cfg_path, lollms_path, lollms_personal_path, custom_default_cfg_path=custom_default_cfg_path, tool_prefix=tool_prefix)
                except Exception as ex:
                    print(f"{ASCIIColors.color_red}Global paths configuration file found but seems to be corrupted{ASCIIColors.color_reset}")
                    cfg.lollms_path = Path(__file__).parent
                    cfg.lollms_personal_path = input("Please specify the folder where your configuration files, your models and your custom personalities need to be stored:")
                    cfg.save_config(global_paths_cfg_path)
                    lollms_path = cfg.lollms_path
                    lollms_personal_path = cfg.lollms_personal_path
                    return LollmsPaths(global_paths_cfg_path, lollms_path, lollms_personal_path, custom_default_cfg_path=custom_default_cfg_path, tool_prefix=tool_prefix)
            else: # First time 
                print(f"{ASCIIColors.color_green}Welcome! It seems this is your first use of the new lollms app.{ASCIIColors.color_reset}")
                print(f"To make it clear where your data are stored, we now give the user the choice where to put its data.")
                print(f"This allows you to mutualize models which are heavy, between multiple lollms compatible apps.")
                print(f"You can change this at any tome using the lollms-settings script or by simply change the content of the global_paths_cfg.yaml file.")
                found = False
                while not found:
                    print(f"Please provide a folder to store your configurations files, your models and your personal data (database, custom personalities etc).")
                    cfg = BaseConfig(config={
                        "lollms_path":str(Path(__file__).parent),
                        "lollms_personal_path":str(Path.home()/"Documents/lollms")
                    })

                    cfg.lollms_personal_path = input(f"Folder path: ({cfg.lollms_personal_path}):")
                    if cfg.lollms_personal_path=="":
                        cfg.lollms_personal_path = str(Path.home()/"Documents/lollms")

                    print(f"Selected: {cfg.lollms_personal_path}")
                    pp= Path(cfg.lollms_personal_path)
                    if not pp.exists():
                        try:
                            pp.mkdir(parents=True)
                        except:
                            print(f"{ASCIIColors.color_red}It seams there is an error in the path you rovided{ASCIIColors.color_reset}")
                            continue
                    if force_local:
                        global_paths_cfg_path = Path(f"./{tool_prefix}global_paths_cfg.yaml")
                    else:
                        global_paths_cfg_path = Path.home()/f"{tool_prefix}global_paths_cfg.yaml"
                    cfg.save_config(global_paths_cfg_path)
                    found = True
                
                return LollmsPaths(global_paths_cfg_path, cfg.lollms_path, cfg.lollms_personal_path, custom_default_cfg_path=custom_default_cfg_path, tool_prefix=tool_prefix)
            
            
    @staticmethod     
    def reset_configs(tool_prefix=""):
        lollms_path = Path(__file__).parent
        global_paths_cfg_path = Path(f"./{tool_prefix}global_paths_cfg.yaml")
        if global_paths_cfg_path.exists():
            ASCIIColors.error("Resetting local settings")
            global_paths_cfg_path.unlink()
            return
        global_paths_cfg_path = Path.home()/f"{tool_prefix}global_paths_cfg.yaml"
        if global_paths_cfg_path.exists():
            ASCIIColors.error("Resetting global settings")
            global_paths_cfg_path.unlink()


