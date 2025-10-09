"""
Modèle Person pour les personnes dans le format GeneWeb

Ce module définit la représentation des personnes avec toutes leurs informations
personnelles, événements et relations familiales.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .date import Date
from .event import PersonalEvent


class Gender(Enum):
    """Sexe d'une personne"""

    MALE = "m"
    FEMALE = "f"
    UNKNOWN = "?"


class AccessLevel(Enum):
    """Niveau d'accès aux informations d'une personne"""

    PUBLIC = "apubl"
    PRIVATE = "apriv"
    DEFAULT = ""  # Suit la règle "If Titles"


@dataclass
class Title:
    """Titre d'une personne (noblesse, profession, etc.)"""

    name: str
    title_type: str = ""
    place: str = ""
    start_date: Optional[Date] = None
    end_date: Optional[Date] = None
    number: int = 0
    is_main: bool = False  # Marqué avec * dans le format .gw

    def __str__(self) -> str:
        """Représentation string du titre"""
        parts = [self.name, self.title_type, self.place]

        if self.start_date:
            parts.append(self.start_date.display_text)
        else:
            parts.append("")

        if self.end_date:
            parts.append(self.end_date.display_text)
        else:
            parts.append("")

        if self.number > 0:
            parts.append(str(self.number))

        return ":".join(parts)


@dataclass
class Person:
    """Représentation d'une personne dans la généalogie

    Contient toutes les informations personnelles, dates importantes,
    événements et relations familiales.
    """

    # Informations de base
    last_name: str
    first_name: str
    occurrence_number: int = 0  # Pour distinguer les homonymes

    # Noms alternatifs
    public_name: Optional[str] = None  # (PublicName)
    nickname: Optional[str] = None  # #nick
    first_name_alias: Optional[str] = None  # {FirstNameAlias}
    surname_alias: Optional[str] = None  # #salias
    general_alias: Optional[str] = None  # #alias

    # Titres
    titles: List[Title] = field(default_factory=list)

    # Informations personnelles
    gender: Gender = Gender.UNKNOWN
    occupation: Optional[str] = None
    image_path: Optional[str] = None

    # Dates importantes
    birth_date: Optional[Date] = None
    death_date: Optional[Date] = None
    baptism_date: Optional[Date] = None

    # Lieux
    birth_place: Optional[str] = None
    death_place: Optional[str] = None
    baptism_place: Optional[str] = None
    burial_place: Optional[str] = None

    # Sources
    birth_source: Optional[str] = None
    death_source: Optional[str] = None
    baptism_source: Optional[str] = None
    burial_source: Optional[str] = None
    person_source: Optional[str] = None

    # Événements personnels (gwplus)
    events: List[PersonalEvent] = field(default_factory=list)

    # Informations de décès
    is_deceased: Optional[bool] = None  # ? pour inconnu
    is_obviously_dead: bool = False  # #od tag
    is_young_death: bool = False  # #mj tag
    burial_type: Optional[str] = None  # #buri ou #crem

    # Contrôle d'accès
    access_level: AccessLevel = AccessLevel.DEFAULT

    # Relations familiales (références)
    families_as_child: List[str] = field(
        default_factory=list
    )  # IDs des familles où cette personne est enfant
    families_as_spouse: List[str] = field(
        default_factory=list
    )  # IDs des familles où cette personne est époux(se)

    # Notes personnelles
    notes: List[str] = field(default_factory=list)

    # Relations spéciales (adoption, parrainage, etc.)
    relations: Dict[str, List[str]] = field(default_factory=dict)

    # Métadonnées personnalisées
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Validation gracieuse
    is_valid: bool = field(default=True)
    validation_errors: List[Any] = field(
        default_factory=list
    )  # List[GeneWebError] mais évite import circulaire

    def __post_init__(self) -> None:
        """Validation après initialisation"""
        # Normaliser les noms (remplacer espaces par underscores)
        self.last_name = self.last_name.replace(" ", "_")
        self.first_name = self.first_name.replace(" ", "_")

        if self.public_name:
            self.public_name = self.public_name.replace(" ", "_")

        # Validation gracieuse des dates
        if self.birth_date and self.death_date:
            if self.birth_date.year and self.death_date.year:
                if self.birth_date.year > self.death_date.year:
                    # Au lieu de lever une exception, ajouter une erreur de validation
                    from .exceptions import GeneWebValidationError

                    error = GeneWebValidationError(
                        f"Date de naissance ({self.birth_date}) postérieure à la date de décès ({self.death_date})",  # noqa: E501
                        field="birth_date",
                        entity_type="Person",
                        entity_id=self.unique_id,
                    )
                    self.add_validation_error(error)

    @property
    def full_name(self) -> str:
        """Retourne le nom complet de la personne"""
        name_parts = [self.last_name, self.first_name]
        if self.occurrence_number > 0:
            name_parts.append(f".{self.occurrence_number}")
        return " ".join(name_parts)

    @property
    def display_name(self) -> str:
        """Retourne le nom d'affichage (avec nom public si disponible)"""
        if self.public_name:
            return f"{self.last_name} {self.public_name}"
        return self.full_name

    @property
    def unique_id(self) -> str:
        """Retourne un identifiant unique pour cette personne"""
        return f"{self.last_name}_{self.first_name}_{self.occurrence_number}"

    @property
    def age_at_death(self) -> Optional[int]:
        """Calcule l'âge au décès si possible"""
        if not self.birth_date or not self.death_date:
            return None

        if not self.birth_date.year or not self.death_date.year:
            return None

        return self.death_date.year - self.birth_date.year

    @property
    def is_alive(self) -> bool:
        """Détermine si la personne est vivante"""
        # Si on a une date de décès, la personne est décédée
        if self.death_date:
            return False

        if self.is_deceased is True:
            return False
        if self.is_deceased is False:
            return True

        # Si inconnu, on peut essayer de déduire
        if self.is_obviously_dead:
            return False

        if self.birth_date and self.birth_date.year:
            # Personnes nées il y a plus de 150 ans sont probablement décédées
            from datetime import datetime

            current_year = datetime.now().year
            if current_year - self.birth_date.year > 150:
                return False

        return True  # Par défaut, on assume vivant si inconnu

    def add_title(self, title: Title) -> None:
        """Ajoute un titre à la personne"""
        self.titles.append(title)

    def add_event(self, event: PersonalEvent) -> None:
        """Ajoute un événement personnel"""
        self.events.append(event)

    def add_note(self, note: str) -> None:
        """Ajoute une note personnelle"""
        self.notes.append(note)

    def add_relation(self, relation_type: str, person_id: str) -> None:
        """Ajoute une relation spéciale (adoption, parrainage, etc.)"""
        if relation_type not in self.relations:
            self.relations[relation_type] = []
        self.relations[relation_type].append(person_id)

    def get_events_by_type(self, event_type: str) -> List[PersonalEvent]:
        """Retourne tous les événements d'un type donné"""
        return [event for event in self.events if event.event_type.value == event_type]

    def get_families(self) -> List[str]:
        """Retourne toutes les familles liées à cette personne"""
        return self.families_as_child + self.families_as_spouse

    def add_validation_error(self, error: Any) -> None:
        """Ajoute une erreur de validation à la personne

        Args:
            error: L'erreur à ajouter
        """
        self.validation_errors.append(error)
        self.is_valid = False

    def clear_validation_errors(self) -> None:
        """Efface toutes les erreurs de validation"""
        self.validation_errors.clear()
        self.is_valid = True

    def to_dict(self) -> Dict[str, Any]:
        """Convertit la personne en dictionnaire pour sérialisation"""
        return {
            "unique_id": self.unique_id,
            "full_name": self.full_name,
            "display_name": self.display_name,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "occurrence_number": self.occurrence_number,
            "public_name": self.public_name,
            "nickname": self.nickname,
            "gender": self.gender.value,
            "occupation": self.occupation,
            "birth_date": self.birth_date.display_text if self.birth_date else None,
            "death_date": self.death_date.display_text if self.death_date else None,
            "birth_place": self.birth_place,
            "death_place": self.death_place,
            "is_alive": self.is_alive,
            "age_at_death": self.age_at_death,
            "families_as_child": self.families_as_child,
            "families_as_spouse": self.families_as_spouse,
            "events": [event.to_dict() for event in self.events],
            "relations": self.relations,
            "notes": self.notes,
            "is_valid": self.is_valid,
            "validation_errors": [str(e) for e in self.validation_errors],
        }

    def __str__(self) -> str:
        """Représentation string de la personne"""
        return self.display_name

    def __repr__(self) -> str:
        """Représentation pour debug"""
        return f"Person('{self.full_name}')"
