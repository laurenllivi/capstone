from homepage import models as hmod

def convert_db_into_date_string(date_object_list):
    '''converts a list of date objects from the database into a string list of dates
    to be displayed on a page'''
    
    dates_list_string = ""
    first = True
    # convert the list of available date objects into a string to display in the text field
    for date in date_object_list:
        # convert the date into the format we want to display
        display_format_year = str(date.date).split("-")[0]
        display_format_month = str(date.date).split("-")[1]
        display_format_day = str(date.date).split("-")[2]
        
        if first:
            dates_list_string = dates_list_string + display_format_month + "/" + display_format_day + "/" + display_format_year
            first = False
        else:
            dates_list_string = dates_list_string + ", " + display_format_month + "/" + display_format_day + "/" + display_format_year
        
    return dates_list_string
    
def convert_date_string_into_db(date_string):
    '''converts a string (containing a date formatted in mm/dd/yyyy) to
    the recognizable database datetime format (yyyy-mm-dd)'''
    
    # first rearrange the date to meet the datetime object python format
    db_format_year = date_string.split("/")[2]
    db_format_month = date_string.split("/")[0]
    db_format_day = date_string.split("/")[1]
    db_format_date = db_format_year + "-" + db_format_month + "-" + db_format_day
    
    return db_format_date
    
    
    