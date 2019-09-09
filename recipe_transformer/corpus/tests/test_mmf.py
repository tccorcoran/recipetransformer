from recipe_transformer.corpus.mmf import mmf_reader


def test_mmf_reader(resources_dir):
    assert len(list(mmf_reader(resources_dir / "1000.mmf"))) == 35736
