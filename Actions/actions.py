# This files contains your custom actions which can be used to run
# custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from fpdf import FPDF
import os
import texttable
from http.client import responses
from typing import Any, Text, Dict, List
from urllib import response
from matplotlib.pyplot import text
from rauth.service import OAuth1Service
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from fatsecret import Fatsecret
from pandas import pandas as pd
from prettytable import PrettyTable
from tabulate import tabulate
from sanic_jwt import Responses
from typing import Any, Text, Dict, List, Tuple
from rasa_sdk.events import EventType, AllSlotsReset
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import FormAction

class AskFornameAction(Action):
    def name(self) -> Text:
        return "action_name"
    
    def required_slots(tracker):
       # type: () -> List[Text]
       """A list of required slots that the form has to fill"""

       return ["name"]

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        name = str(tracker.get_slot('name'))
        dispatcher.utter_message(text = name) 
        return []

    

class waterIntakeAction(Action):
    def name(self) -> Text:
        return "waterintake_action"
    
    def required_slots(tracker):
       # type: () -> List[Text]
       """A list of required slots that the form has to fill"""

       return ["weight","age"]

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        weight = float(tracker.get_slot('weight'))
        age = float(tracker.get_slot('age'))

        if age < 30:
            water_calc = weight * 40
        elif age >=30 and age <=55:
            water_calc = weight * 35
        else:
            water_calc = weight * 30

        water = round(((water_calc / 28.3) * 0.0295735))
        dispatcher.utter_message("You need to drink {} litres of water daily" .format(water))
        dispatcher.utter_message(f"Do you want to Chat again??")
        return[AllSlotsReset()]

class Actionfooddetail(Action):

    def name(self) -> Text:
        return "action_food_detail"

    def required_slots(tracker):
       # type: () -> List[Text]
       return ["foodname"]


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            consumer_key = ''
            consumer_secret = ''
            fs = Fatsecret(consumer_key, consumer_secret)
            foodname = tracker.get_slot('foodname')
            foods = fs.foods_search(foodname)
            df_food = pd.DataFrame(foods)
            df_food['food_description'].str.split('|', expand=True)
            df=df_food['food_description']
            df_split=df.str.split('|', expand=True)
            df1=df_split[0].str.split('-', expand=True)
            df2=df_split.drop([0] , axis=1)
            df3=df_food['food_name']
            data=df1.join(df2, lsuffix="_left", rsuffix="_right")
            food = data.join(df3)
            food_data=food.rename(columns={0: "quantity", "1_left": "Calories", "1_right": "Fat", 2 : "Carbs", 3 : "Protein"})
            food_data_unique= food_data.drop_duplicates(subset ="food_name")
            # unique_data = food_data_unique.quantity.unique()
            # dispatcher.utter_message(food_data_unique.to_string())
            dispatcher.utter_message(food_data_unique.to_string())
            dispatcher.utter_message(f"Do you want to Chat again?")
            return[AllSlotsReset()]



class ActionBMI(Action):

    global height
    global weight

    def name(self) -> Text:
        return "calculate_BMI"

    def required_slots(tracker):
       # type: () -> List[Text]
       """A list of required slots that the form has to fill"""

       return ["height","weight"]


    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) ->List[Dict[Text, Any]]:    

            height = float(tracker.get_slot('height'))
            weight = float(tracker.get_slot('weight'))

            bmi =  weight/((height/100)**2)
            if bmi <= 18.5:
                bmi_result = "Oops! You are underweight."
            elif bmi <= 24.9:
                bmi_result = "Awesome! You are healthy."
            elif bmi <= 29.9:
                bmi_result = "Eee! You are overweight."
            else:
                bmi_result = "Seesh! You are obese."
            dispatcher.utter_message("Your BMI is {}, Result : = {}  ".format(bmi,bmi_result))
            dispatcher.utter_message("Do you want to Chat again? ")
            return[AllSlotsReset()]
               

class ActionBMR(Action):

    global height
    global weight

    def name(self) -> Text:
        return "calculate_BMR"

    def required_slots(tracker):
       # type: () -> List[Text]
       """A list of required slots that the form has to fill"""

       return ["height","weight","gender","age"]

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) ->List[Dict[Text, Any]]:    

            height = tracker.get_slot('height')
            weight = tracker.get_slot('weight')
            age    = tracker.get_slot('age')
            h = float(height)
            w = float(weight)
            a = float(age)
            gender = tracker.get_slot('gender')
            gender = gender.lower() 
            bmi    =  w/((h/100)**2)

            if gender == 'male' or gender == 'm':
                    bmr =88.362 + (13.397 * w) + (4.799 * h) - (5.677 * a)
            elif gender == 'female' or gender == 'f':
                    bmr = 447.593 + (9.247 * w) + (3.098 * h) - (4.330 * a)
            else:
                    print('Invalid gender')

# print('Your BMR is : ',bmr)

            bodyfat = (1.20 * bmi) + (0.23 * a)
            # print("Your body fat percentage is : ",bodyfat)

            # if bmi <= 18.5:
            #     bmi_result = "Oops! You are underweight."
            # elif bmi <= 24.9:
            #     bmi_result = "Awesome! You are healthy."
            # elif bmi <= 29.9:
            #     bmi_result = "Eee! You are overweight."
            # else:
            #     bmi_result = "Seesh! You are obese."
            dispatcher.utter_message("Your BMR is  {} calories/day and body fat percentage is {} . ".format(bmr,bodyfat))
            dispatcher.utter_message("Do you want to Chat again? ")
            return[AllSlotsReset()]

class Actiondiet_chart(Action):

    global height
    global weight

    def name(self) -> Text:
        return "diet_chart_formation"

    def required_slots(tracker):
       # type: () -> List[Text]
       """A list of required slots that the form has to fill"""

       return ["height","weight","age","gender","pftype","level"]


    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) ->List[Dict[Text, Any]]:    

            height = float(tracker.get_slot('height'))
            weight = float(tracker.get_slot('weight'))
            age    = tracker.get_slot('age')
            gender = tracker.get_slot('gender')
            foodtype = tracker.get_slot('ftype')
            pftype=  tracker.get_slot('pftype')
            plevel = tracker.get_slot('plevel')
            gender= gender.lower()
            h = float(height)
            w = float(weight)
            a = float(age)


            bmi =  weight/((height/100)**2)
            if bmi <= 18.5:
                bmi_resultd = "Oops! You are underweight!! So you need to gain the weight and according to that your diet plan is as follows."
            elif bmi <= 24.9:
                bmi_resultd = "Awesome! You are healthy.To reamin healthy just follow the diet chart"
            elif bmi <= 29.9:
                bmi_resultd = "Eee! You are overweight. So you need to lose the weight and according to that your diet plan is as follows"
            else:
                bmi_resultd = "Seesh! You are obese. So you need to lose the weight and according to that your diet plan is as follows"

            if gender == 'male' or gender == 'm':
                bmr = 88.362 + (13.397 * w) + (4.799 * h) - (5.677 * a)
            elif gender == 'female' or gender == 'f':
                bmr = 447.593 + (9.247 * w) + (3.098 * h) - (4.330 * a)
            else:
                bmr = f"I assume that you have not entered the gender field properly!!!"
            

            pftype = pftype
            plevel =plevel
            add_sub_cal = 0
            bmr = bmr
            target_cal =0
            
            if plevel == 'easy' and bmi_resultd == "Oops! You are underweight!! So you need to gain the weight and according to that your diet plan is as follows.":
                add_sub_cal = 100
            elif plevel == "medium" and bmi_resultd== "Oops! You are underweight!! So you need to gain the weight and according to that your diet plan is as follows.":
                add_sub_cal = 200
            elif plevel == "hard" and bmi_resultd == "Oops! You are underweight!! So you need to gain the weight and according to that your diet plan is as follows.":
                add_sub_cal = 300
            elif plevel == "easy" and bmi_resultd == "Eee! You are overweight. So you need to lose the weight and according to that your diet plan is as follows":
                add_sub_cal = -100
            elif plevel == "medium" and bmi_resultd == "Eee! You are overweight. So you need to lose the weight and according to that your diet plan is as follows":
                add_sub_cal = -200
            elif plevel == "hard" and bmi_resultd == "Eee! You are overweight. So you need to lose the weight and according to that your diet plan is as follows":
                add_sub_cal = -300
            elif plevel == "easy" and bmi_resultd == "Seesh! You are obese. So you need to lose the weight and according to that your diet plan is as follows":
                add_sub_cal = -100
            elif plevel == "medium" and bmi_resultd== "Seesh! You are obese. So you need to lose the weight and according to that your diet plan is as follows":
                add_sub_cal = -200
            elif plevel == "hard" and bmi_resultd == "Seesh! You are obese. So you need to lose the weight and according to that your diet plan is as follows":
                add_sub_cal = -300
            else:
                add_sub_cal = 0

            if pftype == '1':
                target_cal = bmr*1.2
            elif pftype == '2':
                target_cal = bmr*1.375
            elif pftype == '3':
                target_cal = bmr*1.55
            elif pftype == '4':
                target_cal = bmr*1.725
            elif pftype == '5':
                target_cal = bmr*1.9

            target_cal = target_cal + add_sub_cal  

            if foodtype == 'non-veg':
                df = pd.read_csv('./static/veg_nonveg.csv')     
            else:
                df = pd.read_csv('./static/veg.csv')
        
            df_20 = df.sample(n=50)
            df_20_list = list(zip(df_20['food_name'],df_20['calories']))
            morning_cal = target_cal*0.25
            lunch_cal = target_cal*0.35
            dinner_cal = target_cal*0.40
            morning_cal_consumed = 0
            lunch_cal_consumed = 0
            dinner_cal_consumed = 0
            total_calory_consumed = 0

            morning_list = [["Food Item","Calories"]]
            lunch_list = [["Food Item","Calories"]]
            dinner_list = [["Food Item","Calories"]]
            while morning_cal>0:
                if morning_cal-df_20_list[0][1] < 0:
                    need_gms = round((100*morning_cal)/df_20_list[0][1],2)
                    morning_cal_consumed = morning_cal_consumed + morning_cal
                    total_calory_consumed = total_calory_consumed + morning_cal
                    morning_list.append((str(need_gms) +' gms '+ df_20_list[0][0] ,str(int(morning_cal))))
                    df_20_list.pop(0)
                    break
                else:
                    morning_cal = morning_cal - df_20_list[0][1]
                    morning_cal_consumed = morning_cal_consumed + df_20_list[0][1]
                    total_calory_consumed = total_calory_consumed + df_20_list[0][1]
                    # morning_list.append(df_20_list.pop(0))
                    xyz = df_20_list.pop(0)
                    morning_list.append((xyz[0],str(xyz[1])))
                    


            while lunch_cal>0:
                if lunch_cal-df_20_list[0][1] < 0:
                    need_gms = round((100*lunch_cal)/df_20_list[0][1],2)
                    lunch_cal_consumed = lunch_cal_consumed + lunch_cal
                    total_calory_consumed = total_calory_consumed + lunch_cal
                    lunch_list.append((str(need_gms) +' gms '+ df_20_list[0][0] ,str(int(lunch_cal))))
                    df_20_list.pop(0)
                    break        
                else:
                    lunch_cal = lunch_cal - df_20_list[0][1] 
                    lunch_cal_consumed = lunch_cal_consumed + df_20_list[0][1]
                    total_calory_consumed = total_calory_consumed + df_20_list[0][1]
                    # lunch_list.append(df_20_list.pop(0))
                    xyz = df_20_list.pop(0)
                    lunch_list.append((xyz[0],str(xyz[1])))

            while dinner_cal>0:
                if dinner_cal-df_20_list[0][1] < 0:
                    need_gms = round((100*dinner_cal)/df_20_list[0][1],2)
                    dinner_cal_consumed = dinner_cal_consumed + dinner_cal
                    total_calory_consumed = total_calory_consumed + dinner_cal
                    dinner_list.append((str(need_gms) +' gms '+ df_20_list[0][0] ,str(int(dinner_cal))))
                    df_20_list.pop(0)
                    break        
                else:
                    dinner_cal = dinner_cal - df_20_list[0][1]
                    dinner_cal_consumed = dinner_cal_consumed + df_20_list[0][1]
                    total_calory_consumed = total_calory_consumed + df_20_list[0][1]
                    # dinner_list.append(df_20_list.pop(0))
                    xyz = df_20_list.pop(0)
                    dinner_list.append((xyz[0],str(xyz[1])))
            
            dispatcher.utter_message(bmi_resultd)
            

            def create_table(table_data, title='', data_size = 10, title_size=14, align_data='L', align_header='L', cell_width='even', x_start='x_default',emphasize_data=[], emphasize_style=None, emphasize_color=(0,0,0)):
                """
                table_data: 
                            list of lists with first element being list of headers
                title: 
                            (Optional) title of table (optional)
                data_size: 
                            the font size of table data
                title_size: 
                            the font size fo the title of the table
                align_data: 
                            align table data
                            L = left align
                            C = center align
                            R = right align
                align_header: 
                            align table data
                            L = left align
                            C = center align
                            R = right align
                cell_width: 
                            even: evenly distribute cell/column width
                            uneven: base cell size on lenght of cell/column items
                            int: int value for width of each cell/column
                            list of ints: list equal to number of columns with the widht of each cell / column
                x_start: 
                            where the left edge of table should start
                emphasize_data:  
                            which data elements are to be emphasized - pass as list 
                            emphasize_style: the font style you want emphaized data to take
                            emphasize_color: emphasize color (if other than black) 
                
                """
                default_style = pdf.font_style
                if emphasize_style == None:
                    emphasize_style = default_style
                # default_font = pdf.font_family
                # default_size = pdf.font_size_pt
                # default_style = pdf.font_style
                # default_color = pdf.color # This does not work

                # Get Width of Columns
                def get_col_widths():
                    col_width = cell_width
                    if col_width == 'even':
                        col_width = pdf.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
                    elif col_width == 'uneven':
                        col_widths = []

                        # searching through columns for largest sized cell (not rows but cols)
                        for col in range(len(table_data[0])): # for every row
                            longest = 0 
                            for row in range(len(table_data)):
                                cell_value = str(table_data[row][col])
                                value_length = pdf.get_string_width(cell_value)
                                if value_length > longest:
                                    longest = value_length
                            col_widths.append(longest + 4) # add 4 for padding
                        col_width = col_widths



                                ### compare columns 

                    elif isinstance(cell_width, list):
                        col_width = cell_width  # TODO: convert all items in list to int        
                    else:
                        # TODO: Add try catch
                        col_width = int(col_width)
                    return col_width

                # Convert dict to lol
                # Why? because i built it with lol first and added dict func after
                # Is there performance differences?
                if isinstance(table_data, dict):
                    header = [key for key in table_data]
                    data = []
                    for key in table_data:
                        value = table_data[key]
                        data.append(value)
                    # need to zip so data is in correct format (first, second, third --> not first, first, first)
                    data = [list(a) for a in zip(*data)]

                else:
                    header = table_data[0]
                    data = table_data[1:]

                line_height = pdf.font_size * 2.5

                col_width = get_col_widths()
                pdf.set_font(size=title_size)

                # Get starting position of x
                # Determin width of table to get x starting point for centred table
                if x_start == 'C':
                    table_width = 0
                    if isinstance(col_width, list):
                        for width in col_width:
                            table_width += width
                    else: # need to multiply cell width by number of cells to get table width 
                        table_width = col_width * len(table_data[0])
                    # Get x start by subtracting table width from pdf width and divide by 2 (margins)
                    margin_width = pdf.w - table_width
                    # TODO: Check if table_width is larger than pdf width

                    center_table = margin_width / 2 # only want width of left margin not both
                    x_start = center_table
                    pdf.set_x(x_start)
                elif isinstance(x_start, int):
                    pdf.set_x(x_start)
                elif x_start == 'x_default':
                    x_start = pdf.set_x(pdf.l_margin)


                # TABLE CREATION #

                # add title
                if title != '':
                    pdf.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=pdf.font_size)
                    pdf.ln(line_height) # move cursor back to the left margin

                pdf.set_font(size=data_size)
                # add header
                y1 = pdf.get_y()
                if x_start:
                    x_left = x_start
                else:
                    x_left = pdf.get_x()
                x_right = pdf.epw + x_left
                if  not isinstance(col_width, list):
                    if x_start:
                        pdf.set_x(x_start)
                    for datum in header:
                        pdf.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3, max_line_height=pdf.font_size)
                        x_right = pdf.get_x()
                    pdf.ln(line_height) # move cursor back to the left margin
                    y2 = pdf.get_y()
                    pdf.line(x_left,y1,x_right,y1)
                    pdf.line(x_left,y2,x_right,y2)

                    for row in data:
                        if x_start: # not sure if I need this
                            pdf.set_x(x_start)
                        for datum in row:
                            if datum in emphasize_data:
                                pdf.set_text_color(*emphasize_color)
                                pdf.set_font(style=emphasize_style)
                                pdf.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=pdf.font_size)
                                pdf.set_text_color(0,0,0)
                                pdf.set_font(style=default_style)
                            else:
                                pdf.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=pdf.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
                        pdf.ln(line_height) # move cursor back to the left margin
                
                else:
                    if x_start:
                        pdf.set_x(x_start)
                    for i in range(len(header)):
                        datum = header[i]
                        pdf.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=pdf.font_size)
                        x_right = pdf.get_x()
                    pdf.ln(line_height) # move cursor back to the left margin
                    y2 = pdf.get_y()
                    pdf.line(x_left,y1,x_right,y1)
                    pdf.line(x_left,y2,x_right,y2)


                    for i in range(len(data)):
                        if x_start:
                            pdf.set_x(x_start)
                        row = data[i]
                        for i in range(len(row)):
                            datum = row[i]
                            if not isinstance(datum, str):
                                datum = str(datum)
                            adjusted_col_width = col_width[i]
                            if datum in emphasize_data:
                                pdf.set_text_color(*emphasize_color)
                                pdf.set_font(style=emphasize_style)
                                pdf.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=pdf.font_size)
                                pdf.set_text_color(0,0,0)
                                pdf.set_font(style=default_style)
                            else:
                                pdf.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=pdf.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
                        pdf.ln(line_height) # move cursor back to the left margin
                y3 = pdf.get_y()
                pdf.line(x_left,y3,x_right,y3)


            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Times", size=10)

            create_table(table_data = morning_list,title='Breakfast', cell_width='even')
            pdf.ln()

            create_table(table_data = lunch_list,title='Lunch', cell_width='even')
            pdf.ln()

            create_table(table_data = dinner_list,title='Dinner', cell_width='even')
            pdf.ln()





            # create_table(table_data = data_as_dict,align_header='R', align_data='R', cell_width=[15,15,10,45,], x_start='C') 


            pdf_name = "diet_plan.pdf"
            pdf.output("static/"+pdf_name)
            link = "static/"+pdf_name
            data = {
                "payload":"pdf_attachment",
                "title": "diet_plan",
                "url": link
                }
            dispatcher.utter_message(json_message=data) 

            dispatcher.utter_message(f"Do you want to Chat again?")      
            return[AllSlotsReset()]
                        
