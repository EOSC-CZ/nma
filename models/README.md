# `models` folder

Contains generated models. 

## Creating models

```bash
nrp model add <model-name> --config <custom config> \
  --use <custom model>[:<jsonpath>] \
  --no-input
```

Will create a new model. You can provide your own oarepo.yaml
config for the model via the --config option (to get the format,
run the command without --config, answer all the questions
and then copy the model part of the oarepo.yaml to your own file)

You can also include a custom model. The file will be copied
to the destination and referenced from the generated model file.
If no path is specified, it will be referenced from the root
of the file, with path the reference will be put there.

Use `--no-input` to disable asking questions (and be sure to
run it with `--config`)

## Compiling models

```bash
nrp model compile <model-name>
```

This command will compile your model into invenio sources

## Installing models

```bash
nrp model install <model-name> [<site-name>]
```

Will install the model into the given site. Site name 
can be omitted if there is only one site in the monorepo.

## Uninstalling models

```bash
nrp model uninstall <model-name> [<site-name>] [--remove-directory]
```

Will uninstall the model from the given site. Site name 
can be omitted if there is only one site in the monorepo.
