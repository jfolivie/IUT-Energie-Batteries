import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

#Simulation constants
F = 96500 # C/mol
RT = 2.5  # kJ/mol

#Simulation parameters
G1 = 0
G2 = 0

#Create time axes

x = np.linspace(0, 1, num = 10000) #axe du tracé

Dh_m = lambda x, G1, G2 : G1*x + G2*x*(1-x) #enthalpie de mélange : modèle réalistique
dDh_m = lambda x, G1, G2 : G1 + G2*(1-2*x) #dérivée par rapport à x de l'enthalpie de mélange

DGm_id = lambda x : RT * (x * np.log(x) + (1-x) * np.log(1-x)) #enthalpie libre de mélange idéale
dDGm_id = lambda x : RT* np.log(x/(1-x)) #dérivée de l'enthalpie libre idéale de mélange
DGm_re = lambda x, G1, G2 : Dh_m(x, G1, G2) + DGm_id(x) #prise en compte de l'écart à l'idealité

E_id = lambda x : -dDGm_id(x) / F 
E_re = lambda x, G1, G2 : -1/F * (dDGm_id(x) + dDh_m(x, G1, G2)) 

#Domaine d'instabilité
#d^2DG(x)/dx^2 > 0 
#Ce domaine existe à condition que G2 > 2 RT. A cette condition, il existe deux racines d'un polynôme du second degré tel que : 
# x^2 - x + 2RT/G2 = 0
# Le domiane définie par les deux solutions simples [x_m, x_p] constitue le domaine d'instabilité

def get_xeq(dDGm, G1) :
    cond = dDGm < 0
    inv_cond = np.invert(cond)
    return np.array([x[cond][0], x[inv_cond][-1]])

def tangent(xeq, G1, G2) : 
    Geq = DGm_re(xeq, G1, G2)
    slope = (Geq[1] - Geq[0]) / (xeq[1] - xeq[0])
    return  slope * xeq + Geq[0], - slope/F

def E_re_2(E, xeq, x, G1, G2) :
    E_re_2 = E_re(x, G1, G2)
    mask = (x > xeq[0]) & (x < xeq[1])
    E_re_2[mask] = E
    return E_re_2


def get_xm(RT, G2) : 
    return 1/2*(1-np.sqrt(1-2*RT/G2))

def get_xp(RT, G2) : 
    return 1/2*(1+np.sqrt(1-2*RT/G2))
    
fig = plt.figure(figsize = (10, 12))
ax1, ax2 = fig.subplots(2)

plt1_a, = ax1.plot(x, DGm_id(x), color = 'black', label = "idealite")
plt2_a, = ax1.plot(x, DGm_re(x, G1, G2), color = 'red', label = "realite")

plt1_b, = ax2.plot(x, E_id(x), color = 'black')
plt2_b, = ax2.plot(x, E_re(x, G1, G2), color = 'red')

plt1_c, = ax1.plot([0,], [0,], 'ro', color = 'red') 
plt2_c, = ax2.plot([0,], [0,], 'ro', color = 'red') 

plt1_d, = ax1.plot([0,], [0,], 'ro', color = 'blue') 
plt1_e, = ax1.plot([0,], [0,], ls = 'dashed', color = 'blue') 

plt2_e, = ax2.plot([0,], [0,], ls = 'dashed', color = 'blue') 

ax1.set_ylabel("$\Delta G_m$ [$kJ \cdot mol^{-1}$]")
ax2.set_ylabel("$E(x)$ [$V$]")
ax2.set_xlabel("$x$ dans $Li_{1-x}M$")

#ax.set_title("Modèle A -> B -> C avec $[A]_0 = 1 ~ mol.L^{-1}$")

fig.legend()

#Create graph axes for sliders
ax_k1 = plt.axes([0.25, 0.10, 0.65, 0.03])
ax_k2 = plt.axes([0.25, 0.05, 0.65, 0.03])

#Create sliders to define axes
slider_k1 = Slider(ax_k1, '$\gamma_1$', -10, 10, 0.2)
slider_k2 = Slider(ax_k2, '$\gamma_2$', -20, 20, 0.2)

fig.subplots_adjust(hspace=0)

#Create a function to be caalled whn slider vlaue is changed
def update(val) : 
    G1 = slider_k1.val
    G2 = slider_k2.val

    val_DGm_re = DGm_re(x, G1, G2)
    val_E_re = E_re(x, G1, G2)
    plt2_a.set_ydata(val_DGm_re)
    plt2_b.set_ydata(val_E_re)

    if G2 > 2 * RT :
        x_eq = get_xeq(val_E_re, G1)
        x_m = get_xp(RT, G2)
        x_p = get_xm(RT, G2)

        tg, E = tangent(x_eq, G1, G2)
        E_2 = E_re_2(E, x_eq, x, G1, G2)

        plt1_c.set_xdata([x_m,x_p]) 
        plt1_c.set_ydata([DGm_re(x_m, G1, G2), DGm_re(x_p, G1, G2)])
        
        plt1_d.set_xdata(x_eq) 
        plt1_d.set_ydata([DGm_re(x_eq[i], G1, G2) for i in range(len(x_eq))])
       
        plt1_e.set_xdata(x_eq)
        plt1_e.set_ydata(tg)

        plt2_e.set_xdata(x)
        plt2_e.set_ydata(E_2)

        plt2_c.set_xdata([x_m,x_p]) 
        plt2_c.set_ydata([E_re(x_m, G1, G2), E_re(x_p, G1, G2)])

#Udapte when slider value is changed
slider_k1.on_changed(update)
slider_k2.on_changed(update)

plt.show()
