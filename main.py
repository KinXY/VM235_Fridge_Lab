from Fluids_ID import Fluids_ID
import pandas as pd
import time
import numpy as np

fluid_name = "isobutane"
fluid_id = Fluids_ID[fluid_name]

T1 = -1.575
T2 = 66.467
T3 = 59.112
T4 = 56.917
T5 = 53.536
T6 = 45.920
T7 = 2.262
T8 = 1.866
T9 = 0.980
T10 = 10.192
T11 = 21.532
T_Ambient = 24.248
P1 = 0.133
P2 = 0.736
P6 = 0.652
P7 = 0.352


def get_P(PA, TA, TB):
    k = 1.1
    res = PA * pow((TB + 273.15) / (TA + 273.15), k / (k - 1))
    res = round(res, 3)
    return res


# arrange the data into a list of dict
data = [
    {"T": T1, "P": P1},
    {"T": T2, "P": P2},
    {"T": T3, "P": get_P(P2, T2, T3)},
    {"T": T4, "P": get_P(P2, T2, T4)},
    {"T": T5, "P": get_P(P2, T2, T5)},
    {"T": T6, "P": P6},
    {"T": T7, "P": P7},
    {"T": T8, "P": get_P(P7, T7, T8)},
    {"T": T9, "P": get_P(P1, T1, T9)},
]


def get_nist_data(T, P):
    request = f"https://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&T={T}&PLow={P}&PHigh={P}&PInc=1&Digits=3&ID={fluid_id}&Type=IsoTherm&TUnit=C&PUnit=MPa&DUnit=mol%2Fl&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm&RefState=DEF"
    # get the data from the website. If error occurs, try again
    handbook = pd.DataFrame()
    while handbook.empty:
        try:
            handbook = pd.read_csv(request, delimiter="\t")
        except:
            print(f"Error occurs when getting data at T = {T}, P = {P}. Try again.")
            time.sleep(1)
    # transform the dataframe into dict
    handbook = handbook.to_dict("records")[0]
    return handbook


# get and output the T-s diagram
def get_TS():
    ts_data = []
    for item in data:
        T = item["T"]
        P = item["P"]
        handbook = get_nist_data(T, P)
        s = handbook["Entropy (J/g*K)"]
        ts_data.append({"T": T, "s": s})
    return ts_data


def get_PH():
    ph_data = []
    for item in data:
        T = item["T"]
        P = item["P"]
        handbook = get_nist_data(T, P)
        h = handbook["Enthalpy (kJ/kg)"]
        ph_data.append({"P": P, "h": h})
    return ph_data

def get_TS_saturation():
    request = "https://webbook.nist.gov/cgi/fluid.cgi?TLow=0&THigh=&TInc=1&Digits=3&ID=C75285&Action=Data&Wide=On&Type=SatP&TUnit=C&PUnit=MPa&DUnit=mol%2Fl&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm&RefState=DEF"
    handbook = pd.DataFrame()
    while handbook.empty:
        try:
            handbook = pd.read_csv(request, delimiter="\t")
        except:
            time.sleep(1)
    # transform the dataframe into dict of lists
    handbook = handbook.to_dict("list")
    T_list1 = handbook["Temperature (C)"]
    s_list1 = handbook["Entropy (l, J/g*K)"]
    # get the reversed list
    T_list2 = handbook["Temperature (C)"][::-1]
    s_list2 = handbook["Entropy (v, J/g*K)"][::-1]
    # combine the two lists
    T_list = T_list1 + T_list2
    s_list = s_list1 + s_list2
    return T_list, s_list


def get_PH_saturation():
    request = "https://webbook.nist.gov/cgi/fluid.cgi?TLow=0&THigh=&TInc=1&Digits=3&ID=C75285&Action=Data&Wide=On&Type=SatP&TUnit=C&PUnit=MPa&DUnit=mol%2Fl&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm&RefState=DEF"
    handbook = pd.DataFrame()
    while handbook.empty:
        try:
            handbook = pd.read_csv(request, delimiter="\t")
        except:
            time.sleep(1)
    # transform the dataframe into dict of lists
    handbook = handbook.to_dict("list")
    P_list1 = handbook["Pressure (MPa)"]
    h_list1 = handbook["Enthalpy (l, kJ/kg)"]       
    # get the reversed list
    P_list2 = handbook["Pressure (MPa)"][::-1]
    h_list2 = handbook["Enthalpy (v, kJ/kg)"][::-1]
    # combine the two lists
    P_list = P_list1 + P_list2
    h_list = h_list1 + h_list2
    return P_list, h_list


def get_TS_isobar(P):
    request = f"https://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&P={P}&TLow=-20&THigh=100&TInc=1&Digits=3&ID={fluid_id}&Type=IsoBar&TUnit=C&PUnit=MPa&DUnit=mol%2Fl&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm&RefState=DEF"
    handbook = pd.DataFrame()
    while handbook.empty:
        try:
            handbook = pd.read_csv(request, delimiter="\t")
        except:
            time.sleep(1)
    # transform the dataframe into dict
    handbook = handbook.to_dict("list")
    T_list = handbook["Temperature (C)"]
    s_list = handbook["Entropy (J/g*K)"]
    return T_list, s_list

def output_TS():
    ts_data = get_TS()
    T_list = [item["T"] for item in ts_data]
    s_list = [item["s"] for item in ts_data]
    T_sat_list, s_sat_list = get_TS_saturation()
    T_isobarMin, s_isobarMin = get_TS_isobar(P1)
    T_isobarMax, s_isobarMax = get_TS_isobar(P2)
    with open("ts_sat_data.txt", "w") as f:
        f.write(f"T = {T_list};\n")
        f.write(f"s = {s_list};\n")
        f.write(f"T_sat = {T_sat_list};\n")
        f.write(f"s_sat = {s_sat_list};\n")
        f.write(f"T_isobarMin = {T_isobarMin};\n")
        f.write(f"s_isobarMin = {s_isobarMin};\n")
        f.write(f"T_isobarMax = {T_isobarMax};\n")
        f.write(f"s_isobarMax = {s_isobarMax};\n")

def output_PH():
    ph_data = get_PH()
    P_list = [item["P"] for item in ph_data]
    h_list = [item["h"] for item in ph_data]
    P_sat_list, h_sat_list = get_PH_saturation()
    with open("ph_sat_data.txt", "w") as f:
        f.write(f"P = {P_list};\n")
        f.write(f"h = {h_list};\n")
        f.write(f"P_sat = {P_sat_list};\n")
        f.write(f"h_sat = {h_sat_list};\n")

if __name__ == "__main__":
    output_PH()
    
