Graphviz utility functions.

*Latest release 20220827.1*:
gvprint: new optional parameter dataurl_encoding to specify the data URL encoding.

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

## Function `gvprint(dot_s, file=None, fmt=None, layout=None, dataurl_encoding=None, **dot_kw)`

Print the graph specified by `dot_s`, a graph in graphViz DOT syntax,
  to `file` (default `sys.stdout`)
  in format `fmt` using the engine specified by `layout` (default `'dot'`).

  If `fmt` is unspecified it defaults to `'png'` unless `file`
  is a terminal in which case it defaults to `'sixel'`.

  In addition to being a file or file descriptor,
  `file` may also take the following special values:
  * `GVCAPTURE`: causes `gvprint` to return the image data as `bytes`
  * `GVDATAURL`: causes `gvprint` to return the image data as a `data:` URL

  For `GVDATAURL`, the parameter `dataurl_encoding` may be used
  to override the default encoding, which is `'utf8'` for `fmt`
  values `'dot'` and `'svg'`, otherwise `'base64'`.

  This uses the graphviz utility `dot` to draw graphs.
  If printing in SIXEL format the `img2sixel` utility is required,
  see [https://saitoha.github.io/libsixel/](libsixel).

  Example:

      data_url = gvprint('digraph FOO {A->B}', file=GVDATAURL, fmt='svg')

produces a `data:` URL rendering as:
<img src="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIKICJodHRwOi8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiPgo8IS0tIEdlbmVyYXRlZCBieSBncmFwaHZpeiB2ZXJzaW9uIDUuMC4wICgyMDIyMDcwNy4xNTQwKQogLS0+CjwhLS0gVGl0bGU6IEZPTyBQYWdlczogMSAtLT4KPHN2ZyB3aWR0aD0iNjJwdCIgaGVpZ2h0PSIxMTZwdCIKIHZpZXdCb3g9IjAuMDAgMC4wMCA2Mi4wMCAxMTYuMDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiPgo8ZyBpZD0iZ3JhcGgwIiBjbGFzcz0iZ3JhcGgiIHRyYW5zZm9ybT0ic2NhbGUoMSAxKSByb3RhdGUoMCkgdHJhbnNsYXRlKDQgMTEyKSI+Cjx0aXRsZT5GT088L3RpdGxlPgo8cG9seWdvbiBmaWxsPSJ3aGl0ZSIgc3Ryb2tlPSJ0cmFuc3BhcmVudCIgcG9pbnRzPSItNCw0IC00LC0xMTIgNTgsLTExMiA1OCw0IC00LDQiLz4KPCEtLSBBIC0tPgo8ZyBpZD0ibm9kZTEiIGNsYXNzPSJub2RlIj4KPHRpdGxlPkE8L3RpdGxlPgo8ZWxsaXBzZSBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBjeD0iMjciIGN5PSItOTAiIHJ4PSIyNyIgcnk9IjE4Ii8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJtaWRkbGUiIHg9IjI3IiB5PSItODYuMyIgZm9udC1mYW1pbHk9IlRpbWVzLHNlcmlmIiBmb250LXNpemU9IjE0LjAwIj5BPC90ZXh0Pgo8L2c+CjwhLS0gQiAtLT4KPGcgaWQ9Im5vZGUyIiBjbGFzcz0ibm9kZSI+Cjx0aXRsZT5CPC90aXRsZT4KPGVsbGlwc2UgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgY3g9IjI3IiBjeT0iLTE4IiByeD0iMjciIHJ5PSIxOCIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSIyNyIgeT0iLTE0LjMiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+QjwvdGV4dD4KPC9nPgo8IS0tIEEmIzQ1OyZndDtCIC0tPgo8ZyBpZD0iZWRnZTEiIGNsYXNzPSJlZGdlIj4KPHRpdGxlPkEmIzQ1OyZndDtCPC90aXRsZT4KPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgZD0iTTI3LC03MS43QzI3LC02My45OCAyNywtNTQuNzEgMjcsLTQ2LjExIi8+Cjxwb2x5Z29uIGZpbGw9ImJsYWNrIiBzdHJva2U9ImJsYWNrIiBwb2ludHM9IjMwLjUsLTQ2LjEgMjcsLTM2LjEgMjMuNSwtNDYuMSAzMC41LC00Ni4xIi8+CjwvZz4KPC9nPgo8L3N2Zz4K">

## Function `quote(s)`

Quote a string for use in DOT syntax.
This implementation passes identifiers and sequences of decimal numerals
through unchanged and double quotes other strings.

# Release Log



*Release 20220827.1*:
gvprint: new optional parameter dataurl_encoding to specify the data URL encoding.

*Release 20220827*:
* Remove dependency on cs.lex - now we need only the stdlib.
* New GVCAPTURE value for gvprint(file=) to return the binary image data as a bytes object; associated gvdata() convenience function.
* New GVDATAURL value for gvprint(file=) to return the binary image data as a data URL; associated gvdataurl() convenience function.

*Release 20220805.1*:
New DOTNodeMixin, a mixin for classes which can be rendered as a DOT node.

*Release 20220805*:
Initial PyPI release.
