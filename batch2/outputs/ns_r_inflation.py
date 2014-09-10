# Uses first-order slow-roll results, with naive N definition, as in inflation paper

import planckStyle as s
from pylab import *
import numpy as np

g = s.getSinglePlotter()

g.make_figure(1, xstretch=1)

roots = ['base_nnu_meffsterile_r_' + s.defdata_all + '_lensing', 'base_r_' + s.defdata_all, g.getRoot('r', s.defdata_all + '_lensing_BAO_HST70p6_JLA')]



def N_r_ns(r, ns):
    return (r - 16) / (8. * ns - 8 + r) / 2.

def r_ns(ns, p):
    return  8.*(1 - ns) * p / (2. + p)

def r_ns_2(ns, p):
    return -4. / 3 * (32 * ns - 12 * ns * p - 28 - 6 * p - 3 * p ** 2 + 3 * p ** 2 * ns ** 2 + 18 * p * ns ** 2 - 4 * ns ** 2) * p / ((2. + p) ** 3)

def ns_N(N, p):  # first order
    return (4 * N - p - 4) / (4.*N + p)

def ns_N_2(N, p):  # solved used above expresion for r_ns, but naive expression for N
    return 0.5 * (-12 * p ** 2 + 96 * N + 80 * N * p + 12 * N * p ** 3 + 32 * p + 96 * N * p ** 2 - 2 * sqrt(384.*p - 1008 * p ** 2 - 2304 * p ** 3 + 384 * N * p + 4608 * N * p ** 2 + 6912 * N * p ** 3 + 3936 * p ** 4 * N + 936 * p ** 5 * N + 2304 * N ** 2 + 4608 * N ** 2 * p + 3456 * N ** 2 * p ** 2 + 1152 * N ** 2 * p ** 3 + 144 * N ** 2 * p ** 4 - 1464 * p ** 4 - 360 * p ** 5 + 72 * N * p ** 6 - 27 * p ** 6)) / (6.*N * p ** 3 + 36 * N * p ** 2 - 8 * N * p - 3 * p ** 3 - 18 * p ** 2 + 4 * p)
#    return (-12.*p ** 2 + 96 * N + 80 * N * p + 12 * N * p ** 3 + 32 * p + 96 * N * p ** 2 + 2 * sqrt(384. * p - 1008 * p ** 2 - 2304 * p ** 3 + 384 * N * p + 4608 * N * p ** 2 + 6912 * N * p ** 3 + 3936 * p ** 4 * N + 936 * p ** 5 * N + 2304 * N ** 2 + 4608 * N ** 2 * p + 3456 * N ** 2 * p ** 2 + 1152 * N ** 2 * p ** 3 + 144 * N ** 2 * p ** 4 - 1464 * p ** 4 - 360 * p ** 5 + 72 * N * p ** 6 - 27 * p ** 6)) / (6. * N * p ** 3 + 36 * N * p ** 2 - 8 * N * p - 3 * p ** 3 - 18 * p ** 2 + 4 * p)

g.plot_2d(roots, ['ns', 'r02'], filled=True)

ns = np.arange(0.93, 0.999, 0.0005)
r = np.arange(0, 0.34, 0.002)
ns, r = np.meshgrid(ns, r)

# this is the first order result
N = N_r_ns(r, ns)
N[r > 8 * (1 - ns) ] = 100

CS = contour(ns, r, N, origin='lower', levels=[50, 60], colors='k', linestyles=':', linewidths=0.3, extent=[0.95, 1.01, 0, 0.25])
# fmt = {}
# strs = [ 'N=50', 'N=60']
# for l, lab in zip(CS.levels, strs):
#    fmt[l] = lab

# clabel(CS, CS.levels, inline=True, fmt={}, fontsize=7)
for x, y, lab in zip([0.954, 0.9575], [0.2, 0.222], ['N=50', 'N=60']):
    plt.text(x, y, lab, size=7, rotation=-55, color='k',
         ha="center", va="center", bbox=dict(ec='1', fc='1', alpha=0))

ns = arange(0.93, 1.1, 0.001)  #
plot(ns, r_ns(ns, 1), ls='-', color='k', lw=1, alpha=0.8)

plt.text(0.954, 0.13, 'Convex', size=7, rotation=-22, color='k',
         ha="center", va="center")
plt.text(0.954, 0.116, 'Concave', size=7, rotation=-22, color='k',
         ha="center", va="center")

modcol = 'red'

text(0.962, 0.155, r'$\phi^2$', fontsize=9, color=modcol, bbox=dict(ec='1', fc='1', alpha=0.8), zorder=-2)

text(0.971, 0.081, r'$\phi$', fontsize=9, color=modcol)


for p in [1, 2]:
    ns = arange(0.93, 1.1, 0.002)  #

    if (p != 1): plot(ns, r_ns(ns, p), ls='-', color='black', lw=0.6, alpha=0.4)

#    print p, ns_N(50, p), ns_N(60, p)
    ns = arange(ns_N(50, p), ns_N(60, p), 0.0005)  #
    plot(ns, r_ns(ns, p), ls='-', color=modcol, lw=1.2, alpha=1)


# mnu = g.param_latex_label(roots[2], 'mnu', labelParams='params_CMB.paramnames')
nnu = g.param_latex_label(roots[0], 'nnu')
meff = g.param_latex_label(roots[0], 'meffsterile', labelParams='clik_latex.paramnames')

labels = [meff + '+' + nnu + '(' + s.lensing + ')', s.LCDM + '(' + s.planckall + ')', s.LCDM + '(' + s.planckall + '+ext)']
g.add_legend(labels, colored_text=True)

xlim([0.95, 1])
g.export()
