__copyright__ = "Copyright 2019-2022 Mark Kim"
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__author__ = "Mark Kim"
__all__ = [ "TermRenderer", "TermWidgetRenderer", "TermWidgetRendered", "TermRendererException" ]

import os


##############################################################################
# EXPORTS

class TermRenderer:
    def __init__(self):
        self.widgetRenderers = {}
        self.setWidgetRenderer("nonetype", BlankWidgetRenderer(self))
        self.setWidgetRenderer("str", StrWidgetRenderer(self))
        self.setWidgetRenderer("int", IntWidgetRenderer(self))
        self.setWidgetRenderer("float", FloatWidgetRenderer(self))
        self.setWidgetRenderer("section", SectionWidgetRenderer(self))
        self.setWidgetRenderer("flexbox", FlexBoxWidgetRenderer(self))
        self.setWidgetRenderer("textbox", TextBoxWidgetRenderer(self))
        self.setWidgetRenderer("table", TableWidgetRenderer(self))
        self.setWidgetRenderer("hrule", HRuleWidgetRenderer(self))
        self.setWidgetRenderer("softbreak", ControlWidgetRenderer(self))
        self.setWidgetRenderer("hardbreak", ControlWidgetRenderer(self))

    def setWidgetRenderer(self, widgetType, termWidgetRenderer):
        self.widgetRenderers[widgetType] = termWidgetRenderer

        return self

    def getWidgetRenderer(self, widgetType):
        widgetRenderer = self.widgetRenderers.get(widgetType)

        return widgetRenderer

    def __call__(self, widget, minwidth=0, maxwidth=None, **kwargs):
        termWidget = TermWidget(widget)
        widgetType = termWidget.getType()
        renderer = self.getWidgetRenderer(widgetType)

        if not renderer:
            raise TermRendererException(f"No widget renderer for widgetType '{widgetType}'")

        if not maxwidth:
            maxwidth = Terminal.width()

        return renderer(widget, minwidth, maxwidth, **kwargs)


class TermWidgetRenderer:
    def __init__(self, termRenderer):
        self.termRenderer = termRenderer

    def __call__(self, widget, minwidth=0, maxwidth=None, **kwargs):
        return TermWidgetRendered()


class TermWidgetRendered:
    def __init__(self, lines=[], packchar=" "):
        self.lines = lines + []
        self.packchar = packchar

    def width(self):
        width = 0

        for l in self.lines:
            width = max(width, len(l))

        return width

    def height(self):
        return len(self.lines)

    def pack(self, minheight=0, minwidth=0, align="l"):
        width = max(self.width(), minwidth)
        dheight = minheight - self.height()

        self.lines += [""] * dheight

        return self.align(align, width, self.packchar)

    def left(self, width, padchar=" "):
        return self.align("l", width, padchar)

    def right(self, width, padchar=" "):
        return self.align("r", width, padchar)

    def center(self, width, padchar=" "):
        return self.align("c", width, padchar)

    def align(self, align, width, padchar=" "):
        lines = []

        for l in self.lines:
            slack = width - len(l)
            if   align == "l": lslack = 0              ; rslack = slack
            elif align == "r": lslack = slack          ; rslack = 0
            elif align == "c": lslack = int(slack / 2) ; rslack = int(slack / 2 + 0.5)
            else             : raise TermRendererException("Invalid alignment '{align}'")

            lines += [f"{padchar * lslack}{l}{padchar * rslack}"]

        self.lines = lines

        return self

    def appendBelow(self, other):
        self.lines += other.lines

        return self

    def appendRight(self, other):
        self.pack(max(self.height(), other.height()))

        for i,l in enumerate(other.lines):
            self.lines[i] += l

        return self

    def padBelow(self, numpads=1, padchar=" "):
        return self.appendBelow(TermWidgetRendered([""] * numpads))

    def padRight(self, numpads=1, padchar=" "):
        self.appendRight(TermWidgetRendered([" " * numpads]))
        self.pack()

        return self

    def __str__(self):
        return "\n".join(self.lines)


class TermRendererException(Exception):
    pass


##############################################################################
# WIDGET RENDERERS

class HRuleWidgetRenderer(TermWidgetRenderer):
    def __call__(self, widget, minwidth=0, maxwidth=None, **kwargs):
        return TermWidgetRendered([""], packchar="-")


class ControlWidgetRenderer(TermWidgetRenderer):
    def __call__(self, widget, minwidth=0, maxwidth=None, **kwargs):
        return TermWidgetRendered()


class BlankWidgetRenderer(TermWidgetRenderer):
    def __call__(self, widget, minwidth=0, maxwidth=None, **kwargs):
        return TermWidgetRendered()


class StrWidgetRenderer(TermWidgetRenderer):
    def __call__(self, string, minwidth=0, maxwidth=None, **kwargs):
        return TermWidgetRendered([string])


class IntWidgetRenderer(TermWidgetRenderer):
    def __call__(self, integer, minwidth=0, maxwidth=None, **kwargs):
        return TermWidgetRendered([str(integer)])


class FloatWidgetRenderer(TermWidgetRenderer):
    def __call__(self, float, minwidth=0, maxwidth=None, **kwargs):
        return TermWidgetRendered([str(float)])


class SectionWidgetRenderer(TermWidgetRenderer):
    def __call__(self, section, minwidth=0, maxwidth=None, **kwargs):
        # Render content
        kwargs["sectionDepth"] = kwargs.get("sectionDepth", 0) + 1
        renderedContent = self.termRenderer(section.contents[0], minwidth, maxwidth, **kwargs)
        kwargs["sectionDepth"] = kwargs.get("sectionDepth", 0) - 1

        # Render title
        renderedTitle = self.termRenderer(f" {section.title} ", 0, maxwidth, **kwargs)
        width = max(minwidth, renderedContent.width(), len(section.title)+6)
        if kwargs["sectionDepth"] == 0:
            renderedTitle.center(width, "=")
        else:
            renderedTitle.center(width, "-")

        return renderedTitle.appendBelow(renderedContent)


class FlexBoxWidgetRenderer(TermWidgetRenderer):
    def __call__(self, flexbox, minwidth=0, maxwidth=None, **kwargs):
        rflexbox = TermWidgetRendered()
        rrow = TermWidgetRendered()
        rcrow = []
        crow = []
        nrow = 0
        ncol = 0

        for c in flexbox.contents:
            rcell = self.termRenderer(c, minwidth, maxwidth, **kwargs)
            twidget = TermWidget(c)
            cellType = twidget.getType()
            breakType = None

            if cellType == "softbreak":
                breakType = "soft"
            elif cellType == "hardbreak":
                breakType = "hard"
            elif ncol and rrow.width() + flexbox.hpadding + rcell.width() > maxwidth:
                breakType = "soft"

            # Resize
            if breakType == "soft":
                widths = [rc.width() for rc in rcrow]
                slack = maxwidth - rrow.width()
                delta = slack / sum(widths)
                carry = 0
                ncol = 0
                rrow = TermWidgetRendered()

                for c2, cw in zip(crow, widths):
                    stretch = cw * delta + carry
                    carry = stretch - round(stretch)
                    cw += round(stretch)

                    if ncol:
                        rrow.padRight(flexbox.hpadding)

                    rrow.appendRight(self.termRenderer(c2, cw, maxwidth, **kwargs))
                    ncol += 1

            if breakType:
                if nrow:
                    rflexbox.padBelow(flexbox.vpadding)

                rflexbox.appendBelow(rrow)
                rrow = TermWidgetRendered()
                rcrow = []
                crow = []
                ncol = 0
                nrow += 1

            if twidget.isPrintable():
                if ncol:
                    rrow.padRight(flexbox.hpadding)

                rrow.appendRight(rcell)
                rcrow += [rcell]
                crow += [c]
                ncol += 1

        if nrow:
            rflexbox.padBelow(flexbox.vpadding)

        rflexbox.appendBelow(rrow)

        return rflexbox


class TextBoxWidgetRenderer(TermWidgetRenderer):
    def __call__(self, textbox, minwidth=0, maxwidth=None, **kwargs):
        rtextbox = TermWidgetRendered()

        for c in textbox.contents:
            rcell = self.termRenderer(c)

            rtextbox.appendBelow(rcell)

        return rtextbox


class TableWidgetRenderer(TermWidgetRenderer):
    def __call__(self, table, minwidth=0, maxwidth=None, **kwargs):
        numcols = table.numcols()
        numrows = table.numrows()
        heights = [0] * numrows
        widths = [0] * numcols
        matrix = []
        rtable = TermWidgetRendered()

        # Render
        for irow in range(numrows):
            matrix += [[]]

            for icol in range(numcols):
                cell = table.get(irow, icol)
                rcell = self.termRenderer(cell, minwidth, maxwidth, **kwargs)

                heights[irow] = max(heights[irow], rcell.height())
                widths[icol] = max(widths[icol], rcell.width())
                matrix[irow] += [rcell]

        # Pack
        for irow in range(numrows):
            for icol in range(numcols):
                matrix[irow][icol].pack(heights[irow], widths[icol], table.aligns[icol])

        # Merge
        for irow in range(numrows):
            rrow = TermWidgetRendered()

            for icol in range(numcols):
                if icol:
                    rrow.padRight(table.hpadding)

                rrow.appendRight(matrix[irow][icol])

            if irow:
                rtable.padBelow(table.vpadding)

            rtable.appendBelow(rrow)

        return rtable


##############################################################################
# UTILITIES

class TermWidget:
    CONTROL_WIDGET_TYPES = [
        "hrule",
        "softbreak",
        "hardbreak",
    ]

    def __init__(self, widget):
        self.widget = widget

    def getType(self):
        widget = self.widget
        wtype = type(widget).__name__.lower()

        if hasattr(widget, "type"):
            wtype = widget.type

        return wtype

    def isPrintable(self):
        wtype = self.getType()

        if wtype in TermWidget.CONTROL_WIDGET_TYPES:
            return False

        return True


class Terminal:
    DEFAULT_COLS = 120
    cachedCols = None

    @staticmethod
    def width():
        if Terminal.cachedCols is None:
            try:
                Terminal.cachedCols = int(os.popen('tput cols', 'r').read()) - 1
            except ValueError:
                Terminal.cachedCols = Terminal.DEFAULT_COLS

        return Terminal.cachedCols

