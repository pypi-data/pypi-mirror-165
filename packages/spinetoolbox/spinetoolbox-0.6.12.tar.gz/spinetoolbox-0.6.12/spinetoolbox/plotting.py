######################################################################################################################
# Copyright (C) 2017-2021 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Functions for plotting on PlotWidget.

Currently plotting from the table views found in the SpineDBEditor are supported.

The main entrance points to plotting are:
- plot_selection() which plots selected cells on a table view returning a PlotWidget object
- plot_pivot_column() which is a specialized method for plotting entire columns of a pivot table
- add_time_series_plot() which adds a time series plot to an existing PlotWidget
- add_map_plot() which adds a map plot to an existing PlotWidget

:author: A. Soininen (VTT)
:date:   9.7.2019
"""

import functools
from numbers import Number
from matplotlib.ticker import MaxNLocator
import numpy as np
from PySide2.QtCore import Qt, QModelIndex
from spinedb_api import (
    Array,
    convert_leaf_maps_to_specialized_containers,
    IndexedValue,
    Map,
    ParameterValueFormatError,
    TimeSeries,
)
from .helpers import first_non_null
from .mvcmodels.shared import PARSED_ROLE
from .widgets.plot_widget import PlotWidget


_PLOT_SETTINGS = {"alpha": 0.7}


class PlottingError(Exception):
    """An exception signalling failure in plotting."""

    def __init__(self, message):
        """
        Args:
            message (str): an error message
        """
        super().__init__()
        self._message = message

    @property
    def message(self):
        """str: the error message."""
        return self._message


def plot_pivot_column(proxy_model, column, hints, plot_widget=None):
    """
    Returns a plot widget with a plot of an entire column in PivotTableModel.

    Args:
        proxy_model (PivotTableSortFilterProxy): a pivot table filter
        column (int): a column index to the model
        hints (PlottingHints): a helper needed for e.g. plot labels
        plot_widget (PlotWidget): an existing plot widget to draw into or None to create a new widget
    Returns:
        PlotWidget: a plot widget
    """
    if plot_widget is None:
        plot_widget = PlotWidget()
        needs_redraw = False
    else:
        needs_redraw = True
    first_data_row = proxy_model.sourceModel().headerRowCount()
    values, labels = _collect_column_values(proxy_model, column, range(first_data_row, proxy_model.rowCount()), hints)
    if values:
        if plot_widget.plot_type is None:
            plot_widget.infer_plot_type(values)
        else:
            _raise_if_value_types_clash(values, plot_widget)
    add_plot_to_widget(values, labels, plot_widget)
    if len(plot_widget.canvas.axes.get_lines()) > 1:
        plot_widget.add_legend()
    plot_widget.canvas.axes.set_xlabel(hints.x_label(proxy_model))
    plot_lines = plot_widget.canvas.axes.get_lines()
    if plot_lines:
        plot_widget.canvas.axes.set_title(plot_lines[0].get_label())
    if needs_redraw:
        plot_widget.canvas.draw()
    return plot_widget


def plot_selection(model, indexes, hints, plot_widget=None):
    """
    Returns a plot widget with plots of the selected indexes.

    Args:
        model (QAbstractTableModel): a model
        indexes (Iterable): a list of QModelIndex objects for plotting
        hints (PlottingHints): a helper needed for e.g. plot labels
        plot_widget (PlotWidget): an existing plot widget to draw into or None to create a new widget
    Returns:
        a PlotWidget object
    """
    if plot_widget is None:
        plot_widget = PlotWidget()
        needs_redraw = False
    else:
        needs_redraw = True
    selections = hints.filter_columns(_organize_selection_to_columns(indexes), model)
    for column, rows in selections.items():
        values, labels = _collect_column_values(model, column, rows, hints)
        plot_widget.all_labels += labels
        if values:
            if plot_widget.plot_type is None:
                plot_widget.infer_plot_type(values)
            else:
                _raise_if_value_types_clash(values, plot_widget)
        add_plot_to_widget(values, labels, plot_widget)
    plot_widget.canvas.axes.set_xlabel(hints.x_label(model))
    if len(plot_widget.all_labels) > 1:
        plot_widget.canvas.axes.set_title("")
        plot_widget.add_legend()
    elif len(plot_widget.all_labels) == 1:
        plot_widget.canvas.axes.set_title(plot_widget.all_labels[0])
    if needs_redraw:
        plot_widget.canvas.draw()
    return plot_widget


def add_array_plot(plot_widget, value, label=None):
    """
    Adds an array plot to a plot widget.

    Args:
        plot_widget (PlotWidget): a plot widget to modify
        value (Array): the array to plot
        label (str): a label for the array
    """
    plot_widget.canvas.axes.plot(value.indexes, value.values, label=label, **_PLOT_SETTINGS)


def add_map_plot(plot_widget, map_value, label=None):
    """
    Adds a map plot to a plot widget.

    Args:
        plot_widget (PlotWidget): a plot widget to modify
        map_value (Map): the map to plot
        label (str): a label for the map
    """
    if not map_value.indexes:
        return
    if map_value.is_nested():
        raise PlottingError("Plotting of nested maps is not supported.")
    if not all(isinstance(value, float) for value in map_value.values):
        raise PlottingError("Cannot plot non-numerical values in map.")
    if not isinstance(map_value.indexes[0], str):
        indexes_as_strings = list(map(str, map_value.indexes))
    else:
        indexes_as_strings = map_value.indexes
    plot_widget.canvas.axes.plot(
        indexes_as_strings, map_value.values, label=label, linestyle="", marker="o", **_PLOT_SETTINGS
    )
    plot_widget.canvas.axes.xaxis.set_major_locator(MaxNLocator(10))


def add_time_series_plot(plot_widget, value, label=None):
    """
    Adds a time series step plot to a plot widget.

    Args:
        plot_widget (PlotWidget): a plot widget to modify
        value (TimeSeries): the time series to plot
        label (str): a label for the time series
    """
    plot_widget.canvas.axes.step(value.indexes, value.values, label=label, where='post', **_PLOT_SETTINGS)
    # matplotlib cannot have time stamps before 0001-01-01T00:00 on the x axis
    left, _ = plot_widget.canvas.axes.get_xlim()
    if left < 1.0:
        # 1.0 corresponds to 0001-01-01T00:00
        plot_widget.canvas.axes.set_xlim(left=1.0)
    # FIXME: The below causes xticklabels to disappear when plotting legend as a subplot
    # plot_widget.canvas.figure.autofmt_xdate()


class PlottingHints:
    """A base class for plotting hints.

    The functionality in this class allows the plotting functions to work
    without explicit knowledge of the underlying table model or widget.
    """

    def cell_label(self, model, index):
        """Returns a label for the cell given by index in a table."""
        raise NotImplementedError()

    def column_label(self, model, column):
        """Returns a label for a column."""
        raise NotImplementedError()

    def filter_columns(self, selections, model):
        """Filters columns and returns the filtered selections."""
        raise NotImplementedError()

    def is_index_in_data(self, model, index):
        """Returns true if the cell given by index is actually plottable data."""
        raise NotImplementedError()

    @staticmethod
    def normalize_row(row, model):
        """Returns a 'human understandable' row number"""
        return row + 1

    def special_x_values(self, model, column, rows):
        """Returns X values if available, otherwise returns None."""
        raise NotImplementedError()

    def x_label(self, model):
        """Returns a label for the x axis."""
        raise NotImplementedError()


class MapTablePlottingHints(PlottingHints):
    """Support for plotting data in Parameter table views."""

    def cell_label(self, model, index):
        """Returns a label build from the columns on the left from the data column."""
        return model.index_name(index)

    def column_label(self, model, column):
        """Returns the column header."""
        return model.headerData(column, orientation=Qt.Horizontal)

    def filter_columns(self, selections, model):
        """Returns the selections unaltered."""
        return selections

    def is_index_in_data(self, model, index):
        """Always returns True."""
        return True

    def special_x_values(self, model, column, rows):
        """Always returns None."""
        return None

    def x_label(self, model):
        """Returns an empty string for the x axis label."""
        return ""


class ParameterTablePlottingHints(PlottingHints):
    """Support for plotting data in Parameter table views."""

    def cell_label(self, model, index):
        """Returns a label build from the columns on the left from the data column."""
        return model.index_name(index)

    def column_label(self, model, column):
        """Returns the column header."""
        return model.headerData(column)

    def filter_columns(self, selections, model):
        """Returns the 'value' or 'default_value' column only."""
        columns = selections.keys()
        filtered = dict()
        for column in columns:
            header = model.headerData(column)
            if header in ("value", "default_value"):
                filtered[column] = selections[column]
        return filtered

    def is_index_in_data(self, model, index):
        """Always returns True."""
        return True

    def special_x_values(self, model, column, rows):
        """Always returns None."""
        return None

    def x_label(self, model):
        """Returns an empty string for the x axis label."""
        return ""


class PivotTablePlottingHints(PlottingHints):
    """Support for plotting data in Tabular view."""

    def cell_label(self, model, index):
        """Returns a label for the table cell given by index."""
        source_index = model.mapToSource(index)
        return model.sourceModel().index_name(source_index)

    def column_label(self, model, column):
        """Returns a label for a table column."""
        return model.sourceModel().column_name(column)

    def filter_columns(self, selections, model):
        """Filters the X column from selections."""
        x_column = model.sourceModel().plot_x_column
        if x_column is None or not model.filterAcceptsColumn(x_column, QModelIndex()):
            return selections
        proxy_x_column = self._map_column_from_source(model, x_column)
        return {column: rows for column, rows in selections.items() if column != proxy_x_column}

    def is_index_in_data(self, model, index):
        """Returns True if index is in the data portion of the table."""
        source_index = model.mapToSource(index)
        source_model = model.sourceModel()
        return source_model.index_in_data(source_index) or source_model.column_is_index_column(source_index.column())

    @staticmethod
    def normalize_row(row, model):
        """See base class."""
        source_row = model.mapToSource(model.index(row, 0)).row()
        return source_row + 1 - model.sourceModel().headerRowCount()

    def special_x_values(self, model, column, rows):
        """Returns the values from the X column if one is designated otherwise returns None."""
        x_column = model.sourceModel().plot_x_column
        if x_column is not None and model.filterAcceptsColumn(x_column, QModelIndex()):
            proxy_x_column = self._map_column_from_source(model, x_column)
            if column != proxy_x_column:
                collect = (
                    _collect_x_column_values
                    if not model.sourceModel().column_is_index_column(proxy_x_column)
                    else _collect_index_column_values
                )
                x_values = collect(model, proxy_x_column, rows, self)
                return x_values
        return None

    def x_label(self, model):
        """Returns the label of the X column, if available."""
        x_column = model.sourceModel().plot_x_column
        if x_column is None or not model.filterAcceptsColumn(x_column, QModelIndex()):
            return ""
        if model.sourceModel().column_is_index_column(x_column):
            return "Index"
        return self.column_label(model, self._map_column_from_source(model, x_column))

    @staticmethod
    def _map_column_to_source(proxy_model, proxy_column):
        """Maps a proxy model column to source model."""
        return proxy_model.mapToSource(proxy_model.index(0, proxy_column)).column()

    @staticmethod
    def _map_column_from_source(proxy_model, source_column):
        """Maps a source model column to proxy model."""
        source_index = proxy_model.sourceModel().index(0, source_column)
        return proxy_model.mapFromSource(source_index).column()


def add_plot_to_widget(values, labels, plot_widget):
    """Adds a new plot to plot_widget."""
    if not values:
        return
    if isinstance(values[0], TimeSeries):
        for value, label in zip(values, labels):
            add_time_series_plot(plot_widget, value, label)
    elif isinstance(values[0], Map):
        for value, label in zip(values, labels):
            add_map_plot(plot_widget, value, label)
    elif isinstance(values[0], Array):
        for value, label in zip(values, labels):
            add_array_plot(plot_widget, value, label)
    elif isinstance(values[1][0], Number):
        plot_widget.canvas.axes.plot(values[0], values[1], label=labels[0], **_PLOT_SETTINGS)
        if isinstance(values[0][0], str):
            # matplotlib tries to plot every single x tick label if they are strings.
            # This can become very slow if the labels are numerous.
            plot_widget.canvas.axes.xaxis.set_major_locator(MaxNLocator(10))
    else:
        raise PlottingError(f"Cannot plot: Don't know how to plot '{type(values[1][0]).__name__}' values.")


def _raise_if_not_all_indexed_values(values):
    """Raises an exception if not all values are TimeSeries or Maps."""
    if not values:
        return
    first_value_type = type(values[0])
    if issubclass(first_value_type, TimeSeries):
        # Clump fixed and variable step time series together. We can plot both at the same time.
        first_value_type = TimeSeries
    if not all(isinstance(value, first_value_type) for value in values[1:]):
        raise PlottingError("Cannot plot a mixture of indexed and other data")


def _filter_name_columns(selections):
    """Returns a dict with all but the entry with the greatest key removed."""
    # In case of Tree and Graph views the user may have selected non-data columns for plotting.
    # This function removes those from the selected columns.
    last_column = max(selections.keys())
    return {last_column: selections[last_column]}


def _organize_selection_to_columns(indexes):
    """Organizes a list of model indexes into a dictionary of {column: (rows)} entries."""
    selections = dict()
    for index in indexes:
        selections.setdefault(index.column(), set()).add(index.row())
    return {column: sorted(rows) for column, rows in selections.items()}


def _collect_single_column_values(model, column, rows, hints):
    """
    Collects selected parameter values from a single column.

    The return value of this function depends on what type of data the given column contains.
    In case of plain numbers, a list of scalars and a single label string are returned.
    In case of indexed parameters (time series, maps), a list of parameter_value objects is returned,
    accompanied by a list of labels, each label corresponding to one of the indexed parameters.

    Args:
        model (QAbstractTableModel): a table model
        column (int): a column index to the model
        rows (Sequence): row indexes to plot
        hints (PlottingHints): a plot support object

    Returns:
        tuple: values and label(s)
    """
    values = list()
    labels = list()
    for row in sorted(rows):
        data_index = model.index(row, column)
        if not hints.is_index_in_data(model, data_index):
            continue
        value = model.data(data_index, role=PARSED_ROLE)
        if isinstance(value, Exception):
            raise PlottingError(f"Failed to plot row {row}: {value}")
        if isinstance(value, (Array, Map, TimeSeries)):
            labels.append(hints.cell_label(model, data_index))
        elif value is not None and not isinstance(value, Number):
            raise PlottingError(f"Cannot plot row {row}: don't know how to plot a '{type(value).__name__}'.")
        values.append(value)
    if not values:
        return values, labels
    if isinstance(first_non_null(values), float):
        labels.append(hints.column_label(model, column))
    return values, labels


def _collect_x_column_values(model, column, rows, hints):
    """
    Collects selected parameter values from an x column.

    Args:
        model (QAbstractTableModel): a table model
        column (int): a column index to the model
        rows (Sequence): row indexes to plot
        hints (PlottingHints): a plot support object

    Returns:
        a tuple of values and label(s)
    """
    values = list()
    for row in sorted(rows):
        data_index = model.index(row, column)
        if not hints.is_index_in_data(model, data_index):
            continue
        value = model.data(data_index, role=PARSED_ROLE)
        if isinstance(value, Exception):
            raise PlottingError(f"Failed to plot '{value}'")
        if not isinstance(value, Number):
            raise PlottingError(f"Cannot plot X column value of type {type(value).__name__}.")
        values.append(value)
    if not values:
        return values
    return values


def _collect_index_column_values(model, column, rows, hints):
    """
    Collects selected values from an index column.

    Args:
        model (QAbstractTableModel): a table model
        column (int): a column index to the model
        rows (Sequence): row indexes to plot
        hints (PlottingHints): a plot support object

    Returns:
        list: column's values
    """
    values = list()
    for row in sorted(rows):
        data_index = model.index(row, column)
        if not hints.is_index_in_data(model, data_index):
            continue
        data_index = model.index(row, column)
        data = model.data(data_index, role=PARSED_ROLE)
        values.append(data)
    if not values:
        return values
    return values


def _collect_column_values(model, column, rows, hints):
    """
    Collects selected parameter values from a single column for plotting.

    The return value of this function depends on what type of data the given column contains.
    In case of plain numbers, a single tuple of two lists of x and y values
    and a single label string are returned.
    In case of time series, a list of TimeSeries objects is returned, accompanied
    by a list of labels, each label corresponding to one of the time series.

    Args:
        model (QAbstractTableModel): a table model
        column (int): a column index to the model
        rows (Sequence): row indexes to plot
        hints (PlottingHints): a support object

    Returns:
        tuple: a tuple of values and label(s)
    """
    values, labels = _collect_single_column_values(model, column, rows, hints)
    if not values:
        return values, labels
    if len(values) == len(labels):
        values, labels = expand_maps(values, labels)
    if isinstance(first_non_null(values), (Array, Map, TimeSeries)):
        values = [x for x in values if x is not None]
        _raise_if_not_all_indexed_values(values)
        _raise_if_indexed_values_not_plottable(values)
        return values, labels
    # Collect the y values as well
    x_values = hints.special_x_values(model, column, rows)
    if x_values is None:
        x_values = _x_values_from_rows(model, rows, hints)
    usable_x, usable_y = _filter_and_check(x_values, values)
    if not usable_x:
        return [], []
    return (usable_x, usable_y), labels


def expand_maps(maps, labels):
    """
    Gathers the leaf elements from ``maps`` and expands ``labels`` accordingly.

    Args:
        maps (list of Map): maps to expand
        labels (list of str): map labels

    Returns:
        tuple: expanded maps and labels
    """
    expanded_values = list()
    expanded_labels = list()
    for map_, label in zip(maps, labels):
        if map_ is None:
            continue
        if not isinstance(map_, Map):
            expanded_values.append(map_)
            expanded_labels.append(label)
            continue
        map_ = convert_leaf_maps_to_specialized_containers(map_)
        if isinstance(map_, (Array, TimeSeries)):
            expanded_values.append(map_)
            expanded_labels.append(label)
            continue
        nested_values, value_labels = _label_nested_maps(map_, label)
        expanded_values += nested_values
        expanded_labels += value_labels
    return expanded_values, expanded_labels


def _label_nested_maps(map_, label):
    """
    Collects leaf values from given Map and labels them.

    Args:
        map_ (Map): a map
        label (str): map's label

    Returns:
        tuple: list of values and list of corresponding labels
    """
    if map_ and not map_.is_nested():
        if isinstance(map_.values[0], (Array, TimeSeries)):
            labels = [label + " - " + str(index) for index in map_.indexes]
            values = list(map_.values)
            return values, labels
        return [map_], [label]
    values = list()
    labels = list()
    for index, value in zip(map_.indexes, map_.values):
        prefix_label = label + str(index)
        nested_values, nested_labels = _label_nested_maps(value, prefix_label)
        values += nested_values
        labels += nested_labels
    return values, labels


def _filter_and_check(xs, ys):
    """Filters Nones and empty values from x and y and checks that data types match."""
    x_type = type(first_non_null(xs))
    y_type = type(first_non_null(ys))
    filtered_xs = list()
    filtered_ys = list()
    for x, y in zip(xs, ys):
        if x is not None and y is not None:
            try:
                filtered_xs.append(x_type(x))
                filtered_ys.append(y_type(y))
            except (ParameterValueFormatError, TypeError, ValueError):
                # pylint: disable=raise-missing-from
                raise PlottingError("Cannot plot a mixture of different types of data")
    return filtered_xs, filtered_ys


def _raise_if_indexed_values_not_plottable(values):
    """Raises an exception if the indexed values in values contain elements that cannot be plotted."""
    for value in values:
        if isinstance(value.values, np.ndarray):
            if value.values.dtype.kind not in ("f", "M", "m", "i", "u"):
                raise PlottingError(f"Cannot plot values of type {value.values.dtype.name}.")
            continue
        if any(not isinstance(x, Number) for x in value.values):
            raise PlottingError(f"Cannot plot values of type {type(value.values[0]).__name__}.")


def _raise_if_value_types_clash(values, plot_widget):
    """Raises a PlottingError if values type is incompatible with plot_widget."""
    if isinstance(values[0], IndexedValue):
        if isinstance(values[0], TimeSeries) and not plot_widget.plot_type == TimeSeries:
            raise PlottingError("Cannot plot a mixture of time series and other value types.")
        if isinstance(values[0], Map) and not plot_widget.plot_type == Map:
            raise PlottingError("Cannot plot a mixture of maps and other value types.")
    elif not isinstance(values[1][0], plot_widget.plot_type):
        raise PlottingError("Cannot plot a mixture of indexed values and scalars.")


def _x_values_from_rows(model, rows, hints):
    """Returns x value array constructed from model rows."""
    normalize = functools.partial(hints.normalize_row, model=model)

    def row_to_index(row):
        return float(normalize(row))

    x_values = np.asarray(list(map(row_to_index, rows)))
    return x_values
