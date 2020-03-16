# -*- coding: utf-8 -*-
"""
感染症シミュレーション（SIRモデル）
Created on Sat Mar 15 14:00:00 2020
@author: Kazunori Asada
"""

import datetime
import matplotlib.pyplot as plt
import numpy as np

# 常微分方程式（SIR）
def ODE_SIR(s0, i0, r0, infR, recR):
    dSdt = -infR * s0 * i0;
    dIdt = infR * s0 * i0 - recR * i0;
    dRdt = recR * i0;
    s1 = s0 + dSdt;
    i1 = i0 + dIdt;
    r1 = r0 + dRdt;
    return s1, i1, r1
    
days = 365
# 配列変数
Susceptible = np.zeros(days + 1) # 感受者数
Infected = np.zeros(days + 1) # 感染者数
Recovered = np.zeros(days + 1) # 回復者数

# 初期値
Population = 10000 # 人口
InfectionRate = 0.21 # 感染率
RecoverRate = 0.14 # 快復率
Infected[0] = 1.0 / Population # 初期感染者数
Susceptible[0] = 1.0 - Infected[0] # 初期感受者数
Recovered[0] = 0.0 # 初期快復者数
PeakPatient = 0.0 #ピーク時の患者数
PeakDay = 0 # ピークまでの日数

R0 = InfectionRate / RecoverRate # 基本再生産数

for t in range(days):
    Susceptible[t + 1], Infected[t + 1], Recovered[t + 1] = ODE_SIR(Susceptible[t], Infected[t], Recovered[t], InfectionRate, RecoverRate)
    if Infected[t + 1] < 1.0 / Population:
        break
    if PeakPatient == 0.0 and Infected[t + 1] < Infected[t]:
        PeakPatient = Infected[t]
        PeakDay = t
    
Infected *= Population
Susceptible *= Population
Recovered *= Population
TerminateDay = t + 1
PeakPatient *= Population
TotalInfection = Recovered[TerminateDay] # 総感染者数

# 2020/01/16に日本国内で初の感染者が確認されてからの経過日数
ElapsedDays = (datetime.datetime.today() - datetime.datetime(2020, 1, 16)).days

# -- プロット
X = np.zeros(days + 1)
for t in range(days + 1):
    X[t] = t
    
plt.title("SIR Epidemics Model")
plt.xlabel("days")
plt.ylabel("poplation")
plt.plot(X, Susceptible, label="Susceptible")
plt.plot(X, Infected, label = "Infected")
plt.plot(X, Recovered, label = "Recovered")
plt.xlim(0, TerminateDay)
if ElapsedDays < TerminateDay:
    plt.vlines(ElapsedDays, 0, Population, 'red', linestyles='dashed', label='today')
    plt.text(ElapsedDays+2, Population/2, 'Today', rotation=90, verticalalignment='center')
plt.legend()
plt.show()
print("Basic reproduction number (R0): ", R0)
print("Number of infected people: %d/%d (%d%%)" % (TotalInfection, Population, TotalInfection * 100.0 / Population ))
print("Peak: %d patients, day %d" % (PeakPatient, PeakDay))
print("Outbreak End: day", TerminateDay)
