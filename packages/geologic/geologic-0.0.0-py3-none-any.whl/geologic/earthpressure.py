import math
"""
Functions for calculation of earth pressure coefficients.
"""

def K_agh (alpha, beta, delta_a, phi):
    """Earth pressure coefficient for active earth pressure as a result of own weight. Inputs in degrees."""
    alpha = math.radians(alpha); beta = math.radians(beta); delta_a = math.radians(delta_a); phi = math.radians(phi)
    K_agh = (math.cos(phi - alpha)**2) / (math.cos(alpha)**2*(1+((math.sin(phi + delta_a)*math.sin(phi - beta))/(math.cos(alpha + delta_a) * math.cos(alpha - beta)))**0.5)**2)
    return K_agh


def theta_a (alpha, beta, delta_a, phi):
    """Fracutre angle theta_a. Inputs in degrees."""
    alpha = math.radians(alpha); beta = math.radians(beta); delta_a = math.radians(delta_a); phi = math.radians(phi)
    theta_a = phi + math.atan(math.cos(phi-alpha)/(math.sin(phi-alpha)+((math.sin(phi + delta_a)*math.cos(alpha - beta))/(math.sin(phi - beta)*math.cos(delta_a + alpha)))**0.5))
    return math.degrees(theta_a)


def K_aph (alpha, beta, delta_a, phi):
    """Earth pressure coefficient for active earth pressure as a result of external loads. Inputs in degrees."""
    a = K_agh(alpha, beta, delta_a, phi)
    alpha = math.radians(alpha); beta = math.radians(beta)
    K_aph = a * ((math.cos(alpha)*math.cos(beta))/(math.cos(alpha-beta)))
    return K_aph


def K_ach  (alpha, beta, delta_a, phi, mode="normal"):
    """Earth pressure coefficient for active earth pressure as a result of cohesion. Inputs in degrees. Mode is either 'normal' or 'simple'."""
    a = K_agh(alpha, beta, delta_a, phi)
    alpha = math.radians(alpha); beta = math.radians(beta); delta = math.radians(delta_a); phi = math.radians(phi)
    if mode == "simple":
        K_ach = a**0.5 * math.cos(delta_a) * (2)
    else:
        K_ach = (2 * math.cos(alpha-beta)*math.cos(phi)*math.cos(alpha+delta))/(math.cos(alpha)*(1+math.sin(phi+alpha+delta-beta)))
    return K_ach


def K_pgh(alpha, beta, delta_p, phi, mode="Pregl"):
    """Earth pressure coefficient for passive earth pressure as a result of own weights. Inputs in degrees. Mode is either 'Pregl' or 'Katzenbach'(not recommended.). For additional Info on Pregl see: https://link.springer.com/content/pdf/10.1007%2F978-3-658-14931-4_16.pdf """
    alpha = math.radians(alpha); beta = math.radians(beta); delta_p = math.radians(delta_p); phi = math.radians(phi)
    if mode=="Katzenbach":
        alpha = math.radians(alpha); beta = math.radians(beta); delta_p = math.radians(delta_p); phi = math.radians(phi)
        K_pgh = (math.cos(phi + alpha) ** 2) / (math.cos(alpha) ** 2 * (1 - ((math.sin(phi - delta_p) * math.sin(phi + beta))\
        / (math.cos(alpha + delta_p) * math.cos(alpha - beta))) ** 0.5) ** 2)
        return K_pgh
    elif mode=="Pregl":
        if phi > 0:
            if delta_p <= 0:
                i_pg = (1-0.53*delta_p)**(0.26+5.96*phi)
            else:
                i_pg = (1+0.41*delta_p)**(-7.13)
            if beta <= 0:
                g_pg = (1+0.73*beta)**2.89
            else:
                g_pg = (1+0.35*beta)**(0.42+8.15*phi)
            if alpha <= 0:
                t_pg = (1+0.72*alpha*math.tan(phi))**(-3.51+1.03*phi)
            else:
                t_pg = (1-0.0012*alpha*math.tan(phi))**(2910-1958*phi)
            K_pg0 = (1+math.sin(phi))/(1-math.sin(phi))
            K_pg = K_pg0 * i_pg * g_pg * t_pg
        elif phi == 0:
            K_pg = K_pp = 1
            K_pc = (2*(1+beta)*(1-alpha))/math.cos(alpha)
        K_pgh = K_pg * math.cos(delta_p+alpha)
        return K_pgh


def K_pph(alpha, beta, delta_p, phi):
    """Earth pressure coefficient for passive earth pressure as a result of external loads. Inputs in degrees. According to Pregl."""
    alpha = math.radians(alpha); beta = math.radians(beta); delta_p = math.radians(delta_p); phi = math.radians(phi)
    if phi > 0:
        if delta_p <= 0:
            i_pp = (1-1.33*delta_p)**(0.08+2.37*phi)
        else:
            i_pp = (1-0.72*delta_p)**2.81
        if beta <= 0:
            g_pp = (1+1.16*beta)**1.57
        else:
            g_pp = (1+3.84*beta)**(0.98*phi)
        if alpha <= 0:
            t_pp = (math.exp(-2*alpha*math.tan(phi)))/math.cos(alpha)
        else:
            t_pp = (math.exp(-2*alpha*math.tan(phi)))/math.cos(alpha)
        K_pp0 = (1+math.sin(phi))/(1-math.sin(phi))
        K_pp = K_pp0 * i_pp * g_pp * t_pp
    elif phi == 0:
        K_pp = 1
    K_pph = K_pp * math.cos(delta_p+alpha)
    return K_pph


def K_pch(alpha, beta, delta_p, phi):
    """Earth pressure coefficient for passive earth pressure as a result of cohesion. Inputs in degrees. According to Pregl."""
    alpha = math.radians(alpha); beta = math.radians(beta); delta_p = math.radians(delta_p); phi = math.radians(phi)
    if phi > 0:
        if delta_p <= 0:
            i_pc = (1-1.33*delta_p)**(0.08+2.37*phi)
        else:
            i_pc = (1+4.46*delta_p*math.tan(phi))**(-1.14+0.57*phi)
        if beta <= 0:
            g_pc = (1 + 0.001 * beta * math.tan(phi))**(205.4 + 2332 * phi)
        else:
            g_pc = math.exp(2*beta*math.tan(phi))
        if alpha <= 0:
            t_pc = (math.exp(-2*alpha*math.tan(phi)))/math.cos(alpha)
        else:
            t_pc = t_pp = (math.exp(-2*alpha*math.tan(phi)))/math.cos(alpha)
        K_pp0 = (1 + math.sin(phi)) / (1 - math.sin(phi))
        K_pc0 = (K_pp0-1)*(math.tan(phi)**(-1))
        K_pc = K_pc0 * i_pc * g_pc * t_pc
    elif phi == 0:
        K_pc = (2*(1+beta)*(1-alpha))/math.cos(alpha)
    K_pch = K_pc * math.cos(delta_p+alpha)
    return K_pch


def theta_p (alpha, beta, delta_p, phi):
    """Fraction angle theta_p. Inputs in degrees. According to Mueler Breslau."""
    alpha = math.radians(alpha); beta = math.radians(beta); delta_p = math.radians(delta_p); phi = math.radians(phi)
    theta_p = (-1)*(phi) + math.atan(((-1)*math.tan(alpha + phi)+math.cos(alpha+phi)**(-1)\
                                      *((math.sin(delta_p-phi)*math.cos(alpha-beta))\
                                        /((-1)*math.sin(phi+beta)*math.cos(delta_p+alpha)))**0.5)**(-1))
    theta_p = math.degrees(theta_p)
    return theta_p