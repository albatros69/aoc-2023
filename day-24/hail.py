#! /usr/bin/env python

from __future__ import annotations

from dataclasses import dataclass, astuple
import sys


@dataclass
class Pt3D:
    x: int
    y: int
    z: int

@dataclass
class Trajectory:
    start_pos: Pt3D
    velocity: Pt3D

    def __init__(self, pos, vit):
        self.start_pos = Pt3D(*pos)
        self.velocity = Pt3D(*vit)

    @property
    def slope(self) -> float:
        return self.velocity.y/self.velocity.x

    @property
    def b(self) -> float:
        return self.start_pos.y - self.slope*self.start_pos.x

    def intersect_p1(self, other: Trajectory):
        if self.slope == other.slope:
            return None
        else:
            x = (other.b - self.b)/(self.slope - other.slope)
            t1 = int((x - self.start_pos.x)/self.velocity.x)
            t2 = int((x - other.start_pos.x)/other.velocity.x)
            if t1 > 0 and t2 > 0:
                return (x, self.slope*x + self.b)
            else:
                return None


trajectories = []
for line in sys.stdin:
    p, v = line.strip().split(' @ ')
    trajectories.append(
        Trajectory(tuple(int(a) for a in p.split(', ')),
                   tuple(int(a) for a in v.split(', '))))

total = 0
# mini, maxi = 7, 27
mini, maxi = 200000000000000, 400000000000000
for i,t in enumerate(trajectories):
    for o in trajectories[i+1:]:
        inter = t.intersect_p1(o)
        if inter is not None:
            (x, y) = inter
            total += (mini <= x <= maxi) and (mini <= y <= maxi)
        # print(t.start_pos, o.start_pos, inter, total)

print("Part 1:", total)


from sympy import Symbol
from sympy import solve_poly_system

# See https://www.reddit.com/r/adventofcode/comments/18pnycy/2023_day_24_solutions/
# Everyone started using solver to get this done. Didn't have the time to dive into
# the doc of one of these so I copied/pasted some code that seemed clean.
# Not very proud of that...
# https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/kepmry2/

# Part 2 uses SymPy. We set up a system of equations that describes the intersections, and solve it.
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
vx = Symbol('vx')
vy = Symbol('vy')
vz = Symbol('vz')

equations = []
t_syms = []
#the secret sauce is that once you have three trajectories to intersect, there's only one valid line
#so we don't have to set up a huge system of equations that would take forever to solve. Just pick the first three.
for idx,traj in enumerate(trajectories[:3]):
    #vx is the velocity of our throw, xv is the velocity of the shard we're trying to hit. Yes, this is a confusing naming convention.
    x0,y0,z0, xv,yv,zv = *astuple(traj.start_pos), *astuple(traj.velocity)
    t = Symbol('t'+str(idx)) #remember that each intersection will have a different time, so it needs its own variable

    #(x + vx*t) is the x-coordinate of our throw, (x0 + xv*t) is the x-coordinate of the shard we're trying to hit.
    #set these equal, and subtract to get x + vx*t - x0 - xv*t = 0
    #similarly for y and z
    eqx = x + vx*t - x0 - xv*t
    eqy = y + vy*t - y0 - yv*t
    eqz = z + vz*t - z0 - zv*t

    equations.append(eqx)
    equations.append(eqy)
    equations.append(eqz)
    t_syms.append(t)

#To my great shame, I don't really know how this works under the hood.
result = solve_poly_system(equations,*([x,y,z,vx,vy,vz]+t_syms))
print("Part 2:", sum(result[0][:3]))
