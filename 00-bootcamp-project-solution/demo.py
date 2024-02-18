dbname = "greenery"
host = "localhost"
number = 1

my_string_1 = "dbname=" + dbname + " host=" + host + " number=" + str(number)
print(my_string_1)

my_string_2 = f"dbname={dbname} host={host} number={number}"
print(my_string_2)

