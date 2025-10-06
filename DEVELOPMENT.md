# Développement de geneweb-py

## État actuel du projet

### ✅ Fonctionnalités implémentées

#### 1. Structure du projet
- Configuration complète avec `pyproject.toml`
- Structure modulaire (`core/`, `api/`, `formats/`, `utils/`, `tests/`, `examples/`)
- Configuration pytest avec couverture de code (73%)
- Installation en mode développement

#### 2. Modèles de données
- **Date** : Parser complet avec support des préfixes (~, ?, <, >), calendriers (Grégorien, Julien, Républicain, Hébreu), dates textuelles
- **Person** : Modèle complet avec noms, dates, lieux, événements, relations
- **Family** : Modèle pour les unités familiales avec époux, enfants, événements
- **Event** : Événements personnels et familiaux avec témoins et notes
- **Genealogy** : Conteneur principal avec validation et statistiques

#### 3. Gestion des erreurs
- Exceptions spécifiques : `GeneWebError`, `GeneWebParseError`, `GeneWebValidationError`, `GeneWebConversionError`, `GeneWebEncodingError`
- Messages d'erreur détaillés avec numéros de ligne

#### 4. Parser complet
- **Parser lexical** : Tokenisation complète des fichiers .gw (94% couverture)
- **Parser syntaxique** : Analyse des blocs structurés (fam, notes, rel, etc.)
- **Parser principal** : GeneWebParser avec API simple et robuste
- **Intégration** : Mapping automatique vers les modèles existants
- **Tests d'intégration** : Parser complet avec fichiers réels
- **Performance** : Parsing efficace avec gestion mémoire optimisée

#### 5. API REST avec FastAPI (Phase 3 en cours)
- **API moderne** : FastAPI pour performance et documentation automatique
- **Endpoints REST** : CRUD complet pour personnes, familles, événements
- **Validation** : Pydantic pour validation des données d'entrée
- **Documentation** : OpenAPI/Swagger automatique
- **Middleware** : Gestion d'erreurs, CORS, logging

#### 6. Tests
- **615+ tests** couvrant tous les modules
- **Couverture de code à 83.84%** (objectif initial : 50% largement dépassé ✅)
- Fixtures pour tests avec fichiers .gw d'exemple
- Tests de validation et de cohérence
- Tests d'intégration API complets
- Tests de convertisseurs (JSON, XML, GEDCOM)
- Tests de parsers (lexical, syntaxique, principal)

#### 7. Exemples
- Exemple d'utilisation basique démontrant toutes les fonctionnalités
- Exemple d'utilisation de l'API REST
- Exemple d'utilisation du parser
- Fichiers de fixtures .gw et .gwplus pour tests

### 🚧 Fonctionnalités en cours de développement

#### 1. API REST (Phase 3 - EN COURS)
- [x] Structure FastAPI complète
- [x] Endpoints de base (personnes, familles, événements)
- [x] Modèles Pydantic pour validation
- [x] Middleware et gestion d'erreurs
- [ ] Implémentation complète des services
- [ ] Tests d'intégration API complets
- [ ] Documentation API complète

#### 2. Conversion de formats (Phase 4 - PLANNIFIÉE)
- [ ] Export vers GEDCOM
- [ ] Export vers JSON/XML
- [ ] Import depuis GEDCOM
- [ ] Validation des conversions

## Architecture technique

### Structure des modules

```
geneweb_py/
├── __init__.py              # Exports principaux
├── core/                    # Fonctionnalités principales ✅
│   ├── __init__.py
│   ├── models.py           # Exports des modèles
│   ├── date.py             # Parser et modèle Date
│   ├── person.py           # Modèle Person
│   ├── family.py           # Modèle Family
│   ├── event.py            # Modèle Event
│   ├── genealogy.py        # Modèle Genealogy
│   ├── exceptions.py       # Exceptions spécifiques
│   └── parser/             # Parser lexical, syntaxique et principal ✅
│       ├── __init__.py
│       ├── lexical.py      # Parser lexical
│       ├── syntax.py       # Parser syntaxique
│       └── gw_parser.py    # Parser principal
├── api/                    # API REST avec FastAPI 🚧
│   ├── __init__.py
│   ├── main.py             # Application FastAPI
│   ├── routers/            # Routers par entité
│   ├── models/             # Modèles Pydantic
│   ├── services/           # Services métier
│   └── middleware/         # Middleware personnalisé
├── formats/                # Convertisseurs (Phase 4)
├── utils/                  # Utilitaires (Phase 4)
└── tests/                  # Tests unitaires et d'intégration ✅
```

### Standards de code

- **Type hints** : Obligatoires pour toutes les fonctions publiques
- **Docstrings** : En français pour les APIs publiques
- **Dataclasses** : Utilisées pour tous les modèles de données
- **Tests** : Couverture > 50% (objectif 90%)
- **Formatage** : Black avec ligne de 88 caractères

## Exemples d'utilisation

### Création d'une personne

```python
from geneweb_py import Person, Date, Gender

person = Person(
    last_name="CORNO",
    first_name="Joseph",
    gender=Gender.MALE,
    birth_date=Date.parse("25/12/1990"),
    birth_place="Paris"
)
```

### Parsing de dates complexes

```python
# Date avec préfixe
date = Date.parse("~10/5/1990")  # "about" 10 mai 1990

# Date avec calendrier
date = Date.parse("10/9/5750H")  # Calendrier hébreu

# Date textuelle
date = Date.parse("0(5_Mai_1990)")
```

### Gestion des familles

```python
from geneweb_py import Family, ChildSex

family = Family(
    family_id="FAM001",
    husband_id="CORNO_Joseph_0",
    wife_id="THOMAS_Marie_0",
    marriage_date=Date.parse("10/08/2015")
)

family.add_child("CORNO_Jean_0", ChildSex.MALE)
```

### Validation et statistiques

```python
genealogy = Genealogy()
# ... ajout de personnes et familles ...

# Validation
errors = genealogy.validate_consistency()

# Statistiques
stats = genealogy.get_statistics()
print(f"Total personnes: {stats['total_persons']}")
```

## Tests et qualité

### Exécution des tests

```bash
# Tous les tests
pytest

# Tests unitaires seulement
pytest tests/unit/

# Avec couverture
pytest --cov=geneweb_py --cov-report=html
```

### Couverture actuelle

- **Date** : 87% ⭐ Excellent
- **Family** : 87% ⭐ Excellent  
- **Person** : 94% ⭐ Excellent
- **Event** : 83% ⭐ Excellent
- **Genealogy** : 96% ⭐ Excellent
- **Exceptions** : 95% ⭐ Excellent
- **Parser lexical** : 97% ⭐ Excellent
- **Parser syntaxique** : 85% ⭐ Excellent
- **Parser principal** : 79% ⭐ Excellent
- **API Routers** : 72-78% ⭐ Bon à Excellent
- **API Services** : 67% ⭐ Bon
- **Convertisseurs** : 75-97% ⭐ Excellent

**Total** : 83.84% (objectif : 85% - presque atteint !)

## Prochaines étapes

### Phase 3 : API REST (priorité haute - EN COURS)
1. ✅ Structure FastAPI complète
2. ✅ Endpoints de base et modèles Pydantic
3. 🚧 Implémentation complète des services
4. 🚧 Tests d'intégration API
5. 📋 Documentation API complète

### Phase 4 : Conversion de formats (priorité moyenne)
1. Export GEDCOM
2. Export JSON/XML
3. Import GEDCOM
4. Tests de conversion bidirectionnelle

### Phase 5 : Optimisations (priorité basse)
1. Amélioration de la couverture de code
2. Optimisation des performances
3. Gestion avancée des erreurs
4. Documentation avancée

## Contribution

### Installation pour le développement

```bash
git clone <repository>
cd geneweb-py
pip install -e .[dev]
```

### Standards de commit

- Messages en français
- Tests obligatoires pour les nouvelles fonctionnalités
- Couverture de code maintenue
- Documentation mise à jour

### Workflow

1. Créer une branche feature
2. Implémenter avec tests
3. Vérifier la couverture
4. Créer une PR
5. Review et merge
