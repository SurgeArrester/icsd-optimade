import json
from pathlib import Path


def test_ingest(tmpdir):
    from icsd_optimade.ingest import ingest_by_year

    # Symlink any cached cifs from main data dir
    data_dir = Path(__file__).parent.parent / "data" / "cifs"
    tmp_data_dir = Path(tmpdir / "data")
    tmp_data_dir.mkdir(parents=True, exist_ok=True)
    (tmp_data_dir / "cifs").symlink_to(data_dir)

    ingest_by_year(
        run_name="test",
        pool_size=1,
        start_year=1987,
        end_year=1987,
        data_dir=Path(tmpdir / "data"),
        log_level="debug",
        skip_download=True,
    )

    assert (Path(tmpdir) / "data" / "cifs").is_dir()
    assert len(list((Path(tmpdir) / "data" / "cifs").iterdir())) > 0
    assert (Path(tmpdir) / "data" / "test-optimade.jsonl").is_file()

    with open(Path(tmpdir) / "data" / "test-optimade.jsonl") as f:
        line = f.readline()
        other_lines = f.readlines()

    header = json.loads(line)
    assert header["x-optimade"]
    assert header["x-optimade"]["meta"]["api_version"] == "1.2.0"
    (json.load(line) for line in other_lines)
    assert len(other_lines) == 696
