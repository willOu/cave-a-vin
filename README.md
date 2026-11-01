# Cave à vin

Application web pour gérer sa cave : quelles bouteilles on a, et où elles sont rangées.

Elle tourne aujourd'hui comme un Artifact claude.ai : https://claude.ai/artifact/5voMMV4i7cNYPizfvQuC7V

## Fonctionnalités

- **Plusieurs caves**, choisies dans les Réglages, chacune avec ses casiers (étagères × bouteilles, rangement côte à côte ou en quinconce, deuxième rangée posée sur la première).
- **Trois vues de la cave** : Étagères (toute la cave d'un coup), Plan (grille) et 3D (cave de service électrique, Three.js).
- **Déplacer une bouteille** en restant appuyé dessus puis en la glissant. Lâchée sur une place occupée, elle échange sa place avec l'autre bouteille.
- **Fiche vin** : domaine, ville du producteur, millésime, appellation, région, bassin, couleur, cépages, garde, prix, notes, et jusqu'à deux photos (étiquette, contre-étiquette).
- **« Bouteille bue »** avec confirmation et historique. L'historique peut être effacé.
- **Carte de France** : les bassins viticoles et les villes des producteurs, au choix pour les vins en cave ou pour tous les vins bus depuis le début.
- **Responsive** : mise en page téléphone, et mise en page ordinateur à partir de 1000 px de large.
- Thème « Grand Cru » (aubergine et or, Bodoni Moda + Manrope).

## Fichiers

| Fichier | Rôle |
|---|---|
| `index.html` | Toute l'application : HTML, CSS et JS, avec la carte (`GEO`) intégrée. |
| `communes.js` | Les 35 000 communes de France (`nom\|département\|longitude\|latitude`), triées par population. Chargé à la demande pour la recherche de la ville du producteur. |
| `data/bassins-viticoles-france.geojson` | Les bassins viticoles, source de la carte. |
| `tools/build_geo.py` | Régénère `GEO` et `communes.js` à partir des GeoJSON (voir l'en-tête du script). |

## Stockage des données

L'application utilise les capacités d'exécution des Artifacts claude.ai, appelées via `window.claude.use(...)` :

- `db` : base partagée. Collections `cellars`, `racks`, `wines`, `drunk` et document `settings/display`.
- `assets` : photos d'étiquettes. Le vin garde l'identifiant de la photo dans `labels`, et l'affiche via `/_blob/<id>`.
- `user` : l'utilisateur connecté.

Ouverte en dehors de claude.ai (en local ou sur GitHub Pages), la page s'affiche mais ne peut ni lire ni enregistrer de données. Pour l'héberger ailleurs, il faut remplacer ces appels par une autre base de données, par exemple Supabase ou Firebase.

## Sources des données géographiques

- Bassins viticoles : GeoJSON fourni par William.
- Contour de la France et communes : [gregoiredavid/france-geojson](https://github.com/gregoiredavid/france-geojson).
- Populations des communes : [@etalab/decoupage-administratif](https://www.npmjs.com/package/@etalab/decoupage-administratif).
