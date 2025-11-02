"""Device-specific configurations for Dreo devices.

This module provides fallback configurations for devices that may not
have complete configuration data from the Dreo cloud API.
"""

from homeassistant.components.climate import ClimateEntityFeature

# Device model configurations
DEVICE_CONFIGS = {
    "DR-HSH034S": {
        "deviceType": "heater",
        "config": {
            "heater_entity_config": {
                "hvac_modes": ["off", "heat", "fan_only"],
                "preset_modes": ["eco", "manual"],
                "temperature_range": [41, 85],  # Fahrenheit
                "temperature_unit": "fahrenheit",
                "hvac_mode_relate_map": {
                    "eco": {
                        "report": {
                            "directive_value": "eco",
                            "hvac_mode_value": "heat"
                        },
                        "controls": [
                            {"directive_name": "mode", "directive_value": "eco"}
                        ],
                        "supported_features": [
                            ClimateEntityFeature.TARGET_TEMPERATURE,
                            ClimateEntityFeature.PRESET_MODE
                        ]
                    },
                    "manual": {
                        "report": {
                            "directive_value": "manual",
                            "hvac_mode_value": "heat"
                        },
                        "controls": [
                            {"directive_name": "mode", "directive_value": "manual"}
                        ],
                        "supported_features": [
                            ClimateEntityFeature.TARGET_TEMPERATURE,
                            ClimateEntityFeature.PRESET_MODE
                        ]
                    }
                }
            },
            "entitySupports": ["climate", "sensor"],
            "sensor_entity_config": {
                "temperature": {
                    "attr_name": "temperature",
                    "directive_name": "temperature",
                    "state_attr_name": "temperature",
                    "sensor_class": "temperature",
                    "attr_icon": "mdi:thermometer",
                    "native_unit_of_measurement": "°F"
                }
            },
            "toggle_entity_config": {
                "oscillate": {
                    "field": "oscillate",
                    "operable_when_off": False
                },
                "childlockon": {
                    "field": "childlockon",
                    "operable_when_off": True
                },
                "muteon": {
                    "field": "muteon",
                    "operable_when_off": True
                },
                "lighton": {
                    "field": "lighton",
                    "operable_when_off": True
                }
            }
        }
    },
    # WH714S is the series name for DR-HSH034S
    "WH714S": {
        "deviceType": "heater",
        "config": {
            "heater_entity_config": {
                "hvac_modes": ["off", "heat", "fan_only"],
                "preset_modes": ["eco", "manual"],
                "temperature_range": [41, 85],
                "temperature_unit": "fahrenheit",
                "hvac_mode_relate_map": {
                    "eco": {
                        "report": {
                            "directive_value": "eco",
                            "hvac_mode_value": "heat"
                        },
                        "controls": [
                            {"directive_name": "mode", "directive_value": "eco"}
                        ],
                        "supported_features": [
                            ClimateEntityFeature.TARGET_TEMPERATURE,
                            ClimateEntityFeature.PRESET_MODE
                        ]
                    },
                    "manual": {
                        "report": {
                            "directive_value": "manual",
                            "hvac_mode_value": "heat"
                        },
                        "controls": [
                            {"directive_name": "mode", "directive_value": "manual"}
                        ],
                        "supported_features": [
                            ClimateEntityFeature.TARGET_TEMPERATURE,
                            ClimateEntityFeature.PRESET_MODE
                        ]
                    }
                }
            },
            "entitySupports": ["climate", "sensor"],
            "sensor_entity_config": {
                "temperature": {
                    "attr_name": "temperature",
                    "directive_name": "temperature",
                    "state_attr_name": "temperature",
                    "sensor_class": "temperature",
                    "attr_icon": "mdi:thermometer",
                    "native_unit_of_measurement": "°F"
                }
            },
            "toggle_entity_config": {
                "oscillate": {
                    "field": "oscillate",
                    "operable_when_off": False
                },
                "childlockon": {
                    "field": "childlockon",
                    "operable_when_off": True
                },
                "muteon": {
                    "field": "muteon",
                    "operable_when_off": True
                },
                "lighton": {
                    "field": "lighton",
                    "operable_when_off": True
                }
            }
        }
    }
}


def get_device_config(model: str, series: str | None = None) -> dict | None:
    """Get device configuration by model or series name.
    
    Args:
        model: Device model number (e.g., "DR-HSH034S")
        series: Device series name (e.g., "WH714S")
        
    Returns:
        Device configuration dict or None if not found
    """
    # Try model first
    if model in DEVICE_CONFIGS:
        return DEVICE_CONFIGS[model]
    
    # Try series as fallback
    if series and series in DEVICE_CONFIGS:
        return DEVICE_CONFIGS[series]
    
    return None


def apply_device_config(device: dict) -> dict:
    """Apply fallback configuration to a device if needed.
    
    Args:
        device: Device dict from Dreo API
        
    Returns:
        Device dict with configuration applied
    """
    model = device.get("model")
    series = device.get("seriesName")
    
    # Try to get fallback configuration
    config_data = get_device_config(model, series)
    if not config_data:
        return device
    
    # Apply device type if missing
    if not device.get("deviceType"):
        device["deviceType"] = config_data["deviceType"]
    
    # Merge or set configuration
    if not device.get("config"):
        device["config"] = config_data["config"]
    elif isinstance(device.get("config"), dict):
        # Deep merge configurations - our fallback config takes precedence for missing keys
        for key, value in config_data["config"].items():
            if key not in device["config"]:
                device["config"][key] = value
            elif key == "sensor_entity_config" and isinstance(value, dict):
                # For sensor_entity_config, merge the temperature sensor config
                if "sensor_entity_config" not in device["config"]:
                    device["config"]["sensor_entity_config"] = {}
                for sensor_key, sensor_conf in value.items():
                    if sensor_key not in device["config"]["sensor_entity_config"]:
                        device["config"]["sensor_entity_config"][sensor_key] = sensor_conf
                    elif isinstance(sensor_conf, dict):
                        # Merge sensor configuration, adding missing keys
                        for conf_key, conf_value in sensor_conf.items():
                            if conf_key not in device["config"]["sensor_entity_config"][sensor_key]:
                                device["config"]["sensor_entity_config"][sensor_key][conf_key] = conf_value
    
    return device
