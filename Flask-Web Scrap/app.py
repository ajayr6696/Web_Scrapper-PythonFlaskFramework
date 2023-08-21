from flask import (
    Flask,
    render_template,
    request,
    Response,
    redirect,
    flash,
    url_for,
    current_app,
    session,
    request,
    jsonify
)
from flask_session import Session
import pandas as pd
import urllib.request 
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup
import requests,validators,uuid,pathlib,os
from html.parser import HTMLParser
import logging
import re
import flask_excel as excel
#import ftfy
#from flask.ext import excel

app = Flask(__name__)
sess = Session()
excel.init_excel(app)
#SESSION_TYPE = 'redis'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
Session(app)

current_tag = []
result = []
final_result=[]
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        current_tag.append(tag)

    def handle_endtag(self, tag):

        current_tag.reverse()
        current_tag.remove(tag)
        current_tag.reverse()

    def handle_data(self, data):
        if len(current_tag) > 0 :
            if current_tag[-1] != 'script' and current_tag[-1] != 'style':

                if(len(data)>2):
                    result.append(data)


@app.route("/",methods=("GET", "POST"), strict_slashes=False)
def index():
    if request.method == "POST":

        #try:
            global requested_url,final_result

            requested_url = request.form.get('urltext')
            

            source = requests.get(requested_url).text
            # parser library?
            soup = BeautifulSoup(source, "html.parser")
            
            parser = MyHTMLParser()
            parser.feed(str(soup))
            #final_result=[]
            title=''
            description=''
            weight=''
            highlights=''
            dimensions=''
            tcin=''
            upc=''
            dpci=''
            includes=''
            brand='' 
            for i in range(len(result)):
                result[i] = result[i].replace('“', '"')
                result[i] = result[i].replace('—', '-')
                if(result[i].endswith(": Target")):
                    title = result[i].split(' : Target')[0].strip()
                    title = title.replace('“', '"')
                    title = title.replace('—', '-')
                    title = title.replace('’', '\'')
                if(result[i]=='Shop all' or result[i]=='Shop all '):
                    i=i+1
                    brand=result[i].strip()
                if(result[i]=='Highlights' or result[i]=='Fit & style'):
                    i=i+1
                    highlights=''
                    while result[i]!='Specifications':
                        highlights = (highlights + ' ' + result[i]).strip()
                        i=i+1
                    highlights = highlights.replace('“', '"')
                    highlights = highlights.replace('—', '-')
                if(result[i]=='Dimensions (Overall):'):
                    i=i+1
                    dimensions=result[i].strip()
                if(result[i]=='Weight:'):
                    i=i+1
                    weight=result[i].strip()
                if(result[i]=='TCIN'):
                    i=i+1
                    tcin=result[i].strip()
                if(result[i]=='UPC'):
                    i=i+1
                    upc=result[i].strip()
                if(result[i]=='Item Number (DPCI)'):
                    i=i+1
                    dpci=result[i].strip()
                if(result[i]=='Description'):
                    i=i+1
                    description=''
                    while result[i]!='If the item details above aren’t accurate or complete, we want to know about it.':
                        description = (description + ' ' + result[i]).strip()
                        i=i+1
                    description = description.replace('“', '"')
                    description = description.replace('—', '-')
                    print(description)
                if(result[i]=='Includes:'):
                    if i > result.index("Specifications") and i < result.index("Description"):
                        i=i+1
                        includes=result[i].strip()

            #D='Title,' + 'Short Description,'+'Long Description:,'+'Product Dimension:,'+'Weight:,'+'TCIN:,'+'UPC:,'+'Item Number (DPCI):,'+'What\'s in the Box:,\n'+title+','+highlights+','+description+','+dimensions+','+weight+','+tcin+','+upc+','+dpci+','+includes
            #data = pd.DataFrame({'Title':[title], 'Short Description:':[highlights], 'Long Description:':[description], 'Product Dimension:':[dimensions], 'Weight:':[weight], 'TCIN:':[tcin], 'UPC:':[upc], 'Item Number (DPCI):':[dpci], 'What\'s in the Box:':[includes] })
            final_result.append('Title:')
            final_result.append(title)
            final_result.append('Short Description:')
            final_result.append(highlights)
            final_result.append('Long Description:')
            final_result.append(description)
            final_result.append('Product Dimension:')
            final_result.append(dimensions)
            final_result.append('Weight:')
            final_result.append(weight)
            final_result.append('TCIN:')
            final_result.append(tcin)
            final_result.append('UPC:')
            final_result.append(upc)
            final_result.append('Item Number (DPCI):')
            final_result.append(dpci)
            final_result.append('What\'s in the Box:')
            final_result.append(includes)
            final_result.append('Brand:')
            final_result.append(brand)
            if not session.get('res'):
                session['res']=[['','',title,highlights,brand,upc,'','',description,'','','','','','','','','','','','','','','','','','','','','','','','','',dimensions,'','',includes,'','','','','','','','','','','','','','','','','','',weight]]
            else:
                a=session.get('res')
                a.append(['','',title,highlights,brand,upc,'','',description,'','','','','','','','','','','','','','','','','','','','','','','','','',dimensions,'','',includes,'','','','','','','','','','','','','','','','','','',weight])
                session['res']=a
            return render_template("index.html",
                url = requested_url,
                results = final_result
                )

        #except Exception as e:
            #flash(e, "danger")
    else: 
        session.pop('res',None)
    return render_template("index.html")


@app.route("/get_csv/", methods=['GET'])
def download_file():
    a=[['Category Code','Shop sku','Title BB(EN)','Short Description BB (EN)','Brand Name','Primary UPC','Model Number','Manufacturer\'s Part Number','Long Description BB (EN)','01 - Image Source (Main Image)','02 - Image Source (Main Image)','03 - Image Source (Main Image)','04 - Image Source (Main Image)','05 - Image Source (Main Image)','06 - Image Source (Main Image)','07 - Image Source (Main Image)','08 - Image Source (Main Image)','09 - Image Source (Main Image)','10 - Image Source (Main Image)','Refurbished','Open Box','Title BB (FR)','Short Description BB (FR)','Long Description BB (FR)','Web Hierarchy Location','French Compliant','ESRB','Software Platform','Energy Star Indicator','Variant Group Code','Collection/Series (EN)','Collection/Series (FR)','Oven Capacity (Cu. Ft.)','Colour Family','Width (Inches)','Height (Inches)','Depth (Inches)','What\'s in the Box (EN)','What\'s in the Box (FR)','Filter','Turntable Type (EN)','Quick On Option','Turntable Diameter (Inches)','Turntable Type (FR)','Child Lock','Power Levels','Control Panel Type (EN)','Control Panel Type (FR)','Auto Cook','Auto Reheat','Auto Defrost','Sensor Cook','Sensor Reheat','Sensor Defrost','Cooking Program Stages','Convection Functions','Kitchen Timer','Depth','Display Language Option (EN)','Display Language Option (FR)','Display Screen Readout (EN)','Display Screen Readout (FR)','Two Level Cooking','Door Opening Type (EN)','Door Opening Type (FR)','Custom Cook','Help Function','Maximum Setting Time (EN)','Maximum Setting Time (FR)','More/Less Function','One-Touch Functions','Recessed Turntable','Colour (EN)','Colour (FR)','Cooking System (EN)','Cooking System (FR)','Keep Warm Feature','Weight','Cavity Dimensions (EN)','Cavity Dimensions (FR)','Maximum Time Setting (EN)','Maximum Time Setting (FR)','Adjustable Power Level','Fan Speeds','Height','Hood Light Settings','Control Panel (EN)','Control Panel (FR)','Digital Display','Vents (EN)','Vents (FR)','Power Requirement','Wattage','Defrost by Time','Defrost by Weight','Clock','Adjustable Cook Time','Reminder Alarm','Moisture Sensor','Bake Function','Broil Function','Microwave Function','Interior Light','Mounting Kit Included','Turntable On/Off','Venting System','Popcorn','Potato','Pizza','Frozen Food','Beverage','Seafood','Ground Meat','Soup','Programmable Favourite','Colour (Cabinet/Door) (EN)','Colour (Cabinet/Door) (FR)','Country of Origin (EN)','Country of Origin (FR)','Microwave Style','Wi-Fi Connectivity','Width','Fryer Type','Maximum Air Flow Capacity','Offer SKU','Product ID','Product ID Type','Offer Description','Offer Internal Description','Offer Price','Offer Price Additional Info','Offer Quantity','Minimum Quantity Alert','Offer State','Availability Start Date','Availability End Date','Logistic Class','Discount Price','Discount Start Date','Discount End Date','Update/Delete','Warranty - Parts & Labour','EHF Amount for Alberta','EHF Amount for British Columbia','EHF Amount for Manitoba','EHF Amount for New Brunswick','EHF Amount for Newfoundland and Labrador','EHF Amount for Nova Scotia','EHF Amount for Northwest Territorities','EHF Amount for Nunavut','EHF Amount for Ontario','EHF Amount for Prince Edward Island','EHF Amount for Quebec','EHF Amount for Saskatchewan','EHF Amount for Yukon','Sales Tax Code'],['BBYCat','shop_sku','_Title_BB_Category_Root_EN','_Short_Description_BB_Category_Root_EN','_Brand_Name_Category_Root_EN','_Primary_UPC_Category_Root_EN','_Model_Number_Category_Root_EN','_Manufacturers_Part_Number_Category_Root_EN','_Long_Description_BB_Category_Root_EN','_MP_Source_Image_URL_01_Category_Root_EN','_MP_Source_Image_URL_02_Category_Root_EN','_MP_Source_Image_URL_03_Category_Root_EN','_MP_Source_Image_URL_04_Category_Root_EN','_MP_Source_Image_URL_05_Category_Root_EN','_MP_Source_Image_URL_06_Category_Root_EN','_MP_Source_Image_URL_07_Category_Root_EN','_MP_Source_Image_URL_08_Category_Root_EN','_MP_Source_Image_URL_09_Category_Root_EN','_MP_Source_Image_URL_10_Category_Root_EN','_Refurbished_Category_Root_EN','_OpenBox_805497_Category_Root_EN','_Title_BB_Category_Root_FR','_Short_Description_BB_Category_Root_FR','_Long_Description_BB_Category_Root_FR','_Web_Hierarchy_Location_Category_Root_EN','_French_Compliant_Category_Root_EN','_ESRB_Category_Root_EN','_Software_Platform_Category_Root_EN','_Energy_Star_Indicator_Category_Root_EN','Variant_Group_Code','_CollectionSeries_27223_CAT_27115_EN','_CollectionSeries_27223_CAT_27115_FR','_OvenCapacityCuFt_5824_CAT_27136_EN','_ColourFamily_688021_CAT_27136_EN','_WidthInches_25132_CAT_27136_EN','_HeightInches_25131_CAT_27136_EN','_DepthInches_25133_CAT_27136_EN','_WhatsintheBox_4667_CAT_27136_EN','_WhatsintheBox_4667_CAT_27136_FR','_Filter_5175_CAT_27136_EN','_TurntableType_5846_CAT_27136_EN','_QuickOnOption_5841_CAT_27136_EN','_TurntableDiameterInches_5845_CAT_27136_EN','_TurntableType_5846_CAT_27136_FR','_ChildLock_5840_CAT_27136_EN','_PowerLevels_5825_CAT_27136_EN','_ControlPanelType_5826_CAT_27136_EN','_ControlPanelType_5826_CAT_27136_FR','_AutoCook_5827_CAT_27136_EN','_AutoReheat_5828_CAT_27136_EN','_AutoDefrost_5829_CAT_27136_EN','_SensorCook_5830_CAT_27136_EN','_SensorReheat_5831_CAT_27136_EN','_SensorDefrost_5832_CAT_27136_EN','_CookingProgramStages_5833_CAT_27136_EN','_ConvectionFunctions_5834_CAT_27136_EN','_KitchenTimer_5835_CAT_27136_EN','_Depth_14236_CAT_27136_EN','_DisplayLanguageOption_5836_CAT_27136_EN','_DisplayLanguageOption_5836_CAT_27136_FR','_DisplayScreenReadout_5837_CAT_27136_EN','_DisplayScreenReadout_5837_CAT_27136_FR','_TwoLevelCooking_5838_CAT_27136_EN','_DoorOpeningType_5839_CAT_27136_EN','_DoorOpeningType_5839_CAT_27136_FR','_CustomCook_9183_CAT_27136_EN','_HelpFunction_9184_CAT_27136_EN','_MaximumSettingTime_9186_CAT_27136_EN','_MaximumSettingTime_9186_CAT_27136_FR','_MoreLessFunction_9187_CAT_27136_EN','_OneTouchFunctions_9188_CAT_27136_EN','_RecessedTurntable_9207_CAT_27136_EN','_Colour_5105_CAT_27136_EN','_Colour_5105_CAT_27136_FR','_CookingSystem_8586_CAT_27136_EN','_CookingSystem_8586_CAT_27136_FR','_KeepWarmFeature_5222_CAT_27136_EN','_Weight_5302_CAT_27136_EN','_CavityDimensions_9191_CAT_27136_EN','_CavityDimensions_9191_CAT_27136_FR','_MaximumTimeSetting_9196_CAT_27136_EN','_MaximumTimeSetting_9196_CAT_27136_FR','_AdjustablePowerLevel_689353_CAT_27136_EN','_FanSpeeds_8256_CAT_27136_EN','_Height_15404_CAT_27136_EN','_HoodLightSettings_9178_CAT_27136_EN','_ControlPanel_9154_CAT_27136_EN','_ControlPanel_9154_CAT_27136_FR','_DigitalDisplay_689283_CAT_27136_EN','_Vents_9206_CAT_27136_EN','_Vents_9206_CAT_27136_FR','_PowerRequirement_8268_CAT_27136_EN','_Wattage_5127_CAT_27136_EN','_DefrostbyTime_689372_CAT_27136_EN','_DefrostbyWeight_689373_CAT_27136_EN','_Clock_15545_CAT_27136_EN','_AdjustableCookTime_689354_CAT_27136_EN','_ReminderAlarm_689355_CAT_27136_EN','_MoistureSensor_8653_CAT_27136_EN','_BakeFunction_689404_CAT_27136_EN','_BroilFunction_689356_CAT_27136_EN','_MicrowaveFunction_689358_CAT_27136_EN','_InteriorLight_8516_CAT_27136_EN','_MountingKitIncluded_9198_CAT_27136_EN','_TurntableOnOff_9204_CAT_27136_EN','_VentingSystem_9205_CAT_27136_EN','_Popcorn_689406_CAT_27136_EN','_Potato_689360_CAT_27136_EN','_Pizza_689361_CAT_27136_EN','_FrozenFood_689362_CAT_27136_EN','_Beverage_689363_CAT_27136_EN','_Seafood_689364_CAT_27136_EN','_GroundMeat_689412_CAT_27136_EN','_Soup_689413_CAT_27136_EN','_ProgrammableFavourite_689367_CAT_27136_EN','_ColourCabinetDoor_9169_CAT_27136_EN','_ColourCabinetDoor_9169_CAT_27136_FR','_CountryofOrigin_26726_CAT_27136_EN','_CountryofOrigin_26726_CAT_27136_FR','_MicrowaveStyle_10851178_CAT_27136_EN','_WiFiConnectivity_13385868_CAT_27136_EN','_Width_6823_CAT_27136_EN','_FryerType_689324_CAT_27136_EN','_MaximumAirFlowCapacity_27576_CAT_27136_EN','sku','product-id','product-id-type','description','internal-description','price','price-additional-info','quantity','min-quantity-alert','state','available-start-date','available-end-date','logistic-class','discount-price','discount-start-date','discount-end-date','update-delete','manufacturer-warranty','ehf-amount-ab','ehf-amount-bc','ehf-amount-mb','ehf-amount-nb','ehf-amount-nl','ehf-amount-ns','ehf-amount-nt','ehf-amount-nu','ehf-amount-on','ehf-amount-pe','ehf-amount-qc','ehf-amount-sk','ehf-amount-yt','pim']]
    b=session.get('res')
    for i in b:
        a.append(i)
    return excel.make_response_from_array(a, "csv")
    session.clear()
if __name__ == "__main__":
    #app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.run(debug=True,host='0.0.0.0')
