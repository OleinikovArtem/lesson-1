import json


class Calculator:
    def __init__(self):
        # create self.readings = []
        self.load_readings_from_file()

    def save_to_file(self):
        with open('meter_readings.json', 'w') as file:
            json.dump(self.readings, file)

    def load_readings_from_file(self):
        try:
            with open('meter_readings.json', 'r') as file:
                self.readings = json.load(file)
        except FileNotFoundError:
            self.readings = []

    def get_bill_by_date(self, month: int, year: int):
        bill = {
            'month_price': self.calculate_price_by_date(month, year),
            'month': month,
            'year': year
        }

        return bill

    def add_readings(self, day: int, night: int, month: int, year: int):
        self.readings.append({'day': day, 'night': night, 'month': month, 'year': year})
        self.save_to_file()

        return self.get_bill_by_date(month, year)

    def calculate_readings_margin(self, previous_day: int, previous_night: int, day: int, night: int):
        margin_day = day - previous_day
        margin_night = night - previous_night
        return {'day': margin_day, 'night': margin_night}

    def get_readings_by_date(self, month: int, year: int):
        current_reading = None
        previous_reading = None

        previous_month = 12 if month == 1 else month - 1
        previous_year = year - 1 if month == 1 else year

        for reading in self.readings:
            if reading['month'] == month and reading['year'] == year:
                current_reading = reading
            elif reading['month'] == previous_month and reading['year'] == previous_year:
                previous_reading = reading

        return {'current_reading': current_reading, 'previous_reading': previous_reading}

    def calculate_price(self, day: int, night: int):
        price = 2.64
        nightPrice = price / 2

        return (day * price) + (night * nightPrice)

    def calculate_price_by_date(self, month: int, year: int):
        readings = self.get_readings_by_date(month, year)
        current_reading = readings['current_reading']
        previous_reading = readings['previous_reading']

        if not current_reading or not previous_reading:
            return f'Readings for the month/year {month}/{year} not found!'

        margin = self.calculate_readings_margin(previous_reading['day'], previous_reading['night'],
                                                current_reading['day'], current_reading['night'])

        return self.calculate_price(margin['day'], margin['night'])


# calculator = Calculator()

# month = int(input('Enter month:'))
# year = int(input('Enter year:'))

# day = int(input('Enter day readings:'))
# night = int(input('Enter night readings:'))

# bill = calculator.add_readings(day, night, month, year)


# bill = calculator.get_bill_by_date(month, year)
# print(bill)
