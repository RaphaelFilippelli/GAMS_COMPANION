# model_runner.py — Specification

## run_gams(work_dir, gms_file, gdx_out, options=None) → Path
- Copy `work_dir` to a temp dir.
- Run GAMS via Python API, passing `options`.
- On success, copy `gdx_out` to `runs/<timestamp>/raw.gdx` and return its Path.
- On failure, raise `RuntimeError`; copy the `.lst` to the same `runs/` folder.

## get_run_log_txt(run_dir) → str
- Returns the text of the first `.lst` file inside `run_dir` or a short message if none.
