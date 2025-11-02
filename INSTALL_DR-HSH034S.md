# Installing DR-HSH034S Support

This guide explains how to install the DR-HSH034S heater support for the Dreo Home Assistant integration.

## What Was Changed

Three files were modified/created to add support for the DR-HSH034S heater:

1. **`custom_components/dreo/device_configs.py`** (NEW) - Device configuration definitions
2. **`custom_components/dreo/__init__.py`** (MODIFIED) - Integration initialization with config application
3. **`DR-HSH034S_SUPPORT_ANALYSIS.md`** (NEW) - Technical analysis document

## Installation Steps

### Option 1: Manual Installation (Recommended for Testing)

1. **Backup your current installation**:
   ```bash
   cd /config/custom_components
   cp -r dreo dreo.backup
   ```

2. **Copy the new files**:
   - Copy `device_configs.py` to `/config/custom_components/dreo/`
   - Replace `__init__.py` with the updated version

3. **Restart Home Assistant**:
   - Go to Settings → System → Restart
   - Or use the command: `ha core restart`

4. **Verify the integration loads**:
   - Check Settings → Devices & Services → Dreo
   - Look for your DR-HSH034S heater device

### Option 2: Git Installation

If you're using git to manage your custom components:

```bash
cd /config/custom_components/dreo
git pull  # If this is a git repository
# Or manually copy the files
```

## What to Expect

After installation and restart, your DR-HSH034S heater should:

1. **Appear as a Climate entity** in Home Assistant
2. **Show current temperature** (in Fahrenheit)
3. **Allow temperature control** (41-85°F range)
4. **Support HVAC modes**:
   - Off
   - Heat
   - Fan Only
5. **Support Preset modes**:
   - Eco mode
   - Manual mode
6. **Provide additional controls** (as switches):
   - Oscillation
   - Child Lock
   - Mute
   - Display Light

## Verification Steps

### 1. Check the Logs

Look for these log messages in Home Assistant logs:

```
# Good signs:
[custom_components.dreo] Using initial state from device list for <device_id>
[custom_components.dreo] Initial state set for <device_id>

# Warning signs (should NOT appear):
[custom_components.dreo] Device type not available for model DR-HSH034S
[custom_components.dreo] Model config is not available for model DR-HSH034S
```

### 2. Check Device & Entities

1. Go to **Settings → Devices & Services → Dreo**
2. Click on your heater device
3. You should see:
   - **Climate entity**: `climate.heater` (or similar)
   - **Switch entities**: For oscillation, child lock, mute, display
   - **Sensor entities**: For temperature and other readings

### 3. Test Basic Functions

Try these operations:

- **Turn on/off**: Use the power button
- **Set temperature**: Adjust target temperature (41-85°F)
- **Change mode**: Switch between Eco and Manual presets
- **Toggle oscillation**: Turn oscillation on/off
- **Child lock**: Enable/disable child lock

## Troubleshooting

### Device Still Shows as "Unknown"

**Check**:
1. Verify `device_configs.py` is in the correct location
2. Check that `__init__.py` has the import: `from .device_configs import apply_device_config`
3. Look for errors in Home Assistant logs
4. Try reloading the integration (Settings → Devices & Services → Dreo → ⋮ → Reload)

### No Climate Entity Created

**Possible causes**:
1. Device type not being set correctly
2. Configuration not being applied
3. Check logs for warnings about the device

**Solution**:
```bash
# Enable debug logging
# Add to configuration.yaml:
logger:
  default: info
  logs:
    custom_components.dreo: debug

# Restart and check logs
```

### Temperature Not Updating

**Check**:
1. Device is powered on
2. Device is connected to WiFi
3. Dreo cloud API is accessible
4. Check the `ecolevel` and `temperature` fields in diagnostics

### Controls Not Working

**Verify**:
1. Device responds in the Dreo mobile app
2. Home Assistant can communicate with Dreo cloud
3. Check for API errors in logs

## Reverting Changes

If you need to revert to the original version:

```bash
cd /config/custom_components
rm -rf dreo
mv dreo.backup dreo
# Restart Home Assistant
```

## Advanced Configuration

### Adjusting Temperature Range

If the 41-85°F range doesn't match your device, edit `device_configs.py`:

```python
"temperature_range": [41, 85],  # Change these values
```

### Adding More Modes

If your device supports additional modes, add them to the configuration:

```python
"preset_modes": ["eco", "manual", "your_mode_here"],
```

## Getting Help

If you encounter issues:

1. **Check the logs** first (Settings → System → Logs)
2. **Enable debug logging** (see Troubleshooting section)
3. **Collect diagnostics**:
   - Settings → Devices & Services → Dreo
   - Click on your device
   - ⋮ → Download diagnostics
4. **Report issues** with:
   - Home Assistant version
   - Integration version
   - Device model (DR-HSH034S)
   - Diagnostic file
   - Relevant log entries

## Technical Details

### How It Works

1. When Home Assistant starts, it loads the Dreo integration
2. The integration fetches device list from Dreo cloud API
3. For each device, `apply_device_config()` checks if it needs fallback configuration
4. If the device is DR-HSH034S or WH714S series, it injects the configuration
5. The device is then set up as a heater with climate entity
6. State updates are processed through the coordinator

### Configuration Structure

The device configuration includes:
- **Device type**: "heater"
- **HVAC modes**: Supported heating modes
- **Preset modes**: Eco, Manual, etc.
- **Temperature range**: Min/max temperatures
- **Feature mapping**: How device states map to HA features
- **Toggle controls**: Switches for various functions

## Future Updates

This is a temporary workaround until official support is added to the pydreo-client library. When that happens:

1. The integration will be updated to use the new library version
2. This custom configuration may no longer be needed
3. You should update to the official version when available

## Files Modified

- `custom_components/dreo/__init__.py` - Added device config application
- `custom_components/dreo/device_configs.py` - New file with DR-HSH034S configuration

## Changelog

### Version 1.0 (Initial Release)
- Added DR-HSH034S heater support
- Created fallback configuration system
- Supports temperature control, modes, and toggles
- Compatible with existing Dreo integration structure
