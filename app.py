import streamlit as st
import pandas as pd
from tensorflow import keras
import tensorflow as tf
import numpy as np
import csv
import pydeck as pd
def custom_loss(y_actual, y_pred):
  n=tf.pow(y_actual-y_pred, 6)
  return n
def last_list(l):
    return l[len(l)-1]
hot_model=keras.models.load_model('hot_model.h5', custom_objects={'custom_loss': custom_loss})
cold_model=keras.models.load_model('cold_model.h5')
weather_h_model=keras.models.load_model('weather_hotmodel.h5')
weather_c_model=keras.models.load_model('weather_coldmodel.h5')
suj_weather_c_model=keras.models.load_model('su_weather_coldmodel.h5')
suj_weather_h_model=keras.models.load_model('su_weather_hotmodel.h5')
suj_hot_model=keras.models.load_model('su_hot_model.h5')
suj_cold_model=keras.models.load_model('su_cold_model.h5')
joo_weather_c_model=keras.models.load_model('jo_weather_coldmodel.h5')
joo_weather_h_model=keras.models.load_model('jo_weather_hotmodel.h5')
joo_hot_model=keras.models.load_model('jo_hot_model.h5')
joo_cold_model=keras.models.load_model('jo_cold_model.h5')
st.write("""
 ## __날씨에 따른__
 """)
st.write("""
 # __[지역별 가구 평균 전력 이용량 예측]__
날씨를 이용하여 성남시 각 구 가구들의 __평균 전력 이용량__ 을 예측합니다.
""")
region=st.selectbox("##예측을 원하시는 지역을 선택하세요.", ("성남시 분당구", "성남시 수정구", "성남시 중원구"))
temp_or_all=st.sidebar.selectbox("무엇으로 예측할까요?", ("월평균기온만으로 예측하기", "월평균기온, 평균풍속, 강수량, 상대습도, 평균기압으로 예측하기"))
temp=st.sidebar.slider("이번달 [월평균기온]을 지정하세요", -10.0, 35.0)
if temp_or_all!='월평균기온만으로 예측하기':
    wind=st.sidebar.slider("이번달 [평균풍속]을 지정하세요", 0.0, 2.5)
    prec=st.sidebar.slider("이번달 [월합강수량]을 지정하세요", 0, 850)
    hum=st.sidebar.slider("이번달 [평균상대습도]를 지정하세요", 0, 100)
    airpress=st.sidebar.slider("이번달 [평균현지기압]을 지정하세요", 1000.0, 1050.0)
search=st.sidebar.button("검색")
if search==True:
    def predict(temp):
      if temp >= 15:
         if temp_or_all=='월평균기온만으로 예측하기':
              return hot_model.predict([[temp**2, temp]])
         else:
             return weather_h_model.predict([[temp, wind, prec, hum, airpress]])
      else:
          if temp_or_all=='월평균기온만으로 예측하기':
              return cold_model.predict([temp])
          else:
             return weather_c_model.predict([[temp, wind, prec, hum, airpress]])

    def suj_predict(temp):
      if temp >= 15:
         if temp_or_all=='월평균기온만으로 예측하기':
              return suj_hot_model.predict([[temp**2, temp]])
         else:
             return suj_weather_h_model.predict([[temp, wind, prec, hum, airpress]])
      else:
          if temp_or_all=='월평균기온만으로 예측하기':
              return suj_cold_model.predict([temp])
          else:
             return suj_weather_c_model.predict([[temp, wind, prec, hum, airpress]])
    def joo_predict(temp):
      if temp >= 15:
         if temp_or_all=='월평균기온만으로 예측하기':
              return joo_hot_model.predict([[temp**2, temp]])
         else:
             return joo_weather_h_model.predict([[temp, wind, prec, hum, airpress]])
      else:
          if temp_or_all=='월평균기온만으로 예측하기':
              return joo_cold_model.predict([temp])
          else:
             return joo_weather_c_model.predict([[temp, wind, prec, hum, airpress]])
    def predict_result(region):
        if region=='성남시 분당구':
            n=float(predict(temp))

            return n

        elif region=='성남시 수정구':
            n=float(suj_predict(temp))
            return n
        else:
            n=float(joo_predict(temp))
            return n

    line='<p style="font-family:sans-serif; color:Blue; font-size: 12px;">=================================================================================</p>'
    line2='<p style="font-family:sans-serif; color:Blue; font-size: 22px;">               전력 이용량 예측 결과 :                  </p>'
    st.write(line, unsafe_allow_html=True)
    st.write('{0} {1}kWh'.format(line2, round(predict_result(region), 2)), unsafe_allow_html=True)
    st.write(line, unsafe_allow_html=True)

    #st.write('월평균기온이 {0}°C'.format(temp))
    # if temp_or_all=='월평균기온만으로 예측하기':
    #     exp= '<p style="font-family:sans-serif; color:Green; font-size: 24px;"> 월평균기온이</p>'
    #
    #     exp2='<p style="font-family:sans-serif; color:Green; font-size: 24px;">일 때 월 가구 평균 전력이용량 예측값:</p>'
    #     st.write(exp, unsafe_allow_html=True)
    #     st.write('{0}℃'.format(temp))
    #     st.write(exp2, unsafe_allow_html=True)
    # else:
    #     exp=new_title = '<p style="font-family:sans-serif; color:Green; font-size: 24px;"> 월평균기온, 평균풍속, 월압강수량, 상대습도, 기압이 각각, </p>'
    #
    #     exp2='<p style="font-family:sans-serif; color:Green; font-size: 24px;">일 때 월 가구 평균 전력이용량 예측값:</p>'
    #     st.write(exp, unsafe_allow_html=True)
    #     st.write('{0}℃, {1}, {2}, {3}, {4}'.format(temp, wind, prec, hum, airpress))
    #     st.write(exp2, unsafe_allow_html=True)
    # if region=='성남시 분당구':
    #     n=float(predict(temp))
    #
    #     st.write("__{0} kWh__".format(round(n, 3)))
    #
    # elif region=='성남시 수정구':
    #     n=float(suj_predict(temp))
    #     st.write("__{0} kWh__".format(round(n, 3)))
    # else:
    #     n=float(joo_predict(temp))
    #     st.write("__{0} kWh__".format(round(n, 3)))

#st.pydeck_chart(pydeck.Deck(initial_view_state=pydeck.ViewState(longitude=127.1388684, latitude=37.4449168, zoom=12, min_zoom=10, max_zoom=14)))
