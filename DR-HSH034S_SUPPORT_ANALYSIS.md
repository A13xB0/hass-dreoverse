# DR-HSH034S Heater Support Analysis

## Current Status

The DR-HSH034S heater is **partially detected** but lacks full support. Based on the diagnostics data:

### Device Information
- **Model**: DR-HSH034S
- **Series**: WH714S
- **Product ID**: 1903999507765997570
- **Device Type**: Currently showing as "Unknown" in pydreo models
- **Product Name**: Heater

### Current State Data Available
The device is reporting the following state attributes:
- `poweron`: Power state
- `mode`: Operating mode (eco, etc.)
- `temperature`: Current temperature (64°F in diagnostics)
- `ecolevel`: Target temperature setting
- `htalevel`: Heat level (1-3)
- `oscmode`: Oscillation mode
- `oscillate`: Oscillation state
- `cruiseconf`: Cruise configuration
- `lighton`: Display light state
- `muteon`: Mute state
- `childlockon`: Child lock state
- `winopenon`: Window open detection
- `ptcon`: Protection mode

## Architecture

This Home Assistant integration (`hass-dreo`) is transitioning to use:
- **New Library**: `pydreo-client` (replacing `pydreo-cloud`)
- **Repository**: https://github.com/dreo-team/pydreo-client
- **Current Version in Integration**: `pydreo-cloud==1.0.0`

**Important Discovery**: The `pydreo-client` library is a simple API client that does NOT contain device configurations. Device configurations come from the Dreo cloud API in the device list response under the `config` field.

This means device support can be added directly in this integration by:
1. Detecting the device model (DR-HSH034S)
2. Injecting the appropriate configuration if it's missing from the API
3. Mapping it to the correct device type (HEATER)

## What Needs to Be Done

### Option 1: Update pydreo-cloud Library (Recommended)
The proper fix requires updating the `pydreo-cloud` library to include configuration for the DR-HSH034S model:

1. **Add device type mapping** for model "DR-HSH034S" or series "WH714S"
2. **Define heater configuration** including:
   - HVAC modes (heat, fan_only, off)
   - Temperature range (likely 41-85°F based on similar heaters)
   - Heat levels (1-3 based on `htalevel` in state)
   - Preset modes (eco, etc.)
   - Supported features (oscillation, child lock, etc.)

### Option 2: Temporary Workaround (If pydreo-cloud is unavailable)
If the pydreo-cloud library cannot be updated, a temporary workaround could be implemented in this integration:

1. Add model-specific detection in `__init__.py`
2. Inject configuration for DR-HSH034S when detected
3. Map the device to `DreoDeviceType.HEATER`

## Implementation Details

### Required Configuration Structure
Based on the existing heater support in `climate.py`, the DR-HSH034S needs:

```python
{
    "heater_entity_config": {
        "hvac_modes": ["off", "heat", "fan_only"],
        "preset_modes": ["eco", "manual"],  # Based on mode field
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
            }
        }
    }
}
```

### State Mapping
- `poweron` → Power on/off
- `mode` → Preset mode (eco, etc.)
- `temperature` → Current temperature
- `ecolevel` → Target temperature (when in eco mode)
- `htalevel` → Heat level (1-3, could map to fan speeds or heat intensity)
- `oscmode` / `oscillate` → Oscillation control

## Next Steps

1. **Contact the pydreo-cloud maintainer** to request DR-HSH034S support
2. **Provide device state data** from diagnostics to help with configuration
3. **Test the integration** once pydreo-cloud is updated
4. **Update this integration's manifest** if a newer pydreo-cloud version is released

## Files to Monitor

- `custom_components/dreo/manifest.json` - Library version
- `custom_components/dreo/climate.py` - Heater climate entity
- `custom_components/dreo/coordinator.py` - Device type handling
- `custom_components/dreo/const.py` - Device type constants

## Contact Information

- **Integration Repository**: https://github.com/jeffsteinbok/hass-dreo
- **Library Repository**: https://github.com/JeffSteinbok/pydreo-cloud (check if accessible)
- **Issue Tracker**: https://github.com/jeffsteinbok/hass-dreo/issues

## Conclusion

The DR-HSH034S heater is detected by the integration but requires configuration support in the `pydreo-cloud` library. The device appears to be a standard heater with temperature control, eco mode, oscillation, and safety features. Once the library is updated with the proper configuration, the integration should automatically support this device through the existing heater climate entity implementation.
