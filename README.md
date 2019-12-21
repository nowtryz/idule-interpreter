Idule interpreter
=================

This project is design to parse and run Idule scripts.

## Idule specifications

### GET
```
get <url>
```
`get` fetch data from a url, and return a *set* containing the list of lines.

### STAT
```
stat <set> (intersect | diff | union) <set> <contraint>
```
Computes the union, difference or intersection and give some statistics about it.

### Assignment
```
r1 = <set>
```
Store the *set* or a string in a variable, this variable can then be used as a *set* in any other operation.

```
r1 = <string>
```
Store the *string* in a variable that can then be used as a word for a constraint. Variable can be printed by simply
typing their name. This *string* must only contains letters, digits, underscores and hyphens.

#### Viewing data:
```
>> r1
<content or r1>
```

### Constraints
```
<set> (contains | exclude) <string> [(or | and) <other constraint>...]
```
Apply constraints to the *set* and return the resulting *set*. The will remove any line that doesn't contains (for
`contains`) or does contain (for `exclude`) the specified word sequence as *string*.

## Examples
```
r1 = get http://localhost/idule.txt contains toto and exclude titi or contains blabla
```
This will fetch lines from `http://localhost/idule.txt`, remove ones that doesn't contain `toto` and contains `titi`,
remove ones that doesn't contain `blabla` and then store the result in `r1`.

*Other examples can be found in the [Queries](queries.txt) file.*
