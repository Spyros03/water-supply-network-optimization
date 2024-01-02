import math

g = 9.81
m_water = 1e-3
v_water = 1.1e-6
r_water = 1000


def darcy_weisbach(v, r, f):
    return (f * v ** 2) / (4 * r * 2 * g)


def colebrook_white(re, d, ks=0.001):
    new_f = 0.02
    count = 0
    current_f = new_f
    new_f = 1 / (-2 * math.log10(((ks / d) / 3.71 + 2.51 / (re * math.sqrt(current_f)))))**2
    while (count < 5 or abs(current_f - new_f) > 1e-6) and count < 100:
        count += 1
        current_f = new_f
        new_f = 1 / (-2 * math.log10(((ks / d) / 3.71 + 2.51 / (re * math.sqrt(current_f)))))**2
    return new_f


def energy_slope(v, d, ks=0.001):
    return darcy_weisbach(v, d/4, colebrook_white(reynolds_number(v, d), d, ks))


def head_loss(q, d, l, ks=0.001):
    v = velocity(q, d)
    return l*energy_slope(v, d, ks)


def discharge(hf, d, l, ks=0.001):
    ref = math.sqrt(2*g*hf/l)*d**1.5/v_water
    f = 1/(-2*math.log10(((ks/d)/3.71)+2.51/ref))**2
    v = math.sqrt(2*g*hf*d/(l*f))
    return v*math.pi*d**2/4


def diameter(q, hf, l, ks=0.001):
    new_f = 0.02
    count = 0
    current_f = new_f
    d = (current_f*8*l*q**2/(hf*math.pi**2*g))**0.2
    re = reynolds_number(velocity(q, d), d)
    new_f = 1/(-2*math.log10(((ks/d)/3.71 + 2.51/(re*math.sqrt(current_f)))))**2
    count += 1
    while (count < 5 or abs(current_f - new_f) > 1e-6) and count < 100:
        current_f = new_f
        d = (current_f * 8 * l * q ** 2 / (hf * math.pi ** 2 * g)) ** 0.2
        re = reynolds_number(velocity(q, d), d)
        new_f = 1 / (-2 * math.log10(((ks / d) / 3.71 + 2.51 / (re * math.sqrt(current_f)))))**2
        count += 1
    return d


def local_energy_losses(v1, v2, k):
    if v1 > v2:
        return k*v1**2/(2*g)
    else:
        return k*v2**2/(2*g)


def k_coefficient(d1, d2):
    if d1 == d2:
        return 0
    elif d2 > d1:
        return (1-(d1/d2)**2)**2
    else:
        ratio = d2/d1
        if ratio < 0.76:
            return 0.42*(1-(d2/d1)**2)
        else:
            return k_coefficient(d2, d1)


def velocity(q, d):
    return q*4/(math.pi*d**2)


def reynolds_number(v, d, vis=v_water):
    return v*d/vis