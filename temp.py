from tk_base_utils import get_abs_path,load_toml


if __name__ == '__main__':
    toml_file = r'$src/tk_openai_sdk_agent/toml/test.toml'
    toml_config = load_toml(get_abs_path(toml_file))
    print(toml_config)