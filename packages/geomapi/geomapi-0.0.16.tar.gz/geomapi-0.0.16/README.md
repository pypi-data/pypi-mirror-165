![geomapiLogo](docs/source/_static/geomapi_logo_B.png)
# GeomAPI

A joint API to standardize geomatic data storage and processing.

[[_TOC_]]

## Installation

Use the package manager [pip](https://pypi.org/project/geomapi) to install geomapi.

```bash
pip install geomapi
```

## Documentation

You can read the full API reference here:
[Documentation](https://geomatics.pages.gitlab.kuleuven.be/research-projects/geomapi/)


## Usage

The main use of this API is importing standardized RDF data into easy to use python classes.
These python classes have a number of fuctions to analyse, edit and combine the most common types of data including:
- Images (pinhole or panoramic)
- Meshes
- Point clouds
- BIM models

## Variable Standards

This library relies on a RDF based standardisation of data storage, Below are some of the more important variables:

- `cartesianTransform`: A 4x4 transformation matrix 
- Paths
  - `path`: The absolute path of the Asset.
  - `graphPath`: the absolute path of the graph folder


## Development

Testing the package is done in the tests folder with:
```py
from context import geomapi
```

### Work method

- nieuwe code comitten, aanpassingen brachen of aan MB vragen
- nieuwe dependencies worden gestemd

#### input protection/ error handling
- try catch blokken
- zoveel mogelijk protection binnen functie
- type hinting input + output

#### documentatie (uitleg, eenheid , datatype)
- uitleg bij functie
- uitleg bij parameters
- type hinting input + output
	
#### standardisatie
- beperk custom classes waar mogelijk 
- beperk aantal argumenten
- gebruik zoveel mogelijk standaardconcepten
- name is zonder speciale tekens of spaties (door windows en RDFlIB)
	
#### PYTHON
- module/files: allemaal kleine letters
- classes: Capital elk woord
- functie: allemaal kleine letters met underscores
- variables: kleine letters, allemaal aan elkaar, 2de woord capital
- niet teveel afkortingen
	
### FUNCTIONS
- histogram in a certain direction
- split horizontal from vertical points
- create virtual image
- triplestore
- documentation
- fix graphPath constructor
- crop point clouds
- collision point clouds
- make imagenodes from vlx metadata

#### KWALITEITSANALYSE
- rendering van KWALITEITSANALYSE

#### CROP MESHES
- check mesh collision functions
- crop_geometry first run a check if the Bboxes intersect => saves alot of intersection calculations
- crop_geometry add non_overlapping bool parameter that culls mesh with each selection => should speed up process
- crop geometry functions have a lot of deepcopies which hurt performance
- intersection based on convex hull

- crop geometry 1m30 on 600 nodes with 40k mesh => for 2M mesh and 6000 boxes this would take 1h30
- trimesh mesh intersection 2m17 for 600 nodes on 40k mesh =>for 2M mesh and 6000 boxes 1000min

#### CROP PCDS
- Python has to memory allocation protection :'(
- create CC script thats loads pcd's and outputs pcd
- segment large pcd's into regions
- BBoxes pcd are to large

- crop BB 4m30s for 6x10M pcd 600 boxes => for 45 clouds and 6000 boxes (normal project) this would take 5h30
- segmentation based on Eucl. distance 5ms for 6x10M pcd 600 meshes => for 45 clouds and 6000 boxes (normal project) this would take 6h

#### GEOMETRY
- protect oriented bounding box en bounding box tegen puntenwolken met te weinig punten (coplanair of 1pnt)
- e57 scanheader also contains oriented bounding box?

#### LINKED DATA 
- functie node.get_oriented_bounding_box()

#### IMAGENODE
- implementeer xml import

#### ENVIRONMENT
- python-fcl is causing crashes!

## Licensing

The code in this project is licensed under GNU license.
