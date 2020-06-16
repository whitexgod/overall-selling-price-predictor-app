from flask import Flask,render_template,request
import pandas as pd
import numpy as np
import pickle

clf_mobile = pickle.load(open('model86%.pkl','rb'))
df_mobile = pickle.load(open('process.pkl', 'rb'))
clf_car = pickle.load(open('model3.pkl','rb'))
clf_bike = pickle.load(open('model90%.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST','GET'])
def predict():
    selected=request.form.get('selected')
    print(selected)
    try:
        if selected == 'car':
            return render_template('index_car.html')
        elif selected == 'mobile':
            return render_template('index_mobile.html', df_mobile=df_mobile)
        elif selected == 'bike':
            return render_template('index_bike.html')
        elif selected == 'laptop':
            return render_template('index_laptop.html')
    except:

        return render_template('index.html')


@app.route('/predict_car', methods=['POST'])
def predict_car():
    try:
        company=request.form.get('company')
        year=request.form.get('year')
        fuel_type=request.form.get('fuel_type')
        kms_driven=request.form.get('kms')
        company=company.lower()
        fuel_type.lower()
        company=company.capitalize()
        kms_driven=kms_driven.strip('kms')
        kms_driven = kms_driven.strip('km')
        def change(text):
            if text == 'petrol':
                return 1
            elif text == 'diesel':
                return 2
            else:
                return 3
        fuel=change(fuel_type)

        d = {'company': company, 'year': year, 'kms_driven': kms_driven, 'fuel_type': fuel}
        data = pd.DataFrame(d, index=[1])
        new = pd.DataFrame(columns=['kms_driven', 'company_Audi', 'company_BMW', 'company_Chevrolet',
                                    'company_Datsun', 'company_Fiat', 'company_Force', 'company_Ford',
                                    'company_Hindustan', 'company_Honda', 'company_Hyundai',
                                    'company_Jaguar', 'company_Jeep', 'company_Land',
                                    'company_Mahindra', 'company_Maruti', 'company_Mercedes',
                                    'company_Mini', 'company_Mitsubishi', 'company_Nissan',
                                    'company_Renault', 'company_Skoda', 'company_Tata',
                                    'company_Toyota', 'company_Volkswagen', 'company_Volvo',
                                    'fuel_type_1', 'fuel_type_2', 'fuel_type_3', 'year_1995',
                                    'year_2000', 'year_2001', 'year_2002', 'year_2003', 'year_2004',
                                    'year_2005', 'year_2006', 'year_2007', 'year_2008', 'year_2009',
                                    'year_2010', 'year_2011', 'year_2012', 'year_2013', 'year_2014',
                                    'year_2015', 'year_2016', 'year_2017', 'year_2018', 'year_2019'])
        F = pd.get_dummies(data, columns=['company', 'fuel_type', 'year'])
        new[F.columns.values] = F[F.columns.values]
        new = new.replace(np.nan, 0)
        x = new.iloc[:, :].values
        pred=round(clf_car.predict(x)[0],2)

        return render_template('index_car.html', pred=pred, label=1)

    except:

        return render_template('index_car.html', label=0)


@app.route('/predict_mobile', methods=['POST'])
def predict_mobile():
    try:

        brand=request.form.get('brand')
        ram=request.form.get('ram')
        rom=request.form.get('rom')
        screen=request.form.get('screen')
        Primary_cam=request.form.get('Primary_cam')
        front_cam=request.form.get('front_cam')
        processor_cost=request.form.get('processor')
        screen=screen.lower().strip('inch')
        Primary_cam=Primary_cam.lower().strip('megapixel')
        front_cam=front_cam.lower().strip('megapixel')

        new = pd.DataFrame(columns=['screen_size', 'Primary_cam', 'front_cam', 'brand_Apple',
                                    'brand_Asus', 'brand_General', 'brand_Gionee', 'brand_Google',
                                    'brand_HTC', 'brand_Honor', 'brand_Huawei', 'brand_InFocus',
                                    'brand_LG', 'brand_Micromax', 'brand_Motorola', 'brand_Nokia',
                                    'brand_OnePlus', 'brand_Oppo', 'brand_Panasonic', 'brand_Realme',
                                    'brand_Samsung', 'brand_Vivo', 'brand_Xiaomi', 'ram_1', 'ram_2',
                                    'ram_3', 'ram_4', 'ram_6', 'ram_8', 'ram_12', 'rom_1', 'rom_8',
                                    'rom_16', 'rom_32', 'rom_64', 'rom_128', 'rom_256', 'rom_512'])
        d = {'brand': brand, 'screen_size': screen, 'Primary_cam': Primary_cam, 'front_cam': front_cam,
             'ram': ram, 'rom': rom}
        data = pd.DataFrame(d, index=[1, 2])
        F = pd.get_dummies(data, columns=['brand', 'ram', 'rom'])
        new[F.columns.values] = F[F.columns.values]
        new = new.replace(np.nan, 0)
        x = new.iloc[:, :].values
        p1=round(clf_mobile.predict(x)[0],2)
        p2=round(clf_mobile.predict(x)[0],2)/2.5
        pred=round(p1-p2)+int(processor_cost)

        return render_template('index_mobile.html', pred=pred, df_mobile=df_mobile, label=1)

    except:

        return render_template('index_mobile.html', label=0)


@app.route('/predict_bike', methods=['POST'])
def predict_bike():
    try:
        brand=request.form.get('brand')
        year=request.form.get('year')
        distance=request.form.get('kms')
        distance=distance.strip('kms')
        year=" "+year
        new=pd.DataFrame(columns=['distance', 'brand_Aprilia', 'brand_BMW', 'brand_Bajaj',
       'brand_Benelli', 'brand_Ducati', 'brand_Harley', 'brand_Hero',
       'brand_Honda', 'brand_Hyosung', 'brand_Jawa', 'brand_KTM',
       'brand_Kawasaki', 'brand_Kinetic', 'brand_LML', 'brand_Lambretta',
       'brand_Mahindra', 'brand_Royal', 'brand_Suzuki', 'brand_TVS',
       'brand_Triumph', 'brand_UM', 'brand_YO', 'brand_Yamaha',
       'brand_Yezdi', 'year_ 1996', 'year_ 1997', 'year_ 1998',
       'year_ 1999', 'year_ 2000', 'year_ 2001', 'year_ 2002',
       'year_ 2003', 'year_ 2004', 'year_ 2005', 'year_ 2006',
       'year_ 2007', 'year_ 2008', 'year_ 2009', 'year_ 2010',
       'year_ 2011', 'year_ 2012', 'year_ 2013', 'year_ 2014',
       'year_ 2015', 'year_ 2016', 'year_ 2017', 'year_ 2018',
       'year_ 2019', 'year_ Before 1995'])

        d = {'brand': brand, 'year': year, 'distance': distance}
        data = pd.DataFrame(d, index=[1])
        F = pd.get_dummies(data, columns=['brand', 'year'])
        new[F.columns.values] = F[F.columns.values]
        new = new.replace(np.nan, 0)
        x = new.iloc[:, :].values
        pred = round(clf_bike.predict(x)[0], 2)

        return render_template('index_bike.html', pred=pred, label=1)

    except:

        return render_template('index_bike.html', label=0)



if __name__ =="__main__":
    app.run(debug=True)