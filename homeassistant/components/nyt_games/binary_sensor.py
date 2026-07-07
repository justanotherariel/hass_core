"""Support for NYT Games binary sensors."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import override

from nyt_games import Wordle

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import NYTGamesConfigEntry, NYTGamesCoordinator
from .entity import WordleEntity


@dataclass(frozen=True, kw_only=True)
class NYTGamesWordleBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a NYT Games Wordle binary sensor entity."""

    value_fn: Callable[[Wordle], bool]


BINARY_SENSORS: tuple[NYTGamesWordleBinarySensorEntityDescription, ...] = (
    NYTGamesWordleBinarySensorEntityDescription(
        key="played_today",
        translation_key="played_today",
        value_fn=lambda wordle: wordle.today_played,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: NYTGamesConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up NYT Games binary sensor entities based on a config entry."""
    coordinator = entry.runtime_data

    async_add_entities(
        NYTGamesWordleBinarySensor(coordinator, description)
        for description in BINARY_SENSORS
    )


class NYTGamesWordleBinarySensor(WordleEntity, BinarySensorEntity):
    """Defines a NYT Games Wordle binary sensor."""

    entity_description: NYTGamesWordleBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: NYTGamesCoordinator,
        description: NYTGamesWordleBinarySensorEntityDescription,
    ) -> None:
        """Initialize a NYT Games Wordle binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{coordinator.config_entry.unique_id}-wordle-{description.key}"
        )

    @property
    @override
    def is_on(self) -> bool:
        """Return the state of the binary sensor."""
        return self.entity_description.value_fn(self.coordinator.data.wordle)
