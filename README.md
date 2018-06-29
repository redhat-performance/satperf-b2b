# Satellite Build to Build Visualizer
The tool aims to leverage the existing Satellite Monitoring Infrastructure to provide easy build to build
comparison of the different metrics that are available from Red Hat Satellite.

## Features
---
The current version of Build to Build Visualizer provides the following features:

* Ability to select Different Builds
* Ability to visualize a selected metric from different builds

## Current Development Status
---
Alpha

## APIs
---
### Create a New Build Record
When a benchmark completes, a new build record needs to be created inside the visualizer. 

API Endpoint: /newbuild

TYPE: POST

Parameters:

* build_tag -- A tag denoting the build of the Product
* benchmark_name -- The name of the benchmark that was ran
* hostname -- The host from which data needs to be collected
* start_time -- The time at which the benchmark started
* end_time -- The time at which the benchmark ended