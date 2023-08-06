Changelog
*********

- 1.0.22 - 2022-08-31
    - Bugfix for `FlowsSplit.Sources` value in `Flows`

- 1.0.21 - 2022-08-25
    - Documentation updates

- 1.0.20 - 2022-04-12
    - Documentation updates
    - Bugfix for `vessel_states` values in `Diversions`

- 1.0.19 - 2022-04-06
    - Add `crude quality` split for `Flows` and `Fleet Metrics`
    - Add `Diversions` feature on LNG platform

- 1.0.17 - 2021-11-22
    - Add `vessel_types` and `vessel_types_alt` (oil liquids platform only) filters for `Flows` and `Fleet Metrics`

- 1.0.16 - 2021-11-17
    - Add `without_eia_adjustment` param for `Inventories`

- 1.0.15 - 2021-10-12
    - Add `vessels` param for vessels endpoint for `Fleet Utilization`, `Congestion` and `Fleet Development`

- 1.0.14 - 2021-09-15
    - Add `period` param for vessels endpoint for `Fleet Utilization` and `Congestion`
    - Add new params for `Fleet Utilization` according to the documentation

- 1.0.13 - 2021-09-08
    - fix change log

- 1.0.12 - 2021-08-20
    - fix typo in `Trades` doc

- 1.0.11 - 2021-08-20
    - add new splits for `Flows` & `Fleet Metrics`
    - add new client `InventoriesCushingDrone`

- 1.0.8 - 2021-06-18
    - review dependencies
    - licensing source code

- 1.0.7 - 2021-06-01
    - add `with_product_estimation` parameter for trades
    - documentation updates
    - availability to update the endpoints url for dev purpose

- 1.0.5 - 2021-02-24
    - add `withFreightView` param according to the documentation
    - add `withOrderbook` param according to the documentation
    - add Contracting metric for fleet-development series/vessels
    - add product and grade split for congestion series
    - add `Fleet Metrics` feature on LNG platform

- 1.0.4 - 2021-01-29
    - fix boolean fields always reflecting as `True` in pandas
    - continuous integration improvements

- 1.0.3 - 2021-01-13
    - change version requirement for a lib : `numpy>=1.19.0`
    - new versions notification through a log message on `Configuration` object creation
    - better error handling on authentication failure

- 1.0.2 - 2020-12-17
    - allow proxy configuration in `Configuration` object
    - allow usage of local ssl certificate in `Configuration` object
    - allow disabling of ssl verification (default set to False) in `Configuration` object

- 1.0.1 - 2020-12-09
    - module and classes names uniformization
    - fix usage of doc string

- 1.0.0 - 2020-12-09
    - first version
