# Cave à vin

Application web pour gérer sa cave : quelles bouteilles on a, et où elles sont rangées.

Elle existe en deux versions issues du même fichier :

- l'application installable (PWA) : https://willou.github.io/cave-a-vin/
- l'Artifact claude.ai : https://claude.ai/artifact/5voMMV4i7cNYPizfvQuC7V

## Fonctionnalités

- **Plusieurs caves**, choisies dans les Réglages, chacune avec ses casiers (étagères × bouteilles, rangement côte à côte ou en quinconce, deuxième rangée posée sur la première).
- **Trois vues de la cave** : Étagères (toute la cave d'un coup), Plan (grille) et 3D (cave de service électrique, Three.js).
- **Déplacer une bouteille** en restant appuyé dessus puis en la glissant. Lâchée sur une place occupée, elle échange sa place avec l'autre bouteille.
- **Fiche vin** : domaine, ville du producteur, millésime, appellation, région, bassin, couleur, cépages, garde, prix, caviste et date d'achat, température de service (conseillée selon la couleur) et carafage, notes, et jusqu'à deux photos (étiquette, contre-étiquette).
- **Coups de cœur** ♥ sur la fiche, avec un filtre et un tri dédiés. Boutons + et − pour ajuster les bouteilles non rangées.
- **Liste des vins** : recherche dans toutes les caves (nom, domaine, ville, caviste, code-barres…), tri par nom, millésime, garde, quantité, prix, coups de cœur ou achats récents.
- **Doublons** : à l'ajout d'un vin déjà présent (même nom, millésime et domaine), l'appli propose d'ajouter les bouteilles à la fiche existante.
- **« Bouteille bue »** avec confirmation, note sur 5, plat et commentaire de dégustation. Ces notes se modifient dans l'historique, qui peut aussi être effacé. Une bouteille bue par erreur se remet en cave (bouton « Annuler » juste après, ou « Remettre en cave » dans l'historique) : elle retrouve sa place si elle est libre.
- **Que boire ce soir ?** : on décrit un plat et Claude choisit jusqu'à 3 bouteilles de la cave, en privilégiant celles à boire.
- **Bilan** : valeur estimée, prix moyen, répartitions par couleur, garde, bassin et millésime, bouteilles bues par mois, meilleures dégustations.
- **Scanner l'étiquette** : Claude lit la photo et pré-remplit la fiche (nom, domaine, millésime, appellation, ville, cépages, garde). La photo devient la photo d'étiquette.
- **Code-barres** : lu depuis une photo (BarcodeDetector, sinon ZXing). Le code est enregistré sur le vin, et le scanner retrouve ensuite ce vin dans la cave.
- **Carte de France** : les bassins viticoles et les villes des producteurs, au choix pour les vins en cave ou pour tous les vins bus depuis le début.
- **Responsive** : mise en page téléphone, et mise en page ordinateur à partir de 1000 px de large.
- Thème « Grand Cru » (aubergine et or, Bodoni Moda + Manrope).

## Application installable (PWA)

Le site https://willou.github.io/cave-a-vin/ est l'application installable sur téléphone et ordinateur (GitHub Pages, branche `main`, dossier racine).

- **Installer** : sur iPhone, Partager puis « Sur l'écran d'accueil ». Sur Android, menu ⋮ puis « Installer l'application ». Sur ordinateur, l'icône d'installation de Chrome ou Edge.
- **Données** : stockées sur l'appareil (IndexedDB), photos comprises. L'application fonctionne hors connexion.
- **Sauvegarde** : Réglages, puis Exporter ou Importer. Un même fichier JSON passe entre l'Artifact claude.ai et l'application installée, ou d'un appareil à l'autre.
- **Claude** : « Que boire ce soir ? » et le scan d'étiquette appellent l'API Anthropic (`claude-opus-5-5`) avec la clé API de l'utilisateur. Cette clé se saisit dans Réglages et reste dans le `localStorage` de l'appareil. Sans clé, ces deux fonctions sont masquées.

## Fichiers

| Fichier | Rôle |
|---|---|
| `src/app.html` | La source de l'application, publiée telle quelle comme Artifact claude.ai. |
| `index.html` | L'application installable, générée depuis `src/app.html` par `tools/build_pwa.py`. |
| `sw.js` | Service worker (hors connexion, mises à jour), généré depuis `tools/sw.template.js`. |
| `manifest.webmanifest`, `icons/` | Nom, couleurs et icônes de l'application installée. |
| `communes.js` | Les 35 000 communes de France (`nom\|département\|longitude\|latitude`), triées par population. Chargé à la demande pour la recherche de la ville du producteur. |
| `data/bassins-viticoles-france.geojson` | Les bassins viticoles, source de la carte. |
| `tools/build_geo.py` | Régénère `GEO` et `communes.js` à partir des GeoJSON (voir l'en-tête du script). |

Après une modification de `src/app.html`, lancez `python3 tools/build_pwa.py`, puis committez `index.html` et `sw.js`.

## Stockage des données

L'application utilise les capacités d'exécution des Artifacts claude.ai, appelées via `window.claude.use(...)` :

- `db` : base partagée. Collections `cellars`, `racks`, `wines`, `drunk` et document `settings/display`.
- `assets` : photos d'étiquettes. Le vin garde l'identifiant de la photo dans `labels`, et l'affiche via `/_blob/<id>`.
- `user` : l'utilisateur connecté.
- `sample` (avec images) : demandes à Claude pour les accords mets-vins et la lecture d'étiquette. Elles sont faites sur le compte claude.ai de la personne qui utilise l'appli.

Hors de claude.ai, `window.claude` n'existe pas : la page bascule alors sur un équivalent local (`Local.db`, `Local.assets`, et `localSample()` pour Claude) avec la même interface. Pour synchroniser plusieurs appareils, il suffirait de remplacer `Local.db` par une base en ligne (Supabase par exemple) qui offre les mêmes méthodes.

## Sources des données géographiques

- Bassins viticoles : GeoJSON fourni par William.
- Contour de la France et communes : [gregoiredavid/france-geojson](https://github.com/gregoiredavid/france-geojson).
- Populations des communes : [@etalab/decoupage-administratif](https://www.npmjs.com/package/@etalab/decoupage-administratif).
