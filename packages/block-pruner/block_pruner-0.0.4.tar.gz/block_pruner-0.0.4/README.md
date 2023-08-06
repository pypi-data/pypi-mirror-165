# Block Pruner

How would you go about deleting blocks of `[start;end]` if the block contains `615` in _example.txt_ ?

_example.txt_

```txt
a
2
start
a
b
615 b
d
end
f
a
g
start
610
h
i
end
b
3
start
e
e
615
s
s
end
a
```

```
$ block_pruner --start start --end end --needle 615 example.txt
a
2
f
a
g
start
610
h
i
end
b
3
a
```

## Usage

```sh
block_pruner --start start --end end --needle 615 example.txt > out.txt
```

## Development

For help getting started developing check [DEVELOPMENT.md](DEVELOPMENT.md)
