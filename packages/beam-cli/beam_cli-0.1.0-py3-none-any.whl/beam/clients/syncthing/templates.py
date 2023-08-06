DEFAULT_FOLDER_NAME = "beam-1"
DEFAULT_REMOTE_DEVICE_NAME = "remote"
DEFAULT_LOCAL_DEVICE_NAME = "local"
DEFAULT_REMOTE_DEVICE_PORT = 22000


def generate_local_device_template(*, device_name: str, device_id: str) -> dict:
    return {
        "deviceID": device_id,
        "name": device_name,
        "addresses": ["dynamic"],
        "compression": "metadata",
        "certName": "",
        "introducer": True,
        "skipIntroductionRemovals": False,
        "introducedBy": "",
        "paused": False,
        "allowedNetworks": [],
        "autoAcceptFolders": True,
        "maxSendKbps": 0,
        "maxRecvKbps": 0,
        "ignoredFolders": [],
        "maxRequestKiB": 0,
        "untrusted": False,
        "remoteGUIPort": 0,
    }


def generate_remote_device_template(
    *,
    device_name: str,
    device_id: str,
    host: str = "0.0.0.0",
    port: int = DEFAULT_REMOTE_DEVICE_PORT,
) -> dict:
    return {
        "deviceID": device_id,
        "name": device_name,
        "addresses": [f"tcp://{host}"],
        "compression": "metadata",
        "certName": "",
        "introducer": False,
        "skipIntroductionRemovals": False,
        "introducedBy": "",
        "paused": False,
        "allowedNetworks": [],
        "autoAcceptFolders": False,
        "maxSendKbps": 0,
        "maxRecvKbps": 0,
        "ignoredFolders": [],
        "maxRequestKiB": 0,
        "untrusted": False,
        "remoteGUIPort": 0,
    }


def generate_folder_device_template(device_id: str) -> dict:
    return {
        "deviceID": device_id,
        "introducedBy": "",
        "encryptionPassword": "",
    }


def generate_folder_template(path: str):
    return [
        {
            "id": DEFAULT_FOLDER_NAME,
            "label": DEFAULT_FOLDER_NAME,
            "filesystemType": "basic",
            "path": path,
            "type": "sendreceive",
            "devices": [],
            "rescanIntervalS": 300,
            "fsWatcherEnabled": True,
            "fsWatcherDelayS": 1,
            "ignorePerms": False,
            "autoNormalize": True,
            "minDiskFree": {"value": 1, "unit": "%"},
            "versioning": {
                "type": "",
                "params": {},
                "cleanupIntervalS": 3600,
                "fsPath": "",
                "fsType": "basic",
            },
            "copiers": 0,
            "pullerMaxPendingKiB": 0,
            "hashers": 0,
            "order": "random",
            "ignoreDelete": False,
            "scanProgressIntervalS": 1,
            "pullerPauseS": 0,
            "maxConflicts": 0,
            "disableSparseFiles": False,
            "disableTempIndexes": False,
            "paused": False,
            "weakHashThresholdPct": 25,
            "markerName": ".",
            "copyOwnershipFromParent": False,
            "modTimeWindowS": 0,
            "maxConcurrentWrites": 2,
            "disableFsync": False,
            "blockPullOrder": "standard",
            "copyRangeMethod": "all",
            "caseSensitiveFS": False,
            "junctionsAsDirs": False,
        }
    ]
