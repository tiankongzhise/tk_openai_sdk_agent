from tk_base_utils import load_toml
# from dotenv import load_dotenv
import os

def test_load_toml():
    print(f'ARK_API_KEY bf: {os.getenv("ARK_API_KEY")}')
    # load_dotenv()
    print(f'ARK_API_KEY: {os.getenv("ARK_API_KEY")}')
    toml_config = load_toml()
    print(toml_config)
