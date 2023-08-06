# Copyright © 2022, Donghua Chen
# All Rights Reserved
# Software Name: LightLogo
# By: Donghua Chen (https://github.com/dhchenx)
# License: BSD-3 - https://github.com/dhchenx/LightLogo/blob/main/LICENSE

#                         BSD 3-Clause License
#
# Copyright (c) 2022, Donghua Chen
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from lightlogo.world3D import *

'''
    LightLogo 3D Playground
'''

w3d = world3D(x_range=[-10, 10], y_range=[-10, 10], z_range=[-10, 10], title="Play 1", )

w3d.create()

turtle: turtle3D = turtle3D()


def create_a_turtle():
    global turtle
    w3d.create_turtles_random(N=1)
    turtle = w3d.turtle_at(len(w3d.turtles()) - 1)


create_a_turtle()

list_actions = []


def reset():
    global turtle, list_actions
    method = [turtle, "reset", []]
    list_actions.append(method)
    return method


def setxyz(x, y, z):
    global turtle, list_actions
    method = [turtle, "setxyz", [x, y, z]]
    list_actions.append(method)
    return method


def size(size):
    global turtle, list_actions
    method = [turtle, "size", [size]]
    list_actions.append(method)
    return method


def color(c):
    global turtle, list_actions
    method = [turtle, "color", [c]]
    list_actions.append(method)
    return method


def pendown():
    global turtle, list_actions
    list_actions.append([turtle, "pendown", []])
    return [turtle, "pendown", []]


def penup():
    global turtle, list_actions
    list_actions.append([turtle, "penup", []])
    return [turtle, "penup", []]


def forward(d):
    global turtle, list_actions
    list_actions.append([turtle, "fd", [d]])
    return [turtle, "fd", [d]]


def backward(d):
    global turtle, list_actions
    list_actions.append([turtle, "fd", [d]])
    return [turtle, "fd", [d]]


def fd(d):
    return forward(d)


def bk(d):
    return backward(d)


def left(a):
    global turtle, list_actions
    list_actions.append([turtle, "left", [a]])
    return [turtle, "left", [a]]


def lt(a):
    return left(a)


def rt(a):
    return right(a)


def right(a):
    global turtle, list_actions
    list_actions.append([turtle, "right", [a]])
    return [turtle, "right", [a]]


def shape(s):
    global turtle, list_actions
    list_actions.append([turtle, "shape", [s]])
    return [turtle, "shape", [s]]


def up(a):
    global turtle, list_actions
    list_actions.append([turtle, "up", [a]])
    return [turtle, "up", [a]]


def down(a):
    global turtle, list_actions
    list_actions.append([turtle, "down", [a]])
    return [turtle, "down", [a]]


def turtle_caller0(method):
    global turtle, list_actions
    list_actions.append([turtle, method, []])
    return [turtle, method, []]


def turtle_caller1(method, a):
    global turtle, list_actions
    list_actions.append([turtle, method, [a]])
    return [turtle, method, [a]]


def turtle_caller2(method, a, b):
    global turtle, list_actions
    list_actions.append([turtle, method, [a, b]])
    return [turtle, method, [a, b]]


def turtle_caller3(method, a, b, c):
    global turtle, list_actions
    list_actions.append([turtle, method, [a, b, c]])
    return [turtle, method, [a, b, c]]


var = lambda k: turtle_caller1("var", k)

setvar = lambda k, v: turtle_caller2("setvar", k, v)

move = lambda x, y, z: turtle_caller3("move", x, y, z)
moveto = lambda x, y, z: turtle_caller3("moveto", x, y, z)
setpos = lambda x, y, z: turtle_caller3("setpos", x, y, z)
setposition = lambda x, y, z: turtle_caller3("setposition", x, y, z)

distance = lambda x, y, z: turtle_caller3("distance", x, y, z)

type = lambda t: turtle_caller1("type", type)

begin_poly = lambda : turtle_caller0("begin_poly")

end_poly = lambda : turtle_caller0("end_poly")

setx = lambda x: turtle_caller1("setx", x)

sety = lambda y: turtle_caller1("sety", y)

setz = lambda z: turtle_caller1("setz", z)

setxrotate = lambda xt: turtle_caller1("setxrotate", xt)
setyrotate = lambda yt: turtle_caller1("setyrotate", yt)
setzrotate = lambda zt: turtle_caller1("setzrotate", zt)

rollback = lambda a: turtle_caller1("rollback", a)
rollforward = lambda a: turtle_caller1("rollforward", a)

xcor = lambda : turtle_caller0("xcor")
ycor = lambda : turtle_caller0("ycor")
zcor = lambda : turtle_caller0("zcor")

home = lambda : turtle_caller0("home")

die = lambda : turtle_caller0("die")
clear = lambda : turtle_caller0("clear")

width = lambda w: turtle_caller1("width", w)

pencolor = lambda c: turtle_caller1("pencolor", c)

showturtle = lambda : turtle_caller0("show")
hideturtle = lambda : turtle_caller0("hide")
st = lambda : turtle_caller0("show")
ht = lambda : turtle_caller0("hide")
goto = lambda x, y, z: turtle_caller3("goto", x, y, z)

fdx = lambda v: turtle_caller1("forwardx", v)
fdy = lambda v: turtle_caller1("forwardy", v)
fdz = lambda v: turtle_caller1("forwardz", v)

bkx = lambda v: turtle_caller1("backwardx", v)
bky = lambda v: turtle_caller1("backwardy", v)
bkz = lambda v: turtle_caller1("backwardz", v)

setheading = lambda a: turtle_caller1("setheading", a)

def clearscreen():
    global turtle
    w3d.clearscreen()
    create_a_turtle()
    w3d.update([turtle])


def play():
    global turtle, list_actions
    w3d.actions(list_actions)
    w3d.update([turtle])
    w3d.run(go=None, setup=None, interval=300, frames=len(list_actions))


def repeat_play():
    # clearscreen()
    global list_actions
    w3d.actions(list_actions)
    w3d.run(go=None, setup=None, interval=300, frames=len(list_actions), repeat=True)


def repeat(repeat_count, actions):
    global list_actions
    for num in range(repeat_count - 1):
        # print("actions:",actions)
        list_actions += actions


print("Welcome to LightLogo Playground!")
