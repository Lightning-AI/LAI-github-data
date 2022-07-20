## BLOCKERS
- [bug] loading credentials crashes the app 
```shell
Traceback (most recent call last):
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/lightning_app/core/app.py", line 307, in maybe_apply_changes
    state += delta
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/deepdiff/delta.py", line 131, in __add__
    self._do_dictionary_item_added()
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/deepdiff/delta.py", line 276, in _do_dictionary_item_added
    self._do_item_added(dictionary_item_added, sort=False)
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/deepdiff/delta.py", line 297, in _do_item_added
    items = items.items()
AttributeError: 'list' object has no attribute 'items'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/bin/lightning", line 8, in <module>
    sys.exit(main())
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/click/core.py", line 1130, in __call__
    return self.main(*args, **kwargs)
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/click/core.py", line 1055, in main
    rv = self.invoke(ctx)
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/click/core.py", line 1657, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/click/core.py", line 1657, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/click/core.py", line 1404, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/click/core.py", line 760, in invoke
    return __callback(*args, **kwargs)
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/lightning_app/cli/lightning_cli.py", line 115, in run_app
    _run_app(file, cloud, without_server, no_cache, name, blocking, open_ui, env)
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/lightning_app/cli/lightning_cli.py", line 81, in _run_app
    dispatch(
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/lightning_app/runners/runtime.py", line 63, in dispatch
    return runtime.dispatch(on_before_run=on_before_run, name=name, no_cache=no_cache)
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/lightning_app/runners/multiprocess.py", line 87, in dispatch
    self.app._run()
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/lightning_app/core/app.py", line 392, in _run
    done = self.run_once()
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/lightning_app/core/app.py", line 325, in run_once
    self.maybe_apply_changes()
  File "/Users/ericchea/Developer/opensource/repos/LAI-github-data/.venv/lib/python3.9/site-packages/lightning_app/core/app.py", line 309, in maybe_apply_changes
    raise Exception(f"Current State {state}, {delta.to_dict()}") from e

```



# lai_github app

This ⚡ [Lightning app](lightning.ai) ⚡ was generated automatically with:

```bash
lightning init app lai_github
```

## To run lai_github

First, install lai_github (warning: this app has not been officially approved on the lightning gallery):

```bash
lightning install app https://github.com/theUser/lai_github
```

Once the app is installed, run it locally with:

```bash
lightning run app lai_github/app.py
```

Run it on the [lightning cloud](lightning.ai) with:

```bash
lightning run app lai_github/app.py --cloud
```

## to test and link

Run flake to make sure all your styling is consistent (it keeps your team from going insane)

```bash
flake8 .
```

To test, follow the README.md instructions in the tests folder.
