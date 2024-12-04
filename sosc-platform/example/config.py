c = get_config()

c.ServerProxy.servers = {
    "mlflow": {
        "command": ["mlflow", "server"],
        "timeout": 30,
        "port": 5000,
        # "launcher_entry": {
        #        "icon_path": "https://mlflow.org/img/mlflow-black.svg",
        # }
    },
    "object-storage": {
        # "command": ["minio", "server", "/home/jovyan/minio", "--console-address", ":9001"],
        "port": 9001
        # "launcher_entry": {
        #        "icon_path": "https://min.io/resources/img/logo.svg",
        # }
    },
}
