# ProGRESS v2.0.1 Release Notes

**Release date:** September 25, 2026

## Summary

ProGRESS v2.0.1 is a patch release with no new features or dependencies.

## Fixed

- Fixed a timezone error when parsing solar observation data.
- Fixed wind resource state handling in the Monte Carlo and example-simulation workflows.

## Upgrade Notes

- Python 3.11 or greater, same as v2.0.0. No new dependencies, so existing v2.0.0 environments can upgrade in place.
- macOS and Windows executables are attached to the GitHub release.

## Assets

- Standalone ProGRESS executables for macOS and Windows, bundling GLPK for dispatch and HiGHS for PCM. Other solvers require a source installation or a custom rebuild (see [Building the Executable](https://github.com/sandialabs/snl-progress/wiki/Building-the-Executable)).
- `pip install snl-progress==2.0.1`
