# rust_decider

Rust implementation of bucketing, targeting, overrides, and dynamic config logic.

## Usage

```sh
# In a virtualenv, python >= 3.7
$ pip install -r requirements-dev.txt
$ maturin develop
$ python
```

```python
import rust_decider

# Init decider
decider = rust_decider.init("darkmode fractional_availability value", "../cfg.json")

# Bucketing needs a context
ctx = rust_decider.make_ctx({"user_id": "8"})

# Get a decision
x = decider.choose("exp_1", ctx)
assert x.err() is None # check for errors
x.decision() # get the variant

# Get a dynamic config value
y = decider.get_map("dc_map", ctx) # fetch a map DC
assert y.err() is None # check for errors
y.val() # get the actual map itself
```

## Development

`cd decider-py/` and run `maturin develop` to build `reddit-decider` python wheel.

## Publishing

Package is automatically published on merge to master to https://pypi.org/project/reddit-decider/ via drone pipeline.

# Formatting / Linting

```sh
$ cargo fmt    --manifest-path decider-py/test/Cargo.toml
$ cargo clippy --manifest-path decider-py/test/Cargo.toml
```
