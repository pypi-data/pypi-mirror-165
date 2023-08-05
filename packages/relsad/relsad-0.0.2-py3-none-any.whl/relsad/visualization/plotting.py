import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from relsad.network.components import (
    Bus,
    CircuitBreaker,
    Disconnector,
    EVPark,
    IntelligentSwitch,
    Line,
    Sensor,
)


def plot_topology(
    buses: list,
    lines: list,
    bus_text: bool = True,
    line_text: bool = False,
    circuitbreaker_text: bool = False,
    disconnector_text: bool = False,
    intelligent_switch_text: bool = False,
    sensor_text: bool = False,
    text_dx: tuple = (0, -0.1),
    **kwargs
):

    """
    Plots the system topology

    Parameters
    ----------
    buses : list
        List with Bus elements in the system
    lines : list
        List with Line elements in the system
    bus_text : bool
        Flag determining if bus name will be plotted
    line_text : bool
        Flag determining if line name will be plotted
    circuitbreaker_text : bool
        Flag determining if circuitbreaker name will be plotted
    disconnector_text : bool
        Flag determining if disconnector name will be plotted
    intelligent_switch_text : bool
        Flag determining if intelligent switch name will be plotted
    sensor_text : bool
        Flag determining if sensor name will be plotted
    **kwargs : dict
        Plotting keyword arguments.

    Returns
    ----------
    fig : figure
        Figure of the system topology
    None

    """
    # Handle keyword arguments

    left = kwargs["left"] if "left" in kwargs else 0.02
    right = kwargs["right"] if "right" in kwargs else 0.98
    bottom = kwargs["bottom"] if "bottom" in kwargs else 0.1
    top = kwargs["top"] if "top" in kwargs else 0.75

    text_size = kwargs["text_size"] if "text_size" in kwargs else 6

    ncol = kwargs["ncol"] if "ncol" in kwargs else None

    # Clear used keyword arguments
    kwargs.pop("left", None)
    kwargs.pop("right", None)
    kwargs.pop("bottom", None)
    kwargs.pop("top", None)
    kwargs.pop("text_size", None)
    kwargs.pop("ncol", None)

    fig, ax = plt.subplots(**kwargs)

    fig.subplots_adjust(
        left=left,
        bottom=bottom,
        right=right,
        top=top,
        wspace=None,
        hspace=None,
    )
    legends = {}
    for bus in buses:
        _plot_bus(
            ax=ax,
            bus=bus,
            text=bus_text,
            text_size=text_size,
            text_dx=text_dx,
        )
        legends["Bus"] = Bus.handle
        if bus.ev_park is not None:
            legends["EV park"] = EVPark.handle
    for line in lines:
        _plot_line(
            ax=ax,
            line=line,
            text=line_text,
            text_size=text_size,
        )
        legends["Line"] = Line.handle
        if line.circuitbreaker is not None:
            _plot_circuitbreaker(
                ax=ax,
                line=line,
                text=circuitbreaker_text,
                text_size=text_size,
            )
            legends["Circuit breaker"] = CircuitBreaker.handle
        for discon in line.disconnectors:
            _plot_disconnector(
                ax=ax,
                discon=discon,
                text=disconnector_text,
                text_size=text_size,
            )
            legends["Disconnector"] = Disconnector.handle
            if discon.intelligent_switch:
                _plot_intelligent_switch(
                    ax=ax,
                    discon=discon,
                    text=intelligent_switch_text,
                    text_size=text_size,
                )
                legends["Intelligent switch"] = IntelligentSwitch.handle
        if line.sensor:
            _plot_sensor(
                ax=ax,
                line=line,
                text=sensor_text,
                text_size=text_size,
            )
            legends["Sensor"] = Sensor.handle

    plt.figlegend(
        legends.values(),
        legends.keys(),
        ncol=ncol if ncol is not None else len(legends),
        loc="upper center",
        bbox_to_anchor=(left + (right - left) / 2, 0.978),
        frameon=False,
        prop={"size": 8},
        handleheight=3,
    )

    plt.axis("off")

    return fig


def _plot_line(
    ax: plt.axis,
    line: Line,
    text: bool = False,
    text_size: int = 8,
):
    """
    Plot lines

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot axis
    line : Line
        A Line element
    text : bool
        Flag determining if line name will be plotted
    text_size : int
        The size of the text in the plot

    Returns
    ----------
    None

    """
    dx_fraction = 0.1

    x1, y1 = line.fbus.coordinate
    x2, y2 = line.tbus.coordinate

    linestyle = ":" if line.is_backup else line.linestyle
    ax.plot(
        [x1, x2],
        [y1, y2],
        color=line.color,
        linestyle=linestyle,
        zorder=2,
    )
    if text:
        dx = x2 - x1
        dy = y2 - y1
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        if dx == 0 and dy != 0:
            x += dy * dx_fraction
        elif dx != 0 and dy == 0:
            y += dx * dx_fraction
        else:
            x += dx * dx_fraction
            y -= dy * dx_fraction
        ax.text(
            x,
            y,
            line.name,
            ha="center",
            va="center",
            size=text_size,
        )


def _plot_circuitbreaker(
    ax: plt.axis,
    line: Line,
    text: bool = False,
    text_size: int = 8,
):
    """
    Plot circuitbreakers

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot axis
    line : Line
        A Line element
    text : bool
        Flag determining if circuitbreaker name will be plotted
    text_size : int
        The size of the text in the plot

    Returns
    ----------
    None

    """
    cb = line.circuitbreaker
    x, y = cb.coordinate

    ax.plot(
        x,
        y,
        marker=cb.marker,
        markeredgewidth=cb.handle.get_markeredgewidth(),
        markersize=cb.size,
        linestyle="None",
        color=cb.color,
        markeredgecolor=cb.edgecolor,
        zorder=3,
    )
    if text:
        ax.text(
            x,
            y - 0.2,
            cb.name,
            ha="center",
            va="center",
            size=text_size,
        )


def _plot_disconnector(
    ax: plt.axis,
    discon: Disconnector,
    text: bool = False,
    text_size: int = 8,
):
    """
    Plot disconnectors

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot axis
    discon : Disconnecotr
        A Disconnector elements
    text : bool
        Flag determining if disconnector name will be plotted
    text_size : int
        The size of the text in the plot

    Returns
    ----------
    None

    """
    x, y = discon.coordinate
    ax.plot(
        x,
        y,
        marker=discon.marker,
        markeredgewidth=discon.handle.get_markeredgewidth(),
        markersize=discon.size,
        linestyle="None",
        color=discon.color,
        markeredgecolor=discon.edgecolor,
        zorder=3,
    )
    if text:
        ax.text(
            x,
            y - 0.2,
            discon.name,
            ha="center",
            va="center",
            size=text_size,
        )


def _plot_intelligent_switch(
    ax: plt.axis,
    discon: Disconnector,
    text: bool = False,
    text_size: int = 8,
):
    """
    Plot intelligent switches

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot axis
    discon : Disconnector
        A Disconnector elements
    text : bool
        Flag determining if intelligent switch name will be plotted
    text_size : int
        The size of the text on the plot

    Returns
    ----------
    None

    """
    x, y = discon.coordinate
    ax.plot(
        x,
        y,
        marker=discon.intelligent_switch.marker,
        markeredgewidth=discon.intelligent_switch.handle.get_markeredgewidth(),
        markersize=discon.intelligent_switch.size,
        linestyle="None",
        color=discon.intelligent_switch.color,
        zorder=3,
    )
    if text:
        ax.text(
            x,
            y - 0.2,
            discon.intelligent_switch.name,
            ha="center",
            va="center",
            size=text_size,
        )


def _plot_sensor(
    ax: plt.axis,
    line: Line,
    text: bool = False,
    text_size: int = 8,
):
    """
    Plot sensors

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot axis
    line : Line
        A Line element
    text : bool
        Flag determining if sensor name will be plotted
    text_size : int
        The size of the text in the plot

    Returns
    ----------
    None

    """
    x1, y1 = line.fbus.coordinate
    x2, y2 = line.tbus.coordinate

    x = (x1 + x2) / 2
    y = (y1 + y2) / 2

    ax.plot(
        x,
        y,
        marker=line.sensor.marker,
        markeredgewidth=line.sensor.handle.get_markeredgewidth(),
        markersize=line.sensor.size,
        linestyle="None",
        color=line.sensor.color,
        zorder=3,
    )
    if text:
        ax.text(
            x,
            y + 0.2,
            line.sensor.name,
            ha="center",
            va="center",
            size=text_size,
        )


def _plot_bus(
    ax: plt.axis,
    bus: Bus,
    text: bool = False,
    text_size: int = 8,
    text_dx: tuple = (0, 0),
):
    """
    Plot circuitbreakers

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot axis
    bus : Bus
        Bus element
    text : bool
        Flag determining if bus name will be plotted
    text_size : int
        The size of the text in the plot
    text_dx : tuple
        The distance from the text to the center point

    Returns
    ----------
    None

    """
    x, y = bus.coordinate
    ax.plot(
        x,
        y,
        marker=bus.marker,
        markeredgewidth=bus.handle.get_markeredgewidth(),
        markersize=bus.size,
        linestyle="None",
        color=bus.color,
        clip_on=False,
        zorder=3,
    )
    if text:
        ax.text(
            x + text_dx[0],
            y + text_dx[1],
            bus.name,
            ha="center",
            va="center",
            size=text_size,
        )
    if bus.ev_park is not None:
        ax.plot(
            x,
            y,
            marker=bus.ev_park.marker,
            markeredgewidth=bus.ev_park.handle.get_markeredgewidth(),
            markersize=bus.ev_park.size,
            linestyle="None",
            color=bus.color,
            clip_on=False,
            zorder=3,
        )


def plot_history(
    comp_list: list,
    attribute: str,
    save_dir: str,
):
    """
    Plots the history

    Parameters
    ----------
    comp_list : list
        List of components
    attribute : str
        An attribute
    save_dir : str
        The saving directory

    Returns
    ----------
    None

    """
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(1, 1, 1)
    for comp in comp_list:
        data = comp.get_history(attribute)
        ax.plot(list(data.values()), label=comp.name)
    ax.set_title(attribute)
    ax.legend()
    fig.savefig(os.path.join(save_dir, attribute + ".pdf"), format="pdf")
    plt.close(fig)


def plot_monte_carlo_history(
    comp_list: list,
    attribute: str,
    save_dir: str,
):
    """
    Plots the history from the Monte Carlo simulation

    Parameters
    ----------
    comp_list : list
        List of components
    attribute : str
        An attribute
    save_dir : str
        The saving directory

    Returns
    ----------
    None


    """
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(1, 1, 1)
    for comp in comp_list:
        data = comp.get_monte_carlo_history(attribute)
        ax.plot(list(data.values()), label=comp.name)
    ax.set_title(attribute)
    ax.legend()
    fig.savefig(os.path.join(save_dir, attribute + ".pdf"), format="pdf")
    plt.close(fig)


def plot_history_last_state(
    comp_list: list,
    attribute: str,
    save_dir: str,
):
    """
    Plots the last state from the history

    Parameters
    ----------
    comp_list : list
        List of components
    attribute : str
        An attribute
    save_dir : str
        The saving directory

    Returns
    ----------
    None


    """
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(1, 1, 1)
    df = pd.DataFrame()
    for comp in comp_list:
        data = comp.get_history(attribute)
        df[comp] = data.values()
    df.iloc[-1].plot.bar()
    ax.set_title(attribute)
    ax.legend()
    fig.savefig(os.path.join(save_dir, attribute + ".pdf"), format="pdf")
    plt.close(fig)


if __name__ == "__main__":
    pass
