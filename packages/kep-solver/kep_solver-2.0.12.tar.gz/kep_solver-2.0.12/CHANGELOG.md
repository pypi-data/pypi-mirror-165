# Changelog

## [2.0.12]

- Fixed bug with single altruistic donors (i.e. chains containing just an
	altruistic donor) counting as containing an effective two-way exchange.

## [2.0.11]

- Add documentation of output format

## [2.0.10]

- Bug fixes for the JSON output.

## [2.0.9]

- Add support for JSON output (in UK style). This involved some refactoring, as
	this output needs to know the model used to solve an instance.
- Add tests for JSON output
- pool.Pool objects now must have a string description
- pool.Pool exposes maxCycleLength and maxChainLength as properties
- pool.solve\_single() now returns a Solution and the Model used to find it
- model.UK\_age\_score(): Move the UK age scoring into its own function
- Hide pulp warnings on overwriting objectives

## [2.0.8]

- More fixes for backarcs. Make sure that a backarc exchange only has two
	vertices in it, otherwise we might accidentally catch a long chain in the
	reverse direction.
- EffectiveTwoWay: Chains should be counted.

## [2.0.7]

- The CycleAndChainModel needs all cycles and exchanges to have unique IDs, so
	force this.
- Accidentally missed version 2.0.6

## [2.0.5]

- Another backarc calculation fix. Each arc should have at most one "backarc"
	exchange, even if there are multiple other exchanges that could match the
	correct recipients (due to some of said recipients having multiple donors).

## [2.0.4]

- Equality comparisons of exchanges only considers exchange IDs now
- Fix backarc calculation. Backarcs can use different donors, but must have the
	right recipients

## [2.0.3]

- Fix error with Pulp and empty objectives

## [2.0.2]

- Rework UK backarcs. To match existing code, these are implemented in a
	specific manner.
- Alternate and embedded exchanges for cycles must be cycles, and alternate and
	embedded exchanges for chains must be chains that use the same non-directed
	donor
- Add __repr__ to Donor

## [2.0.0]

- New class for Exchange objects
- Add build\_alternates\_and\_embeds() function to find alternate and embedded
	cycles
- Update documentation to add example of CompatibiltyGraph usage
- Moved to [Black](https://black.readthedocs.io/en/stable/) for formatting

## [1.0.4]

- Use setuptools\_scm for versioning

## [1.0.3]

- Fix continuous deployment

## [1.0.2]

- Fix documentation

## [1.0.1]

- Add ability to read blood groups of donors and recipients
- Add Recipient.pairedWith(Donor) function
- Add custom exceptions for data IO
- Allow variations of bloodgroup/bloodtype in input
- Allow variations of cPRA/PRA/cpra in input
- Add functions for blood group compatibility checks to Donor and Recipient

## [1.0.0]

First release
