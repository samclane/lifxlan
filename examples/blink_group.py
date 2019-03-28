#!/usr/bin/env python
# coding=utf-8
import sys
from time import sleep

from lifxlan import BLUE, GREEN, LifxLAN, Group


def main():
    num_lights = None
    if len(sys.argv) != 2:
        print("\nDiscovery will go much faster if you provide the number of lights on your LAN:")
        print("  python {} <number of lights on LAN>\n".format(sys.argv[0]))
    else:
        num_lights = int(sys.argv[1])

    # instantiate LifxLAN client, num_lights may be None (unknown).
    # In fact, you don't need to provide LifxLAN with the number of bulbs at all.
    # lifx = LifxLAN() works just as well. Knowing the number of bulbs in advance
    # simply makes initial bulb discovery faster.
    lifx = LifxLAN(num_lights)

    # test power control
    print("Discovering lights...")
    original_powers = lifx.get_power_all_lights()

    print("Building group...")
    g = Group([*original_powers])

    print("Turning lights on...")
    g.set_power("on")

    print("Toggling power of all lights...")
    toggle_all_lights_power(g, 0.2)

    print("Restoring power to all lights...")
    for light in original_powers:
        light.set_power(original_powers[light])

    # test color control
    original_colors = lifx.get_color_all_lights()

    print("Turning lights on...")
    lifx.set_power_all_lights("on")

    print("Toggling color of all lights quickly...")
    toggle_all_lights_color(g, 0.2)

    print("Toggling color of all lights slowly...")
    toggle_all_lights_color(g, 0.5)

    print("Restoring original color to all lights...")
    for light in original_colors:
        light.set_color(original_colors[light])

    sleep(0.2)

    print("Restoring original power to all lights...")
    for light in original_powers:
        light.set_power(original_powers[light])


def toggle_all_lights_power(group, interval=0.5, num_cycles=3):
    rapid = True if interval < 1 else False
    for i in range(num_cycles):
        group.set_power("on", rapid=rapid)
        sleep(interval)
        group.set_power("off", rapid=rapid)
        sleep(interval)


def toggle_all_lights_color(group, interval=0.5, num_cycles=3):
    rapid = True if interval < 1 else False
    for i in range(num_cycles):
        group.set_color(BLUE, rapid=rapid)
        sleep(interval)
        group.set_color(GREEN, rapid=rapid)
        sleep(interval)


if __name__ == "__main__":
    main()
