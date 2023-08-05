Graphviz utility functions.

*Latest release 20220827*:
* Remove dependency on cs.lex - now we need only the stdlib.
* New GVCAPTURE value for gvprint(file=) to return the binary image data as a bytes object; associated gvdata() convenience function.
* New GVDATAURL value for gvprint(file=) to return the binary image data as a data URL; associated gvdataurl() convenience function.

See also the [https://www.graphviz.org/documentation/](graphviz documentation)
and particularly the [https://graphviz.org/doc/info/lang.html](DOT language specification)
and the [https://www.graphviz.org/doc/info/command.html](`dot` command line tool).

## Class `DOTNodeMixin`

A mixin providing methods for things which can be drawn as
nodes in a DOT graph description.

*Method `DOTNodeMixin.dot_node(self, label=None, **node_attrs) -> str`*:
A DOT syntax node definition for `self`.

*Method `DOTNodeMixin.dot_node_attrs(self) -> Mapping[str, str]`*:
The default DOT node attributes.

*Method `DOTNodeMixin.dot_node_label(self) -> str`*:
The default node label.
This implementation returns `str(serlf)`
and a common implementation might return `self.name` or similar.

## Function `gvdata(dot_s, **kw)`

Convenience wrapper for `gvprint` which returns the binary image data.

## Function `gvdataurl(dot_s, **kw)`

Convenience wrapper for `gvprint` which returns the binary image data
as a `data:` URL.

## Function `gvprint(dot_s, file=None, fmt=None, layout=None, **dot_kw)`

Print the graph specified by `dot_s`, a graph in graphViz DOT syntax,
  to `file` (default `sys.stdout`)
  in format `fmt` using the engine specified by `layout` (default `'dot'`).

  If `fmt` is unspecified it defaults to `'png'` unless `file`
  is a terminal in which case it defaults to `'sixel'`.

  In addition to being a file or file descriptor,
  `file` may also take the following special values:
  * `GVCAPTURE`: causes `gvprint` to return the image data as `bytes`
  * `GVDATAURL`: causes `gvprint` to return the image data as a `data:` URL

  This uses the graphviz utility `dot` to draw graphs.
  If printing in SIXEL format the `img2sixel` utility is required,
  see [https://saitoha.github.io/libsixel/](libsixel).

  Example:

      data_url = gvprint('digraph FOO {A->B}', file=GVDATAURL, fmt='svg')

produces a `data:` URL rendering as:
<img src="data:image/svg+xml;utf8,<%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%20standalone%3D%22no%22%3F><%21DOCTYPE%20svg%20PUBLIC%20%22-//W3C//DTD%20SVG%201.1//EN%22%20%22http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd%22><%21--%20Generated%20by%20graphviz%20version%205.0.0%20%2820220707.1540%29%20--><%21--%20Title:%20FOO%20Pages:%201%20--><svg%20width%3D%2262pt%22%20height%3D%22116pt%22%20viewBox%3D%220.00%200.00%2062.00%20116.00%22%20xmlns%3D%22http://www.w3.org/2000/svg%22%20xmlns:xlink%3D%22http://www.w3.org/1999/xlink%22><g%20id%3D%22graph0%22%20class%3D%22graph%22%20transform%3D%22scale%281%201%29%20rotate%280%29%20translate%284%20112%29%22><title>FOO</title><polygon%20fill%3D%22white%22%20stroke%3D%22transparent%22%20points%3D%22-4%2C4%20-4%2C-112%2058%2C-112%2058%2C4%20-4%2C4%22/><%21--%20A%20--><g%20id%3D%22node1%22%20class%3D%22node%22><title>A</title><ellipse%20fill%3D%22none%22%20stroke%3D%22black%22%20cx%3D%2227%22%20cy%3D%22-90%22%20rx%3D%2227%22%20ry%3D%2218%22/><text%20text-anchor%3D%22middle%22%20x%3D%2227%22%20y%3D%22-86.3%22%20font-family%3D%22Times%2Cserif%22%20font-size%3D%2214.00%22>A</text></g><%21--%20B%20--><g%20id%3D%22node2%22%20class%3D%22node%22><title>B</title><ellipse%20fill%3D%22none%22%20stroke%3D%22black%22%20cx%3D%2227%22%20cy%3D%22-18%22%20rx%3D%2227%22%20ry%3D%2218%22/><text%20text-anchor%3D%22middle%22%20x%3D%2227%22%20y%3D%22-14.3%22%20font-family%3D%22Times%2Cserif%22%20font-size%3D%2214.00%22>B</text></g><%21--%20A%26%2345%3B%26gt%3BB%20--><g%20id%3D%22edge1%22%20class%3D%22edge%22><title>A%26%2345%3B%26gt%3BB</title><path%20fill%3D%22none%22%20stroke%3D%22black%22%20d%3D%22M27%2C-71.7C27%2C-63.98%2027%2C-54.71%2027%2C-46.11%22/><polygon%20fill%3D%22black%22%20stroke%3D%22black%22%20points%3D%2230.5%2C-46.1%2027%2C-36.1%2023.5%2C-46.1%2030.5%2C-46.1%22/></g></g></svg>">

## Function `quote(s)`

Quote a string for use in DOT syntax.
This implementation passes identifiers and sequences of decimal numerals
through unchanged and double quotes other strings.

# Release Log



*Release 20220827*:
* Remove dependency on cs.lex - now we need only the stdlib.
* New GVCAPTURE value for gvprint(file=) to return the binary image data as a bytes object; associated gvdata() convenience function.
* New GVDATAURL value for gvprint(file=) to return the binary image data as a data URL; associated gvdataurl() convenience function.

*Release 20220805.1*:
New DOTNodeMixin, a mixin for classes which can be rendered as a DOT node.

*Release 20220805*:
Initial PyPI release.
