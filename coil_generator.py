"""
Copyright (c) 2021 Alexander Dvorkovyy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Generate footprint file for a PCB coil shape in KiCAD 6 format.

IMPORTANT: coils are not connected, you have to connect them in series
in the footprint editor. Use PTH pads for that.

IMPORTANT2: Not tested with 4 and more layers

PCB shape parameters:
radius          -- coil outer radius in mm
layers          -- names of the layers where coil shapes have to be placed
turns           -- number of full coil turns on each layer
trace_width     -- width of the trace in mm 
trace_clearance -- distance between sibling turns in mm

Change the values of these parameters directly in the script and run it.
Capture the output into a footprint file stored in desired KiCAD6 footprint library.
"""

import sys
from math import tan, sin, cos, pi

radius = 4 # mm

# 2-Layer stackup
layers = ["F.Cu", "B.Cu"]

# 4-Layer stackup
# IMPORTANT: front layer has to be the first, back the last
#layers = ["F.Cu", "In1.Cu", "In2.Cu",  "B.Cu"]


# Number of turns on each layer
turns = 10

mils = 25.4 / 1000
trace_width = 6 * mils
trace_clearance = 6 * mils

trace_pitch = (trace_width + trace_clearance)

prec = 4 # decimal fraction digits

def coil_turn(radius: float, layer: str, direction: int) -> str:
    """Generate 1 complete coil turn"""
    if direction == 1:
        return ("(fp_arc "
            f"(start {-radius:.{prec}f} 0) "
            f"(mid 0 {-radius:.{prec}f}) "
            f"(end {radius:.{prec}f} 0) "
            f"(layer {layer}) (width {trace_width:.{prec}f}))\n"
        "(fp_arc "
            f"(start {radius:.{prec}f} 0) "
            f"(mid {-trace_pitch / 2:.{prec}f} {radius - trace_pitch / 2:.{prec}f}) "
            f"(end {-(radius - trace_pitch):.{prec}f} 0) "
            f"(layer {layer}) (width {trace_width:.{prec}f}))\n")
    else:
        return ("(fp_arc "
            f"(start {-(radius - trace_pitch):.{prec}f} 0) "
            f"(mid {trace_pitch / 2:.{prec}f} {-(radius - trace_pitch / 2):.{prec}f}) "
            f"(end {radius:.{prec}f} 0) "
            f"(layer {layer}) (width {trace_width:.{prec}f}))\n"
        "(fp_arc "
            f"(start {radius:.{prec}f} 0) "
            f"(mid 0 {radius:.{prec}f}) "
            f"(end {-radius:.{prec}f} 0) "
            f"(layer {layer}) (width {trace_width:.{prec}f}))\n")

def coil_layer(radius: float, layer: str, turns: int, direction: int) -> str:
    """Generate complete coil on 1 layer."""
    return ''.join([coil_turn(radius - n*trace_pitch, layer, direction) for n in range(turns)])

def coil_pad(radius: float, pad:str, layer: str) -> str:
    """Add 1mm coil pad on the outer side of the coil."""
    return (f"(pad \"{ pad }\" smd roundrect "
                f"(at {-(radius + 0.5 - trace_width / 2):.{prec}f} 0) "
                f"(size 1 {trace_width:.{prec}f}) "
                f"(layers {layer}) "
                "(roundrect_rratio 0.5))\n")

def keepout_area(radius: float) -> str:
    """Add keepout area where no copper or other metal should be placed.

    As of TI recommendation, it is 30% of the coil diameter. This should
    work for frequencies 1-30Mhz.
    """
    zone_radius = radius * 1.6
    polygon_sides = 40    
    side_halflength = zone_radius * tan(pi / polygon_sides)

    polygon = ""
    for n in range(polygon_sides):
        angle = n * 2 * pi / polygon_sides
        s = sin(angle)
        c = cos(angle)
        x = zone_radius * c - side_halflength * s
        y = zone_radius * s + side_halflength * c
        polygon += f"(xy {x:.{prec}f} {y:.{prec}f})\n"

    return (
        "(zone (net 0) (net_name \"\") (layers *.Cu) (name MagneticField) (hatch edge 0.508)\n"
        "  (connect_pads (clearance 0))\n"
        "  (min_thickness 0.254)\n"
        "  (keepout (tracks allowed) (vias allowed) (pads allowed ) (copperpour not_allowed) (footprints not_allowed))\n"
        "  (fill (thermal_gap 0.508) (thermal_bridge_width 0.508))\n"
        "  (polygon\n"
        "    (pts\n"
        f"{polygon}"
        "    )\n"
        "  )\n"
        ")\n"
        )

def footprint_name(radius: float, layers: list[str], turns: int) -> str:
    return ("pcb_coil_"
        f"{round(radius * 2)}mm"
        f"_{len(layers)}L"
        f"x{turns}T"
        f"_{round(trace_width / mils)}"
        f"-{round(trace_clearance / mils)}")

def header(radius: float, layers: list[str], turns: int) -> str:
    name = footprint_name(radius, layers, turns)
    descr = (f"PCB coil shape of {radius * 2}mm diameter "
        f"placed on {len(layers)} layers. "
        f"Traces of {round(trace_width / mils)} mils width "
        f"and {round(trace_clearance / mils)} mils clearance.")
    
    return(
f"""(footprint "{name}" (version 20211014) (generator pcbnew) (layer "F.Cu")
  (tedit 6185AD35)
  (descr "${descr}")
  (tags "pcb_coil")
  (attr through_hole exclude_from_bom)
  (fp_text reference "Ref**" (at 0 {-(radius + 1)} unlocked) (layer "F.SilkS")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value "{name}" (at 0 {radius + 1} unlocked) (layer "F.Fab")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  """
    )

def coil(radius: float, layers: list[str], turns: int) -> str:
    """Generate complete coil footprint"""
    result = header(radius, layers, turns)

    direction = 1
    for layer in layers:
        result += coil_layer(radius, layer, turns, direction)
        direction = -direction

    result += coil_pad(radius, "2", layers[0])
    result += coil_pad(radius, "1", layers[-1])
    result += keepout_area(radius)
    result += ")\n"
    return result

if __name__ == '__main__':
    # there has to be enough space inside of the coil to place the vias
    if radius - trace_pitch * turns < 0.2 * len(layers):
        print("Not enough space: try to reduce number of turns or increase the radius", file=sys.stderr)
        exit(1)

    coil_definition = coil(radius, layers, turns)
    print(coil_definition)