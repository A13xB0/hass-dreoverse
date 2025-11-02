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
                "temperature_range": [5, 35],  # Celsius
                "temperature_unit": "celsius",
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
            "entitySupports": ["climate"],
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
                "temperature_range": [5, 35],  # Celsius
                "temperature_unit": "celsius",
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
            "entitySupports": ["climate"],
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
    
    # Check if device already has configuration
    if device.get("config") and device.get("deviceType"):
        return device
    
    # Try to get fallback configuration
    config_data = get_device_config(model, series)
    if config_data:
        # Apply configuration
        if not device.get("deviceType"):
            device["deviceType"] = config_data["deviceType"]
        
        if not device.get("config"):
            device["config"] = config_data["config"]
        elif isinstance(device.get("config"), dict):
            # Merge configurations
            for key, value in config_data["config"].items():
                if key not in device["config"]:
                    device["config"][key] = value
    
    return device
