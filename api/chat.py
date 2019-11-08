from tracker.util.chat import Chat

class Welcome(Chat):
    text = 'Hello, what\'s your name?'

    set_answer_to_session = 'customer_name'

    direct_to = 'Company'


class Company(Chat):
    text = 'Hi {customer_name}, what\'s the name of your company?'

    set_answer_to_session = 'company_name'

    direct_to = 'Trucks'


class Trucks(Chat):
    text = 'Do you own trucks?'

    set_answer_to_session = 'have_trucks'

    direct_if_positive = {
        'yes': 'TrucksQuantity',
        'no': 'YouHaveNoTrucks'
    }


class YouHaveNoTrucks(Chat):
    text = 'We need truck owners, bye bye :)'

    set_answer_to_session = 'notruck'

    terminate = True


class TrucksQuantity(Chat):
    text = 'How many trucks do you have?'

    set_answer_to_session = 'number_of_trucks'

    update_answer_to_session = 'number'

    direct_to = 'TruckBrands'


class TruckBrands(Chat):
    text = 'What brands are they?'

    set_answer_to_session = 'brands'

    direct_to = 'BrandQuantity'

    # Initialize itarate index for the next steps 
    iterate_index = 0

    def set_answer(self, session, user_message):
        """
            Override set_answer to split the brands entered by user
        """
        if user_message:
            user_message = user_message.replace(' and ', ',').split(',')
            session[self.set_answer_to_session] = user_message


class BrandQuantity(Chat):
    set_iteration_session = ('brands', 'current_truck_brand')

    text = 'How many {current_truck_brand} trucks do you have?'

    set_answer_to_session = '{current_truck_brand}_number'

    update_answer_to_session = 'number'

    direct_to = 'IfSameModels'


class IfSameModels(Chat):
    text = 'Are they same models?'

    set_answer_to_session = 'if_same_models_{current_truck_brand}'

    direct_if_positive = {
        'yes': 'TrucksSameModels',
        'no': 'TrucksVariantModels'
    }


class TrucksSameModels(Chat):
    text = 'What model are they?'

    set_answer_to_session = 'model_{current_truck_brand}'

    direct_to = 'EngineSize'


class EngineSize(Chat):
    text = 'What is engine size?'

    set_answer_to_session = 'engine_size_{current_truck_brand}'

    direct_to = 'AxlesNumber'


class AxlesNumber(Chat):
    text = 'How many axles do they have?'

    set_answer_to_session = 'axles_number_{current_truck_brand}'

    direct_if_session_iteration = {
        'finished': 'Bye',
        'notfinished': 'BrandQuantity'
    }


class TrucksVariantModels(Chat):
    text = 'This is just a test code, chat tree is not done for different models for the trucks.'

    set_answer_to_session = 'variant_trucks'

    terminate = True


class Bye(Chat):
    text = 'Your conversation is saved. We will contact to you as soon as possible. Thank you.'

    set_answer_to_session = 'bye'

    terminate = True