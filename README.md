# textsheet

`textsheet` is a small python script allowing for spreadsheet-like functionality in text files.

## Installation

1. Clone the repository.
2. Run `py textsheet.py <path/to/your/file>` to open textsheet.

## Usage

`textsheet` works on text files containing **T**ab **S**eperated **V**alues (TSV).
Additionally these files may have a line containing `__code__` followed by lines of valid python code.
This code will be executed on loading the file with `textsheet` and on each saved change to the file.

To easily view TSV files a text editor with support for elastic tabstops is recommended.

## Examples

### Simple

Loading the following file with `textsheet`:
```
a	b	sum
4	5
__code__
set(2,3, val(2,1) + val(2,2))
```
will result in the following outcome:
```
a	b	sum
4	5	9
__code__
set(2,3, val(2,1) + val(2,2))
```

### Basic API
Loading the following file with `textsheet`:
```
a	b	sum
4	5
3	134
35	5
34	89
END
__code__
i = 2
while(get(i,1) != "END"):
	set(i,3, val(i,1)+val(i,2))
	i += 1
```
will result in the following outcome:
```
a	b	sum
4	5	9
3	134	137
35	5	40
34	89	123
END
__code__
i = 2
while(get(i,1) != "END"):
	set(i,3, val(i,1)+val(i,2))
	i += 1
```

## API

*todo*
