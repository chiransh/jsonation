# jsonation

To transform the JSON input, we have to adhere to some rules based on the data type criteria.

To perform the transformation:

First, we have to sanitize the JSON input by removing leading/trailing whitespaces and the empty keys from the input JSON
Next, we need to loop over the sanitized JSON object and transform the values as per the data type.
If the value doesn't fit the data type criteria, we will omit that field.
For the "L" (list) data type, we will loop over the elements and transform each item based on the data type criteria. If any item doesn't fit the data type, we will omit that field.

For the "M" (map) data type, we will iterate over the map items and follow the transformation criteria for the values in the map. After that, we will sort the map items based on the keys.

Finally, we will output the transformed JSON object to stdout.

# This implementation defines few helper functions:

sanitize_string: takes a string argument and returns a sanitized version of the string with leading and trailing whitespace removed.
load_input_data: This method reads in the JSON file specified by input_path and returns its contents as a Python dictionary. If the JSON is malformed or cannot be read, it returns None.

transform_string: This method takes a value val and attempts to transform it into a Unix epoch timestamp. If val is not a valid string representation of a date and time, it returns the original string value. If val is None or an empty string, it returns None.

transform_numeric: This attempts to transform it into a numeric value. If val is not a valid numeric string, it returns None. If val is None or an empty string, it returns None.

transform_bool: This attempts to transform it into a boolean value (True or False). If val is not a valid boolean string, it returns None. If val is None or an empty string, it returns None.

transform_null: This attempts to transform it into a null value ('null'). If val is not a valid null string, it returns None. If val is None or an empty string, it returns None.

transform_value: This recursively transforms it based on its type. If val is a list, it transforms each element in the list and returns a new list containing the transformed elements (if any). If val is a dictionary, it recursively transforms each key-value pair in the dictionary and returns a new dictionary containing the transformed key-value pairs (if any). If val is not one of these types, it returns None.



# Usage -
To use the JsonTransformer class, you can create an instance of the class by specifying the input data file path as an argument.
input_path = 'sample1.json'

JsonTransformer(input_path).transform()


# Installation - 
To use this code, you must have Python 3 installed on your system. You will also need to install the dateutil library, which can be installed using pip
