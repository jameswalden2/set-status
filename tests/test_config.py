from set_status.config import ConfigClient, ConfigProvider


def test_config_client_read_config(tmp_dir):
    client = ConfigClient(config_dir=tmp_dir)

    client.update_config(provider=ConfigProvider.gh, config={"token": "abc"})
    config = client.read_config(provider=ConfigProvider.gh)

    assert config.get("token")
    assert config["token"] == "abc"
