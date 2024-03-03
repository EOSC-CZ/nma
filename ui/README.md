# `ui` folder

Contains user interface for your repository.

## Creating UI

```bash
nrp ui add <model-name> --config <custom config> \
  --no-input
```

Will create a template of a UI.

Use `--no-input` to disable asking questions (and be sure to
run it with `--config`)

## Installing UI

```bash
nrp ui install <ui-name> [<site-name>]
```

Will install the ui into the given site. Site name 
can be omitted if there is only one site in the monorepo.

## Uninstalling UI

```bash
nrp ui uninstall <ui-name> [<site-name>] [--remove-directory]
```

Will uninstall the ui from the given site. Site name 
can be omitted if there is only one site in the monorepo.
