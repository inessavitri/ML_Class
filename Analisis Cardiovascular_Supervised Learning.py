# -*- coding: utf-8 -*-
"""KELOMPOK 7_ENSEMBLE MODEL

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16XIGi9bPv23lhruMe6bDxrnTApf6sl4R

### KELOMPOK 7

- Angela Saputri
- Mutiara Larasati
- Ines Savitri

## **INTRODUCTION**

### **Latar Belakang**

Cardiovascular diseases (CVDs) adalah penyebab kematian nomor 1 secara global, mengambil sekitar 17,9 juta jiwa setiap tahun, yang menyumbang 31% dari semua kematian di seluruh dunia.Gagal jantung adalah kejadian umum yang disebabkan oleh CVD dan kumpulan data ini berisi 12 fitur yang dapat digunakan untuk memprediksi kematian akibat gagal jantung.

Sebagian besar penyakit kardiovaskular dapat dicegah dengan mengatasi faktor risiko perilaku seperti penggunaan tembakau, diet tidak sehat dan obesitas, kurangnya aktivitas fisik, dan penggunaan alkohol yang berbahaya menggunakan strategi di seluruh populasi.

Orang dengan penyakit kardiovaskular atau yang berada pada risiko kardiovaskular tinggi (karena adanya satu atau lebih faktor risiko seperti hipertensi, diabetes, hiperlipidemia atau penyakit yang sudah ada) memerlukan deteksi dan manajemen dini di mana model pembelajaran mesin dapat sangat membantu.

### **Data yang digunakan**

Dataset yang digunakan berasal dari kaggle dataset https://www.kaggle.com/datasets/andrewmvd/heart-failure-clinical-data,  yang berisi 299 baris dan 3 kolom. 
Data tersebut berisi kumpulan fitur yang digunakan untuk memprediksi kematian akibat gagal jantung.

### **Dataset Heart Failure**
Data ini memiliki 13 atribut dengan tujuan yang ingin dicapai dari final project ini adalah prediksi kematian akibat penyakit gagal jantung. Berikut adalah informasi atribut data heart failure :

1. age - umur pasien
2. anaemia - apakah ada pengurangan haemoglobin (1 = yes; 0 = no)
3. creatinine_phosphokinase - level enzim CPK dalam mcg/L
4. diabetes - apakah pasien punya riwayat diabete (1 = yes; 0 = no)
5. ejection_fraction - persentase darah yang meninggalkan jantung dalam persentasi di setiap kontraksi jantung
6. high_blood_pressure - apakah pasien punya darah tinggi (1 = yes; 0 = no)
7. platelets - jumlah platelet di darah dalam kiloplatelets/mL
8. serum_creatinine - level serum creatinine di darah dalam mg/dL
9. serum_sodium - level serum sodium di darah dalam mEq/L
10. sex - apakah pasien pria atau wanita (1 = male; 0 = female)
11. smoking - apakah pasien merokok (1 = yes; 0 = no)
12. time - waktu dalam hari untuk follow-up
13. DEATH_EVENT - apakah pasien sudah meninggal saat waktu follow-up (1 = yes Death; 0 = no)

### **Objektif yang ingin dicapai**
- Mampu memahami konsep Classification dengan Ensamble Model
- Mampu mempersiapkan data untuk digunakan dalam Ensemble Model
- Mampu mengimplementasikan Ensamble Model untuk membuat Prediksi

### **Import Pustaka**
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np 
import missingno as msn
import math
import scipy.stats
import statsmodels.api as sm

from matplotlib import pylab
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# %matplotlib inline

from sklearn.preprocessing import StandardScaler

from sklearn import metrics
from sklearn import preprocessing
from sklearn import ensemble
from scipy.stats import randint
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import BorderlineSMOTE
from imblearn.over_sampling import ADASYN

from sklearn.utils import resample

import warnings
warnings.filterwarnings('ignore')

from google.colab import files
uploaded = files.upload()

# Download datasets
df = pd.read_csv('heart_failure_clinical_records_dataset.csv')

df.head()

# Mengetahui jumlah data dan kolom
df.shape

df.dtypes

df.info()

# Mengetahui nilai unik |data column
for col in df.columns :
  print(col, 'Unique Value')
  print(df[col].unique())
  print('-'*100)

"""## **Data Cleaning**"""

# Mengetahui missing value pada setiap baris dan kolom
df.isnull()

# Cleansing data dengan standar missing value
df.isnull().sum()

"""Dapat terlihat bahwa dataset yang digunakan tidak memiliki missing value.

### **Cek Duplikasi Data**
"""

# Mengetahui apakah terdapat duplikasi data dalam dataset
df.duplicated()

df.duplicated().sum()

"""Dapat terlihat bahwa pada dataset yang digunakan tidak terdapat duplikasi data.

### **Cek Outliers**
"""

df.describe()

for col in df.columns:
    plt.figure()
    sns.boxplot(x=df[col])
plt.show()

"""### **Mengatasi Outliers**"""

for x in df.columns:
    Q1,Q3 = np.percentile(df.loc[:,x], [25, 75])
    IQR = Q3-Q1
    
    upper_bound = Q3 + (1.5*IQR)
    lower_bound = Q1 - (1.5*IQR)

    df.loc[df[x] < lower_bound, x] = np.nan
    df.loc[df[x] > upper_bound, x] = np.nan

df.isnull().sum()
median = df.median()
df.fillna(median,inplace=True)

for col in df.columns:
    plt.figure()
    sns.boxplot(x=df[col])
plt.show()

"""Sudah tidak terdapat nilai outlier"""

# Setelah outlier diatas
df.describe()

"""# **EDA (Exploratory Data Analysis)**

### **Numeric and Categoric**

Tahap ini akan membagi data menjadi data kategori dan data numeric, yang berguna untuk visualisasi data
"""

# Numerical Fitur 
# Tipe data yang berisi angka atau bilangan
num_col = ['age', 'creatinine_phosphokinase', 'ejection_fraction', 'platelets', 'serum_creatinine', 'serum_sodium', 'time']

# Categorical Fitur
# Tipe data yang hanya memiliki dua nilai, yaitu 0 dan 1
cat_col = ['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking', 'DEATH_EVENT']

"""**Distribusi Kolom Gender**"""

# Distribusi Kolom Gender

ax = sns.countplot(x="sex",data = df, palette='BrBG');
ax.set_title("Data berdasarkan Gender (Perempuan dan Laki-Laki)", y=1.02, fontsize=11, fontweight="bold")
for rect in ax.patches:
    ax.text (rect.get_x() + rect.get_width()  / 2,rect.get_height()+ 0.45,rect.get_height(),horizontalalignment='center', fontsize = 11)

"""Note : (0) adalah Perempuan (1) adalah Laki-Laki

Dari output di atas, dapat kita ketahui terdapat 105 Pasien Perempuan dan 194 Pasien Laki-Laki. Berarti 65% adalah Laki-Laki. Ada data gender yang lebih condong seperti yang biasanya kita perkirakan perincian antara gender seharusnya mendekati 50/50.

**Pasien meninggal berdasarkan umur**
"""

# Berapa banyak pasien yang meninggal berdasarkan umur?

g = sns.catplot(x="sex", kind="count", hue="DEATH_EVENT", data= df, palette="Set2")
g.fig.suptitle("Pasien yang meninggal berdasarkan umur", y=1.03, fontsize=18, fontweight="bold")

# extract the matplotlib axes_subplot objects from the FacetGrid
ax = g.facet_axis(0, 0)

# iterate through the axes containers
for c in ax.containers:
    labels = [v.get_height() for v in c]
    ax.bar_label(c, labels=labels, label_type='edge')

"""Dari output di atas, dapat kita ketahui bahwa

- 196 laki-laki, 62 (31,6%) meninggal.
- 105 perempuan, 34 (32,4%) meninggal. 

Secara keseluruhan, dari 299 pasien, 96 (32%) meninggal.

**Distribusi Pasien Penderita Anemia**
"""

# Distribusi Pasien Penderita Anemia
fig = px.pie(df, names='anaemia', height=400, width= 400, color_discrete_sequence=px.colors.sequential.Blues_r,  title='Anaemia')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()

"""Terdapat 56.9% pasien yang tidak mempunyai anaemia, dan yang mempunyai anaemia 43.1%"""

# Kolom Anaemia

g = sns.catplot(x="anaemia",  kind="count", hue= "DEATH_EVENT", col = "sex", data = df, palette="Set2");
g.fig.suptitle("Nilai Frekuensi dari kolom Anaemia", y=1.0, fontsize=13, fontweight="bold")


for ax in g.axes.ravel():

    for c in ax.containers:
        labels = [v.get_height() for v in c]
        ax.bar_label(c, labels=labels, label_type='edge')

"""Dari output di atas, dapat kita ketahui bahwa

1. Hampir setengah dari perempuan menderita anemia.
- 13% perempuan yang meninggal tidak menderita anemia.
- 19% perempuan yang meninggal menderita anemia.
2. 40% laki-laki mengalami anemia.
- 19% laki-laki yang meninggal tidak menderita anemia.
- 13% laki-laki yang meninggal menderita anemia. 

Tampaknya anemia bukan merupakan faktor risiko utama terutama pada pria.

**Distribusi Pasien Penderita Diabetes**
"""

# Distribusi Pasien Penderita Diabetes
fig = px.pie(df, names='diabetes', height=400, width= 400, color_discrete_sequence=px.colors.sequential.Blues_r,  title='Diabetes')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()

"""
Pasien yang mengidap diabetes sebanyak 41.8% dan yang tidak mempunyai riwayat diabetes lebih banyak yaitu 58.2%"""

# Kolom Diabetes

g = sns.catplot(x="diabetes",  kind="count", hue= "DEATH_EVENT", col = "sex", data = df, palette="Set2");
g.fig.suptitle("Nilai Frekuensi dari kolom Diabetes", y=1.05, fontsize=12, fontweight="bold")


for ax in g.axes.ravel():

    for c in ax.containers:
        labels = [v.get_height() for v in c]
        ax.bar_label(c, labels=labels, label_type='edge')

"""Dari output di atas dapat kita ketahui bahwa:

1. 52% perempuan menderita diabetes.
- 19% perempuan dengan diabetes meninggal.
- 13% perempuan tanpa diabetes meninggal.
2. 36% laki-laki menderita diabetes.
- 10% laki-laki dengan diabetes meninggal.
- 22% laki-laki tanpa diabetes meninggal. 

Diabetes tampaknya bukan penyebab utama kematian di antara para pasien.
"""

# Distribusi Pasien Penderita Diabetes
fig = px.pie(df, names='high_blood_pressure', height=400, width= 400, color_discrete_sequence=px.colors.sequential.Blues_r,  title='High Blood Pressure')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()

"""Pasien yang mengidap darah tinggi sebanyak 35.1% dan yang tidak mempunyai riwayat darah tinggi lebih banyak yaitu 64.9%"""

# Kolom High Blood Pressure

g = sns.catplot(x="high_blood_pressure",  kind="count", hue= "DEATH_EVENT", col = "sex", data = df, palette="Set2");
g.fig.suptitle("Nilai Frekuensi dari kolom High Blood Pressure", y=1.0, fontsize=12, fontweight="bold")


for ax in g.axes.ravel():

    for c in ax.containers:
        labels = [v.get_height() for v in c]
        ax.bar_label(c, labels=labels, label_type='edge')

"""Dari output di atas, dapat kita ketahui bahwa:

1. 42% perempuan memiliki tekanan darah tinggi.
- 16% perempuan dengan tekanan darah tinggi meninggal.
- 16% perempuan tanpa tekanan darah tinggi meninggal.
2. 31% laki-laki memiliki tekanan darah tinggi.
- 11% laki-laki dengan tekanan darah tinggi meninggal.
- 21% laki-laki tanpa tekanan darah tinggi meninggal. 

Tekanan darah tinggi saja bukanlah faktor risiko utama.
"""

# Kolom Smoking

g = sns.catplot(x="smoking",  kind="count", hue= "DEATH_EVENT", col = "sex", data = df, palette="Set2");
g.fig.suptitle("Nilai Frekuensi dari kolom Smoking", y=1.0, fontsize=12, fontweight="bold")


for ax in g.axes.ravel():

    for c in ax.containers:
        labels = [v.get_height() for v in c]
        ax.bar_label(c, labels=labels, label_type='edge')

"""Dari Output di atas, dapat kita ketahui bahwa:

1. Merokok populer di kalangan pria dibandingkan dengan wanita: 0,04% wanita merokok.
- 3 dari 4 perokok pada wanita meninggal.
- 30% wanita bukan perokok meninggal.
2. 47% pria merokok.
- 14% perokok pria meninggal.
- 18% pria bukan perokok meninggal. 

Setidaknya berdasarkan data laki-laki, merokok tampaknya tidak menjadi faktor risiko utama.
"""

# Distribusi Ejection Fraction atau Fraksi Ejeksi

plt.figure(1 , figsize = (20, 9 ))

plt.subplot(1 , 2 , 1)
'''Fraksi ejeksi normal antara 50% sampai 75%, berdasarkan dari American Heart Association'''
plt.scatter(x = 'age' , y = 'ejection_fraction' , data = df[(df['ejection_fraction'] > 75)] , color = 'b' , s = 30  , alpha = 0.5 , 
           label = 'High Ejection Fraction Percent')
plt.scatter(x = 'age' , y = 'ejection_fraction' , data = df[(df['ejection_fraction'] <= 75) & (df['ejection_fraction'] > 50 )] , 
            color = 'green' , s = 50  , alpha = 0.5 , label = 'Normal Ejection Fraction Percent')

'''Garis peningkatan fraksi ejeksi bisa dalam rentang antara 41% dan 50%'''
plt.scatter(x = 'age' , y = 'ejection_fraction' , data = df[(df['ejection_fraction'] <= 50 ) & (df['ejection_fraction'] >= 41)] , 
            color = 'y' , s = 50 , alpha = 0.5 , label = 'Border Line Ejection Fraction Percent')
plt.scatter(x = 'age' , y = 'ejection_fraction' , data = df[(df['ejection_fraction'] <= 40 )] , color = 'r' , s = 30 , alpha = 0.5 , 
           label = 'Low Ejection Fraction Percent')
plt.xlabel('Age')
plt.ylabel('Ejection Fraction (in %)')
plt.legend()

plt.subplot(1 , 2 , 2 )
plt.scatter(x = 'age' , y = 'ejection_fraction' , data = df[df['DEATH_EVENT'] == 0 ] , label = 'No' , alpha = 0.3 )
plt.scatter(x = 'age' , y = 'ejection_fraction' , data = df[df['DEATH_EVENT'] == 1 ] , label = 'Yes' , s = 30 , color = 'r', alpha = 0.8 )
plt.xlabel('Age')
plt.ylabel('Ejection Fraction (in %)')
plt.legend()

plt.show()

"""Ejection Fraction (Fraksi ejeksi), mengukur jumlah darah yang dipompa keluar dari bilik bawah jantung, atau ventrikel. Ini adalah persentase darah yang meninggalkan ventrikel kiri saat jantung berkontraksi. Fraksi ejeksi normal adalah sekitar 50% hingga 75%, menurut American Heart Association. Fraksi ejeksi batas dapat berkisar antara 41% dan 50%"""

df.query('ejection_fraction <= 75' and 'ejection_fraction >50')

"""Untuk pasien yang memiliki fraksi ejeksi normal sebanyak 37 pasien dengan jumlah pasien yang meninggal sebanyak 7."""

# Distribusi Platelets atau Trombosit
plt.figure(1 , figsize = (20, 9 ))

plt.subplot(1 , 2 , 1)
'''Jumlah trombosit normal berada direntang 150,000 sampai 450,000 trombosit per mikroliter darah.'''
plt.scatter(x = 'age' , y = 'platelets' , data = df[(df['platelets'] > 450001)] , color = 'b' , s = 50  , alpha = 0.5 , 
           label = 'Thrombocytosis (High Blood Platelets)')
plt.scatter(x = 'age' , y = 'platelets' , data = df[(df['platelets'] <= 450000) & (df['platelets'] >= 150000 )] , 
            color = 'green' , s = 100  , alpha = 0.5 , label = 'Normal platelet count range')
plt.scatter(x = 'age' , y = 'platelets' , data = df[(df['platelets'] < 150000 )] , color = 'r' , s = 50 , alpha = 0.5 , 
           label = 'Thrombocytopenia (Low Blood Platelets)')
plt.xlabel('Age')
plt.ylabel('Platelets in the blood (kiloplatelets/mL)')
plt.legend()

plt.subplot(1 , 2 , 2 )
plt.scatter(x = 'age' , y = 'platelets' , data = df[df['DEATH_EVENT'] == 0 ] , label = 'Noh' , alpha = 0.3 )
plt.scatter(x = 'age' , y = 'platelets' , data = df[df['DEATH_EVENT'] == 1 ] , label = 'Yes' , s = 50 , color = 'r', alpha = 0.8 )
plt.xlabel('Age')
plt.ylabel('Platelets in the blood (kiloplatelets/mL)')
plt.legend()

plt.show()

"""Jumlah trombosit normal berkisar antara 150.000 hingga 450.000 trombosit per mikroliter darah. Memiliki lebih dari 450.000 trombosit adalah suatu kondisi yang disebut trombositosis. Memiliki kurang dari 150.000 dikenal sebagai trombositopenia"""

df.query('platelets > 450001')

"""Tidak ada pasien yang memiliki trombosit tinggi.

**Jumlah Pasien Meninggal**
"""

# Set Label
yes = len(df[df['DEATH_EVENT'] == 1])
no = len(df[df['DEATH_EVENT'] == 0])

plt.rcdefaults()
fig, ax = plt.subplots()
y = ('yes', 'no')
y_total = np.arange(len(y))
x = (yes, no)
ax.barh(y_total, x, align='center')
ax.set_yticks(y_total)
ax.set_yticklabels(y)
ax.invert_yaxis() # labels read top-to-bottom
ax.set_xlabel('Count')
ax.set_title('DEATH EVENT')
for i, v in enumerate(x):
    ax.text(v + 10, i, str(v), color='black', va='center', fontweight='normal')
plt.show()

y = ('yes', 'no')
y_total = np.arange(len(y))
x = (yes, no)
labels = 'yes', 'no'
sizes = [yes, no]
fig1, ax1 = plt.subplots()
ax1.pie(sizes,  labels=labels, autopct='%1.1f%%', startangle=90) 
ax1.axis('equal')
plt.title('Percentage of DEATH EVENT', size=16)
plt.show()

"""Pasien yang tidak meninggal lebih banyak dibanding yang meninggal, terdapat 203 (67.9%) pasien yang tidak meninggal dan 96 (32.1%) pasien yang meninggal.

Dari output di atas, dapat terlihat bahwa kolom DEATH_EVENT menunjukkan data yang imbalance. Imbalance adalah suatu keadaan dimana distribusi kelas data tidak seimbang, jumlah kelas data (instance) lebih sedikit atau lebih banyak dari data kelas lainnya. Maka perlu dilakukan teknik penyeimbangan data.

## **Data Pre-processing**

### **Korelasi**
"""

plt.figure(figsize=(12,10))
sns.heatmap(df.corr(), annot=True, cmap='YlGnBu')
plt.title("Correlation Heatmap");

"""- Terdapat korelasi negatif antara time dan DEATH_EVENT sebesar -0.53 artinya korelasi antara dua variabel ini berlawanan atau terbalik.
- Terdapat korelasi positif antara age dan DEATH_EVENT & serum_creatinine dan DEATH_EVENT yang artinya hubungan dua variabel ini bergerak dalam arah yang sama.
- Untuk variabel lainny memiliki korelasi yang netral dengan DEATH_EVENT, perubahan tidak mempengaruhi DEATH_EVENT.

**Menghapus kolom yang tidak digunakan**
"""

HF_Final = df.drop(columns= ['time'])

HF_Final.head()

"""Menghapus variabel time , karena tidak berhubungan dengan death_event. dan tujuannya adalah untuk memprediksi kematian atau kelangsungan hidup pasien, time tidak boleh digunakan sebagai input model.

**Scaling Data**
"""

scaler = StandardScaler()

data_X = HF_Final.drop(columns = ['DEATH_EVENT'])

X = scaler.fit_transform(data_X)
y = HF_Final["DEATH_EVENT"]

"""**Split Data**"""

# Split dataset menjadi training 80% dan testing 20%
x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=1)

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

"""## **Modelling**

### **BAGGING - RANDOM FOREST**
"""

model_rf = RandomForestClassifier(random_state=1)
model_rf.fit(x_train, y_train)

y_pred_rf = model_rf.predict(x_test)

print('Accuracy of Random Forest classifier on test set: {:.5f}'.format(metrics.accuracy_score(y_test, y_pred_rf)))

"""### **BOOSTING - GRADIENT BOOSTING**

**Boosting** adalah metode untuk mengubah pembelajaran yang lemah menjadi pembelajaran yang kuat. Dalam meningkatkan, setiap pohon baru cocok dengan versi modifikasi dari kumpulan data asli. Ini sangat bergantung pada prediksi bahwa model berikutnya akan mengurangi kesalahan prediksi ketika digabung dengan yang sebelumnya. Ide utamanya adalah untuk menetapkan hasil target untuk model yang akan datang ini untuk meminimalkan kesalahan.

**Gradient Boosting** melatih banyak model secara bertahap, aditif, dan berurutan. Istilah peningkatan gradien muncul karena hasil target setiap kasus didasarkan pada kesalahan gradien sehubungan dengan prediksi. Setiap model mengurangi kesalahan prediksi dengan mengambil langkah ke arah yang benar.
"""

model_GB = ensemble.GradientBoostingClassifier(random_state=1)
model_GB.fit(x_train,y_train)

y_pred_GB = model_GB.predict(x_test)

print('Accuracy of Gradient Boosting classifier on test set: {:.5f}'.format(metrics.accuracy_score(y_test, y_pred_GB)))

"""### **Hyperparameter Turning Random Forest (Hutan Acak)**"""

rs_space={'max_depth':list(np.arange(10, 100, step=10)) + [None],
              'n_estimators':np.arange(10, 500, step=50),
              'max_features':randint(1,10),
              'criterion':['gini','entropy'],
              'min_samples_leaf':randint(1,4),
              'min_samples_split':np.arange(2, 10, step=2)
         }

RF_rs = RandomizedSearchCV(model_rf, rs_space, n_iter=100, scoring='accuracy', n_jobs=-1, cv=3)
RF_rs_result = RF_rs.fit(x_train, y_train)

#Prediksi menggunakan model tuning
y_pred_rf_tunned = RF_rs_result.predict(x_test)

print('Accuracy of Random Forest classifier Tuning on test set: {:.5f}'.format(metrics.accuracy_score(y_test, y_pred_rf_tunned)))

print(RF_rs.best_params_)
print(classification_report(y_test, y_pred_rf_tunned))

"""### **Hyperparameter Tuning Gradient Boosting**"""

GBC_parameter_grid = {
         'n_estimators': np.arange(10,150,10), 
         'max_depth': range(1,20),
         'learning_rate': [0.001, 0.01, 0.1]
         }

GBC_rs = RandomizedSearchCV(model_GB, GBC_parameter_grid, scoring='roc_auc',n_jobs=4, cv=3)
GBC_rs_result = GBC_rs.fit(x_train,y_train)

#Prediksi menggunakan model tuning
y_pred_gb_tunned = GBC_rs_result.predict(x_test)

print('Accuracy of Gradient Boosting Tuning on test set: {:.5f}'.format(metrics.accuracy_score(y_test, y_pred_gb_tunned)))

print(GBC_rs.best_params_)
print(classification_report(y_test, y_pred_gb_tunned))

"""## **Evaluasi Model**"""

rf = metrics.accuracy_score(y_test, y_pred_rf)
gb = metrics.accuracy_score(y_test, y_pred_GB)
rfc_tunned = metrics.accuracy_score(y_test, y_pred_rf_tunned)
gb_tunned = metrics.accuracy_score(y_test, y_pred_gb_tunned)

# --- Create Accuracy Comparison Table ---
compare = pd.DataFrame({'Model': ['Random Forest', 'Gradient Boosting', 'Random Forest Tunned', 'Gradient Boosting Tunned'], 
                        'Accuracy': [rf*100, gb*100, rfc_tunned*100, gb_tunned*100]})

# --- Create Accuracy Comparison Table ---

compare.sort_values(by='Accuracy', ascending=False).style.background_gradient(cmap='PuRd').hide_index().set_properties(**{'font-family': 'Segoe UI'})

cm = confusion_matrix(y_test, RF_rs_result.predict(x_test))
cm = pd.DataFrame(cm , index = ['0', '1'] , columns = ['0', '1'])
plt.figure(figsize = (5,5))
plt.title("Gradient Boosting Confusion Matrix")
sns.heatmap(cm, cmap='Blues', annot = True, fmt='',xticklabels = ["0", "1"], yticklabels = ["0", "1"])
plt.xlabel('Predicted')
plt.ylabel('Actual')

cm = confusion_matrix(y_test, GBC_rs_result.predict(x_test))
cm = pd.DataFrame(cm , index = ['0', '1'] , columns = ['0', '1'])
plt.figure(figsize = (5,5))
plt.title("Gradient Boosting Confusion Matrix")
sns.heatmap(cm, cmap='Blues', annot = True, fmt='',xticklabels = ["0", "1"], yticklabels = ["0", "1"])
plt.xlabel('Predicted')
plt.ylabel('Actual')

"""### **Model Random Forest dan Gradient Bosting**"""

model_rf_tunned = RandomForestClassifier(criterion='entropy', max_depth=None, max_features=4, min_samples_leaf=1, min_samples_split=8, n_estimators=60)
model_rf_tunned.fit(x_train, y_train)

# Feature Penting
feature_imp = pd.Series(model_rf_tunned.feature_importances_, index=data_X.columns).sort_values(ascending=False)

sns.barplot(x=feature_imp, y=feature_imp.index)

plt.xlabel('Features Importance Score')
plt.ylabel('Features')
plt.title('Visualizing Important Features')

plt.show()

"""Berdasarkan feature important, 3 feature yang sangat penting adalah serum_creatinine, ejection_fraction dan juga age

Selesai.
"""



