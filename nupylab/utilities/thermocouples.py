"""Thermocouple Polynomial Equations.

TYPE tuples are coefficients for converting T in Celsius to millivolts.
INVERSE tuples are coefficients for converting millivolts to T in Celsius.
First two values in tuple indicate lower and upper limits of equation validity,
in Celsius for TYPE tuples and in millivolts for INVERSE tuples.
"""

from math import exp

TYPE_B = (
    (0.0,
     630.615,
     0.0,
     -0.00024650818346,
     5.9040421171e-06,
     -1.3257931636e-09,
     1.5668291901e-12,
     -1.694452924e-15,
     6.2990347094e-19),
    (630.615,
     1820.0,
     -3.8938168621,
     0.02857174747,
     -8.4885104785e-05,
     1.5785280164e-07,
     -1.6835344864e-10,
     1.1109794013e-13,
     -4.4515431033e-17,
     9.8975640821e-21,
     -9.3791330289e-25)
)

INVERSE_B = (
    (0.291,
     2.431,
     98.423321,
     699.715,
     -847.65304,
     1005.2644,
     -833.45952,
     455.08542,
     -155.23037,
     29.88675,
     -2.474286),
    (2.431,
     13.82,
     213.15071,
     285.10504,
     -52.742887,
     9.9160804,
     -1.2965303,
     0.1119587,
     -0.0060625199,
     0.00018661696,
     -2.4878585e-06)
)

TYPE_E = (
    (-270.0,
     0.0,
     0.0,
     0.058665508708,
     4.5410977124e-05,
     -7.7998048686e-07,
     -2.5800160843e-08,
     -5.9452583057e-10,
     -9.3214058667e-12,
     -1.0287605534e-13,
     -8.0370123621e-16,
     -4.3979497391e-18,
     -1.6414776355e-20,
     -3.9673619516e-23,
     -5.5827328721e-26,
     -3.4657842013e-29),
    (0.0,
     1000.0,
     0.0,
     0.05866550871,
     4.5032275582e-05,
     2.8908407212e-08,
     -3.3056896652e-10,
     6.502440327e-13,
     -1.9197495504e-16,
     -1.2536600497e-18,
     2.1489217569e-21,
     -1.4388041782e-24,
     3.5960899481e-28),
)

INVERSE_E = (
    (-8.825,
     0.0,
     0.0,
     16.977288,
     -0.4351497,
     -0.15859697,
     -0.092502871,
     -0.026084314,
     -0.0041360199,
     -0.0003403403,
     -1.156489e-05),
    (0.0,
     76.373,
     0.0,
     17.057035,
     -0.23301759,
     0.0065435585,
     -7.3562749e-05,
     -1.7896001e-06,
     8.4036165e-08,
     -1.3735879e-09,
     1.0629823e-11,
     -3.2447087e-14)
)

TYPE_J = (
    (-210.0,
     760.0,
     0.0,
     0.050381187815,
     3.047583693e-05,
     -8.568106572e-08,
     1.3228195295e-10,
     -1.7052958337e-13,
     2.0948090697e-16,
     -1.2538395336e-19,
     1.5631725697e-23),
    (760.0,
     1200.0,
     296.45625681,
     -1.4976127786,
     0.0031787103924,
     -3.1847686701e-06,
     1.5720819004e-09,
     -3.0691369056e-13)
)

INVERSE_J = (
    (-8.095,
     0.0,
     0.0,
     19.528268,
     -1.2286185,
     -1.0752178,
     -0.59086933,
     -0.17256713,
     -0.028131513,
     -0.002396337,
     -8.3823321e-05),
    (0.0,
     42.919,
     0.0,
     19.7843,
     -0.20012,
     0.0103697,
     -0.000254969,
     3.58515e-06,
     -5.34429e-08,
     5.09989e-10),
    (42.919,
     69.553,
     -3113.58187,
     300.543684,
     -9.9477323,
     0.17027663,
     -0.00143033468,
     4.73886084e-06)
)

TYPE_K = (  # Type K has additional exponential term from last 3 coefficients
    (-270.0,
     0.0,
     0.0,
     0.039450128025,
     2.3622373598e-05,
     -3.2858906784e-07,
     -4.9904828777e-09,
     -6.7509059173e-11,
     -5.7410327428e-13,
     -3.1088872894e-15,
     -1.0451609365e-17,
     -1.9889266878e-20,
     -1.6322697486e-23,
     0.0,
     0.0,
     0.0),
    (0.0,
     1372.0,
     -0.017600413686,
     0.038921204975,
     1.8558770032e-05,
     -9.9457592874e-08,
     3.1840945719e-10,
     -5.6072844889e-13,
     5.6075059059e-16,
     -3.2020720003e-19,
     9.7151147152e-23,
     -1.2104721275e-26,
     0.1185976,
     -0.0001183432,
     126.9686)
)

INVERSE_K = (
    (-5.89,
     0.0,
     0.0,
     25.173462,
     -1.1662878,
     -1.0833638,
     -0.8977354,
     -0.37342377,
     -0.086632643,
     -0.010450598,
     -0.00051920577),
    (0.0,
     20.64,
     0.0,
     25.08355,
     0.07860106,
     -0.2503131,
     0.0831527,
     -0.01228034,
     0.0009804036,
     -4.41303e-05,
     1.057734e-06,
     -1.052755e-08),
    (20.64,
     54.89,
     -131.8058,
     48.30222,
     -1.646031,
     0.05464731,
     -0.0009650715,
     8.802193e-06,
     -3.11081e-08)
)

TYPE_N = (
    (-270.0,
     0.0,
     0.0,
     0.026159105962,
     1.0957484228e-05,
     -9.3841111554e-08,
     -4.6412039759e-11,
     -2.6303357716e-12,
     -2.2653438003e-14,
     -7.6089300791e-17,
     -9.3419667835e-20),
    (0.0,
     1300.0,
     0.0,
     0.025929394601,
     1.571014188e-05,
     4.3825627237e-08,
     -2.5261169794e-10,
     6.4311819339e-13,
     -1.0063471519e-15,
     9.9745338992e-19,
     -6.0863245607e-22,
     2.0849229339e-25,
     -3.0682196151e-29)
)

INVERSE_N = (
    (-3.99,
     0.0,
     0.0,
     38.436847,
     1.1010485,
     5.2229312,
     7.2060525,
     5.8488586,
     2.7754916,
     0.77075166,
     0.11582665,
     0.0073138868),
    (0.0,
     20.613,
     0.0,
     38.6896,
     -1.08267,
     0.0470205,
     -2.12169e-06,
     -0.000117272,
     5.3928e-06,
     -7.98156e-08),
    (20.613,
     47.513,
     19.72485,
     33.00943,
     -0.3915159,
     0.009855391,
     -0.0001274371,
     7.767022e-07)
)

TYPE_R = (
    (-50.0,
     1064.18,
     0.0,
     0.00528961729765,
     1.39166589782e-05,
     -2.38855693017e-08,
     3.56916001063e-11,
     -4.62347666298e-14,
     5.00777441034e-17,
     -3.73105886191e-20,
     1.57716482367e-23,
     -2.81038625251e-27),
    (1064.18,
     1664.5,
     2.95157925316,
     -0.00252061251332,
     1.59564501865e-05,
     -7.64085947576e-09,
     2.05305291024e-12,
     -2.93359668173e-16),
    (1664.5,
     1768.1,
     152.232118209,
     -0.268819888545,
     0.000171280280471,
     -3.45895706453e-08,
     -9.34633971046e-15)
)

INVERSE_R = (
    (-0.226,
     1.923,
     0.0,
     188.9138,
     -93.83529,
     130.68619,
     -227.0358,
     351.45659,
     -389.539,
     282.39471,
     -126.07281,
     31.353611,
     -3.3187769),
    (1.923,
     13.228,
     13.34584505,
     147.2644573,
     -18.44024844,
     4.031129726,
     -0.624942836,
     0.06468412046,
     -0.004458750426,
     0.0001994710149,
     -5.31340179e-06,
     6.481976217e-08),
    (11.361,
     19.739,
     -81.99599416,
     155.3962042,
     -8.342197663,
     0.4279433549,
     -0.0119157791,
     0.0001492290091),
    (19.739,
     21.103,
     34061.77836,
     -7023.729171,
     558.2903813,
     -19.52394635,
     0.2560740231)
)

TYPE_S = (
    (-50.0,
     1064.18,
     0.0,
     0.00540313308631,
     1.2593428974e-05,
     -2.32477968689e-08,
     3.22028823036e-11,
     -3.31465196389e-14,
     2.55744251786e-17,
     -1.25068871393e-20,
     2.71443176145e-24),
    (1064.18,
     1664.5,
     1.32900444085,
     0.00334509311344,
     6.54805192818e-06,
     -1.64856259209e-09,
     1.29989605174-14),
    (1664.5,
     1768.1,
     146.628232636,
     -0.258430516752,
     0.000163693574641,
     -3.30439046987e-08,
     -9.43223690612e-15)
)

INVERSE_S = (
    (-0.235,
     1.874,
     0.0,
     184.94946,
     -80.0504062,
     102.23743,
     -152.248592,
     188.821343,
     -159.085941,
     82.302788,
     -23.4181944,
     2.7978626),
    (1.874,
     11.95,
     12.91507177,
     146.6298863,
     -15.34713402,
     3.145945973,
     -0.4163257839,
     0.03187963771,
     -0.0012916375,
     2.183475087e-05,
     -1.447379511e-07,
     8.211272125e-09),
    (10.332,
     17.536,
     -80.87801117,
     162.1573104,
     -8.536869453,
     0.4719686976,
     -0.01441693666,
     0.000208161889),
    (17.536,
     18.693,
     53338.75126,
     -12358.92298,
     1092.657613,
     -42.65693686,
     0.624720542)
)

TYPE_T = (
    (-270.0,
     0.0,
     0.0,
     0.038748106364,
     4.4194434347e-05,
     1.1844323105e-07,
     2.0032973554e-08,
     9.0138019559e-10,
     2.2651156593e-11,
     3.6071154205e-13,
     3.8493939883e-15,
     2.8213521925e-17,
     1.4251594779e-19,
     4.8768662286e-22,
     1.079553927e-24,
     1.3945027062e-27,
     7.9795153927e-31),
    (0.0,
     400.0,
     0.0,
     0.038748106364,
     3.329222788e-05,
     2.0618243404e-07,
     -2.1882256846e-09,
     1.0996880928e-11,
     -3.0815758772e-14,
     4.547913529e-17,
     -2.7512901673e-20)
)

INVERSE_T = (
    (-5.603,
     0.0,
     0.0,
     25.949192,
     -0.21316967,
     0.79018692,
     0.42527777,
     0.13304473,
     0.020241446,
     0.0012668171),
    (0.0,
     20.872,
     0.0,
     25.928,
     -0.7602961,
     0.04637791,
     -0.002165394,
     6.048144e-05,
     -7.293422e-07)
)


def calculate_temperature(
    millivoltage: float, TC_type: str, cold_junction_temp: float = 23
) -> float:
    """Calculate temperature with cold junction correction.

    Args:
        millivoltage: measured reading in millivolts.
        TC_type: thermocouple type.
        cold_junction_temp: cold junction temperature in Celsius.

    Returns:
        corrected thermocouple temperature in Celsius.

    Raises:
        ValueError if millivoltage or cold_junction_temp are outside applicable TC
        range.
    """
    cj_voltage = convert_to_voltage(cold_junction_temp, TC_type)
    return convert_to_temperature(millivoltage + cj_voltage, TC_type)


def calculate_voltage(
    temperature: float, TC_type: str, cold_junction_temp: float = 23
) -> float:
    """Calculate measured voltage with cold junction correction.

    Args:
        temperature: hot junction temperature in Celsius.
        TC_type: thermocouple type.
        cold_junction_temp: cold junction temperature in Celsius.

    Returns:
        measured voltage in millivolts.

    Raises:
        ValueError if temperature or cold_junction_temp are outside applicable TC
        range.
    """
    cj_voltage = convert_to_voltage(cold_junction_temp, TC_type)
    hj_voltage = convert_to_voltage(temperature, TC_type)
    return hj_voltage - cj_voltage


def convert_to_temperature(millivoltage: float, TC_type: str) -> float:
    """Convert voltage in millivolts to temperature in Celsius."""
    table = globals()[f"INVERSE_{TC_type.upper()}"]
    if millivoltage < table[0][0] or millivoltage > table[-1][1]:
        raise ValueError("voltage out of valid range for TC")
    for subset in table:
        if millivoltage >= subset[0] and millivoltage <= subset[1]:
            coeff = subset
            break
        else:
            continue
    temperature = 0
    for index, c in enumerate(coeff[2:]):
        temperature += c * millivoltage**index
    return temperature


def convert_to_voltage(temperature: float, TC_type: str) -> float:
    """Convert temperature in Celsius to voltage in millivolts."""
    table = globals()[f"TYPE_{TC_type.upper()}"]
    if temperature < table[0][0] or temperature > table[-1][1]:
        raise ValueError("temperature out of valid range for TC")
    for subset in table:
        if temperature >= subset[0] and temperature <= subset[1]:
            coeff = subset
            break
        else:
            continue
    millivoltage = 0
    if TC_type.upper() != 'K':
        for index, c in enumerate(coeff[2:]):
            millivoltage += c * temperature**index
    else:
        for index, c in enumerate(coeff[2:-3]):
            millivoltage += c * temperature**index
        millivoltage += coeff[-3] * exp(coeff[-2] * (temperature - coeff[-1])**2)
    return millivoltage
