# Exploration

## Overview

This program provides data types for representing the exploration of
spaces that can defined (or abstracted) in terms of discrete decisions,
such as videogame levels with multiple rooms and also other things like
conversation trees or a city block grid.

It represents space using a `DecisionGraph`, which is a multi-di-graph
indicating the transition(s) between decisions, which can include
information about prerequisites for transitions as well as effects a
transition might have on the world. There is also a convention for
representing unexplored regions using specially-tagged nodes of the
graph. An `Exploration` is a sequence of `DecisionGraph`s, along with a
sequence of decisions indicating where the explorer was at each step, a
sequence of transitions indicating which transition was taken at each
step, and a sequence of states indicating extra state at each step. These
representations were developed with Metroidvania games in mind.

Core capabilities include:

- Representing exploration processes as a series of decisions including
    partial information about not-yet-explored decisions.
- Reasoning about reachability modulo transition requirements in terms of
    powers that must be possessed and/or tokens that must be spent for a
    transition. TODO
- The ability to represent fairly sophisticated game logic in the
    `DecisionGraph`, and even construct playable maps. Game logic that
    can't be captured this way can still be represented through making
    custom changes to maps between exploration steps. TODO
- Creating maps and explorations from various text formats, including
    exploration journal formats. TODO

## Dependencies:

- Python version 3.7+
- `networkx` For underlying graph structures.
- `pytest` for testing, install with `[test]` option to get it automatically.

## Installing

Just run `pip install exploration`. The `egtool` script should be
installed along with the module.

You can then run `python -m exploration.tests` to run tests.

## Getting Started:

The `egtool` script provides a command-line interface to core
functionality. The `exploration.main` module provides equivalent entry
points from Python. `exploration.core` provides the main types and
explains how they fit together.

## Plans

- Better support for open-world games, where decisions are not as closely
    linked to virtual space structure.

## Changelog

- v0.1.2 Core functionality (`core.py`) is working & tested, with the
    exception of the zones system. Journals are not working, and tests
    for those have been disabled for now. Could be used for
    representation purposes, but is not yet complete. This version is
    effectively the first alpha release since I'm demoing at the PCG
    workshop. Note most of the 'core capabilities' are still TODO.
- v0.1.1 Still pre-alpha as it's in the process of being re-architected a
    bit, but some core functionality is present if rough (e.g.,
    `core.DecisionGraph` and `core.Exploration`).
- v0.1 Initial pre-alpha upload.
