import json
from io import BytesIO

import ase.io
from optimade.adapters import Structure

from .client import ICSDClient
from .utils import get_cif


def map_cif_to_optimade(entry_id: int, client: ICSDClient) -> str | RuntimeError:
    """For a given ICSD entry ID (CollCode), either look up a cached
    copy of the CIF or download from the ICSD API and map it into an OPTIMADE
    Structure resource via ASE, returning a JSON string of the structure.

    Returns:
        A JSON string representing the structure, or a RuntimeError if the parsing failed.

    Raises:
        Forbidden: If the CIF download failed for rate-limit reasons.

    """

    cif_bytes = get_cif(entry_id, client)

    try:
        with BytesIO(cif_bytes) as fp:
            atoms = ase.io.read(fp, format="cif")
    except Exception as exc:
        return RuntimeError(f"Unable to convert CIF to ASE atoms: {exc}")

    try:
        structure = Structure.ingest_from(atoms)
    except Exception as exc:
        return RuntimeError(f"Unable to convert ASE atoms to OPTIMADE structure: {exc}")

    entry = structure.entry.model_dump()
    entry["id"] = str(entry_id)
    entry["attributes"]["immutable_id"] = str(entry_id)
    # ASE spg cannot be serialized as JSON, first just take the number
    entry["attributes"]["_ase_spacegroup"] = entry["attributes"]["_ase_spacegroup"].no  # type: ignore
    return json.dumps(entry)
