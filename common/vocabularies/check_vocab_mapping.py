import click


@click.command()
@click.argument("vocab_yaml_file", type=click.Path(exists=True))
def check_vocab_mapping(vocab_yaml_file):
    """Check the vocabulary mapping in the given YAML file."""
    import yaml

    with open(vocab_yaml_file, "r") as file:
        vocab_data = list(yaml.safe_load_all(file))

    for vocab in vocab_data:
        vocab_id = vocab.get("id")
        iri = vocab["props"]["iri"]

        if "#" in iri:
            id_from_iri = iri.rsplit("#")[-1]
        else:
            id_from_iri = iri.strip("/").rsplit("/")[-1]

        if vocab_id != id_from_iri:
            click.echo(f"Mismatch in vocabulary ID: {vocab_id=} vs {id_from_iri=}")


if __name__ == "__main__":
    check_vocab_mapping()
