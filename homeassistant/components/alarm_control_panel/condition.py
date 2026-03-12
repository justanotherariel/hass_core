"""Provides conditions for alarm control panels."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.condition import (
    Condition,
    EntityStateConditionBase,
    make_entity_state_condition,
)
from homeassistant.helpers.trigger import EntityMatchSpec

from .const import DOMAIN, AlarmControlPanelEntityFeature, AlarmControlPanelState


def make_entity_state_required_features_condition(
    domain: str, to_state: str, required_features: int
) -> type[EntityStateConditionBase]:
    """Create an entity state condition class with required feature filtering."""

    class CustomCondition(EntityStateConditionBase):
        """Condition for entity state changes."""

        _match_specs = [
            EntityMatchSpec(domain=domain, required_features=required_features)
        ]
        _states = {to_state}

    return CustomCondition


CONDITIONS: dict[str, type[Condition]] = {
    "is_armed": make_entity_state_condition(
        DOMAIN,
        {
            AlarmControlPanelState.ARMED_AWAY,
            AlarmControlPanelState.ARMED_CUSTOM_BYPASS,
            AlarmControlPanelState.ARMED_HOME,
            AlarmControlPanelState.ARMED_NIGHT,
            AlarmControlPanelState.ARMED_VACATION,
        },
    ),
    "is_armed_away": make_entity_state_required_features_condition(
        DOMAIN,
        AlarmControlPanelState.ARMED_AWAY,
        AlarmControlPanelEntityFeature.ARM_AWAY,
    ),
    "is_armed_home": make_entity_state_required_features_condition(
        DOMAIN,
        AlarmControlPanelState.ARMED_HOME,
        AlarmControlPanelEntityFeature.ARM_HOME,
    ),
    "is_armed_night": make_entity_state_required_features_condition(
        DOMAIN,
        AlarmControlPanelState.ARMED_NIGHT,
        AlarmControlPanelEntityFeature.ARM_NIGHT,
    ),
    "is_armed_vacation": make_entity_state_required_features_condition(
        DOMAIN,
        AlarmControlPanelState.ARMED_VACATION,
        AlarmControlPanelEntityFeature.ARM_VACATION,
    ),
    "is_disarmed": make_entity_state_condition(DOMAIN, AlarmControlPanelState.DISARMED),
    "is_triggered": make_entity_state_condition(
        DOMAIN, AlarmControlPanelState.TRIGGERED
    ),
}


async def async_get_conditions(hass: HomeAssistant) -> dict[str, type[Condition]]:
    """Return the alarm control panel conditions."""
    return CONDITIONS
