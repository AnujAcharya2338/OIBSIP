from config import API_KEY


def get_city():
    while True:
            try:
                city_name = input("Enter the city's name:")
                city = city_name.strip()

                if not city:
                     print("Please enter the city's name:")
                     continue
                return city
                
            except EOFError:
                print("Please enter the name of a city.")

city = get_city()
print(city)
