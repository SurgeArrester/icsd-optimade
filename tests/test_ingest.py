import json

from optimade.models.structures import StructureResource


def test_cif_mapper(icsd_client):
    from icsd_optimade.ingest import map_cif_to_optimade

    json_str = map_cif_to_optimade(111000, icsd_client)
    assert StructureResource(**json.loads(json_str))
