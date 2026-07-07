from utils.recent_files import add_recent_file, clear_recent_files, load_recent_files, MAX_RECENT_FILES


def test_recent_files_round_trip(tmp_path):
    clear_recent_files()
    files = [str(tmp_path / f"file_{i}.parquet") for i in range(3)]
    for path in files:
        add_recent_file(path)

    recent = load_recent_files()
    assert recent == list(reversed(files))


def test_recent_files_dedupes_and_limits(tmp_path):
    clear_recent_files()
    first = str(tmp_path / "a.parquet")
    second = str(tmp_path / "b.parquet")

    add_recent_file(first)
    add_recent_file(second)
    add_recent_file(first)

    recent = load_recent_files()
    assert recent == [first, second]

    for i in range(MAX_RECENT_FILES + 5):
        add_recent_file(str(tmp_path / f"extra_{i}.parquet"))

    assert len(load_recent_files()) == MAX_RECENT_FILES

    clear_recent_files()
    assert load_recent_files() == []
