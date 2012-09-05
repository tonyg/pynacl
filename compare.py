#!/usr/bin/python

import sys, json

def abbreviate_small_time(s, spacer="", suffix="s"):
    def _unit(text, unit):
        return text+spacer+unit+suffix
    if s > 1:
        return _unit("%d"%s, "")
    if s > 1e-3:
        return _unit("%0.2f" % (s*1e3), "m")
    if s > 1e-6:
        return _unit("%0.2f" % (s*1e6), "u")
    if s > 1e-9:
        return _unit("%0.2f" % (s*1e9), "n")
    return _unit("%g" % s, "")

def dump_html():
    portable = json.load(open(sys.argv[1]))
    optimized = json.load(open(sys.argv[2]))

    print "%-30s %10s%10s%10s" % ("", "portable", "optimized", "slowdown")
    for k in sorted(portable):
        slowdown = "%.1fx" % (portable[k] / optimized[k])
        print "%-30s:%10s%10s%10s" % (k,
                                      abbreviate_small_time(portable[k]),
                                      abbreviate_small_time(optimized[k]),
                                      slowdown)

    f = open("compare.html", "w")
    f.write("""<html><body>
    <style>
    table {border: 1px solid #CCC;}
    td,th {border: 1px solid #CCC;}
    td.name {text-align: left; }
    td.data {text-align: right; }
    th {padding-left: 10px; padding-right: 10px; }

    </style>
    <table cellspacing=0>
    <tr><th>name</th><th>ref</th><th>optimized</th><th>slowdown</th></tr>
    """)
    for k in sorted(portable):
        slowdown = portable[k] / optimized[k]
        f.write('<tr>')
        f.write('<td class="name">%s</td>' % k)
        f.write('<td class="data">%s</td>' % abbreviate_small_time(portable[k],
                                                                   spacer=" "))
        f.write('<td class="data">%s</td>' % abbreviate_small_time(optimized[k],
                                                                   spacer=" "))
        if slowdown < 2:
            color = "#AFA"
        elif slowdown < 4:
            color = "#FFA"
        else:
            color = "#FAA"
        f.write('<td class="data" style="background-color: %s">%.1fx</td>' %
                (color, slowdown))
        f.write('</tr>\n')
    f.write("""
    </table>
    </body>
    </html>
    """)
    f.close()

    f = open("compare2.html", "w")
    f.write("""<html><body>
    <style>
    th {padding-left: 10px; padding-right: 10px; }

    </style>
    <table cellspacing=0 style="border: 1px solid #CCC;">
    <tr><th style="padding-left: 10px; padding-right: 10px;">name</th><th style="padding-left: 10px; padding-right: 10px;">ref</th><th style="padding-left: 10px; padding-right: 10px;">optimized</th><th style="padding-left: 10px; padding-right: 10px;">slowdown</th></tr>
    """)
    for k in sorted(portable):
        slowdown = portable[k] / optimized[k]
        f.write('<tr>')
        f.write('<td style="border: 1px solid #CCC; text-align: left">%s</td>' % k)
        f.write('<td style="border: 1px solid #CCC; text-align: right">%s</td>' % abbreviate_small_time(portable[k],
                                                                   spacer=" "))
        f.write('<td style="border: 1px solid #CCC; text-align: right">%s</td>' % abbreviate_small_time(optimized[k],
                                                                   spacer=" "))
        if slowdown < 2:
            color = "#AFA"
        elif slowdown < 4:
            color = "#FFA"
        else:
            color = "#FAA"
        f.write('<td style="border: 1px solid #CCC; text-align: right; background-color: %s">%.1fx</td>' %
                (color, slowdown))
        f.write('</tr>\n')
    f.write("""
    </table>
    </body>
    </html>
    """)
    f.close()

if __name__ == '__main__':
    dump_html()
