# hedit
`hedit` edits header of FITS file.

usage: im hedit [-h] [--value VALUE] [--comment COMMENT] [--delete] [--value-is-key] file key

positional arguments:
  file               A file path or pattern (e.g., "*.fits")
  key                Key for the header card

options:
  -h, --help         show this help message and exit
  --value VALUE      Value for the header card
  --comment COMMENT  Value for the header card
  --delete           Delete the header card
  --value-is-key     Copy value form the card
