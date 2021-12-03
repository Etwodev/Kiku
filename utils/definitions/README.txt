All references for active programs are stored here, whether it's embed information, error information, filetype information etc.
For each type please split into a seperate file. Like this:

$ ls utils/definitions

> README.txt
> errors.py
> commands.py
> listeners.py
> file_types.py

For command embeds, things are slightly different and use a specialised naming system to make it easier to adjust.
Without denoting the state, command and reference, it can get very cluttered. So for this, I designed this dummy-system.

COMMANDS
are easy enough to understand, the original command name always comes first.

STATES
are the second part of the name is the state- either primary, secondary, teriary or quaternary. This is the order in which they will be triggered.
These will be always triggered.

OUTCOMES
are the results of the states, if there is no results found for a specific command, that would be an outcome. Outcomes are denoted by some sort of keyword,
such as none, clean, etc.

Combining this together with an example command of lookup, we get:

lookup_primary_loading
> Loading
lookup_secondary_clean
> Here you go! {Image}
lookup_secondary_none
> Oops! No tags found...