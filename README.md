# TimeAggregator

A simple little calculator that sums up timeranges.

Useful if you keep tasklists in sublime and want to quickly see aggregated times.


Example:

	00:20 Clean room
	01:00 Watch TV
	01:30 Do homework


With TimeAggregator you can easily get to this:

	00:20 Clean room
	01:00 Watch TV
	01:30 Do homework
    02:50 << TIMESUM   (2017-11-04 13:36:10)


Just search for "TimeAggregator" in Sublimes Command Palette.

There are 2 Modes:

* Running it at the current cursor position will insert the summed up value at the current cursor position.
* Running it on all lines that contain the magic string "<< TIMESUM".