import datetime
import json

from optimade.models import ReferenceResource, StructureResource


def test_cif_mapper(icsd_client):
    from icsd_optimade.ingest import map_cif_to_optimade

    json_str = map_cif_to_optimade(111000, icsd_client)

    struc_dct = json.loads(json_str.split("\n")[0])
    ref_dct = json.loads(json_str.split("\n")[1])
    assert struc_dct
    assert ref_dct
    structure = StructureResource(**struc_dct)
    assert structure

    reference = ReferenceResource(**ref_dct)
    assert reference

    assert structure.id == "604000"
    assert structure.attributes.immutable_id == "604000"
    assert structure.attributes.elements == ["Ir", "Si", "U"]
    assert structure.attributes.last_modified == datetime.datetime(2019, 8, 1)

    assert structure.relationships.references.data[0].id == "604000"
