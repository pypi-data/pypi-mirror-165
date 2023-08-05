__copyright__ = "Copyright 2019-2022 Mark Kim"
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__author__ = "Mark Kim"

from .termrenderer import TermRenderer


##############################################################################
# BASE WIDGET

class Widget:
    def __init__(self, wtype=None):
        self.type = wtype

        if wtype is None:
            self.type = type(self).__name__.lower()

    def jsonable(self):
        jsonable = {
            "type" : self.type,
        }

        return jsonable


##############################################################################
# CONTROL WIDGETS

class ControlWidget(Widget): pass
class HRule(ControlWidget): pass
class SoftBreak(ControlWidget): pass
class HardBreak(ControlWidget): pass


##############################################################################
# PRINTABLE WIDGETS

class ContainerWidget(Widget):
    def __init__(self, *contents, **format):
        super().__init__()
        self.contents = list(contents)
        self.format = dict(format)

    def section(self, title, container):
        section = Section(title, container)

        return self.draw(section)

    def draw(self, container):
        self.write(container)

        return container

    def write(self, *contents):
        self.contents += list(contents)

        return self

    def jsonable(self):
        jsonable = super().jsonable()
        jsonable["contents"] = []

        def jsonify(c):
            if hasattr(c, "jsonable") : return c.jsonable()
            elif isinstance(c, list)  : return [jsonify(x) for x in c]
            else                      : return c

        for c in self.contents:
            jsonable["contents"] += [jsonify(c)]

        return jsonable

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


class Table(ContainerWidget):
    def __init__(self, aligns="", hpadding=1, vpadding=0):
        super().__init__()
        self.aligns = aligns
        self.hpadding = hpadding
        self.vpadding = vpadding

    def jsonable(self):
        jsonable = super().jsonable()
        jsonable["aligns"] = self.aligns
        jsonable["hpadding"] = self.hpadding
        jsonable["vpadding"] = self.vpadding

        return jsonable

    def get(self, irow, icol, default=None):
        cell = default

        if irow < len(self.contents):
            row = self.contents[irow]

            if icol < len(row):
                cell = row[icol]
            elif isinstance(row[0], HRule):
                cell = row[0]

        return cell

    def draw(self, container):
        # Ensure there is a row to append to
        if not self.contents:
            self.contents += [[]]

        # Ensure the last column doesn't go past the number of columns
        elif len(self.contents[-1]) >= self.numcols():
            # New row
            self.contents += [[]]

        # Append after the last column of last row 
        self.contents[-1] += [container]

        return container

    def write(self, *contents):
        ncols = len(contents)
        self.aligns += "l" * (ncols - len(self.aligns))
        self.contents += [list(contents)]

        return self

    def numrows(self):
        return len(self.contents)

    def numcols(self):
        return len(self.aligns)


class FlexBox(ContainerWidget):
    def __init__(self, hpadding=1, vpadding=1):
        super().__init__()
        self.hpadding = hpadding
        self.vpadding = vpadding

    def jsonable(self):
        jsonable = super().jsonable()
        jsonable["hpadding"] = self.hpadding
        jsonable["vpadding"] = self.vpadding

        return jsonable


class TextBox(ContainerWidget):
    def write(self, *args, **kwargs):
        for s in args:
            if isinstance(s, str):
                lines = s.split("\n")

                if not len(self.contents) or not isinstance(self.contents[-1], str):
                    self.contents += [""]

                self.contents[-1] += lines[0]
                self.contents += lines[1:]
            else:
                self.contents += [s]

        return self


class Section(ContainerWidget):
    def __init__(self, title, container):
        super().__init__()
        self.title = title
        self.contents += [container]

    def draw(self, *args, **kwargs):
        return self.contents[0].draw(*args, **kwargs)

    def write(self, *args, **kwargs):
        self.contents[0].write(*args, **kwargs)

        return self

    def jsonable(self):
        jsonable = super().jsonable()
        jsonable["title"] = self.title

        return jsonable


class Screen(Section):
    def __init__(self, title, renderer=None):
        self.column = Table("l", vpadding=1)
        self.textbox = TextBox()
        self.flexbox = FlexBox()
        self.renderer = renderer if renderer else TermRenderer()
        self.column.write(self.textbox)
        self.column.write(self.flexbox)

        super().__init__(title, self.column)
        self.type = "section"

    def write(self, *args, **kwargs):
        self.textbox.write(*args, **kwargs)

        return self

    def draw(self, container):
        self.flexbox.write(container)

        return container

    def __exit__(self, type, value, traceback):
        print(self.renderer(self))

