import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL

from solakon_one.config_flow import ConfigFlow
from solakon_one.const import CONF_DEVICE_ID


def test_reconfigure_updates_connection_without_replacing_entry_data() -> None:
    async def run_test() -> None:
        flow = ConfigFlow()
        flow.hass = MagicMock()
        entry = MagicMock()
        entry.data = {
            CONF_HOST: "192.0.2.10",
            CONF_PORT: 502,
            CONF_DEVICE_ID: 7,
            CONF_SCAN_INTERVAL: 30,
        }
        user_input = {CONF_HOST: "198.51.100.20", CONF_PORT: 1502}

        with (
            patch(
                "solakon_one.config_flow.validate_input",
                new=AsyncMock(),
            ) as validate_input,
            patch.object(
                flow,
                "_get_reconfigure_entry",
                return_value=entry,
            ),
            patch.object(
                flow,
                "async_update_reload_and_abort",
                return_value={
                    "type": "abort",
                    "reason": "reconfigure_successful",
                },
            ) as update_entry,
        ):
            result = await flow.async_step_reconfigure(user_input)

        validate_input.assert_awaited_once_with(flow.hass, entry.data | user_input)
        update_entry.assert_called_once_with(
            entry,
            data_updates=user_input,
        )
        assert result == {
            "type": "abort",
            "reason": "reconfigure_successful",
        }

    asyncio.run(run_test())
