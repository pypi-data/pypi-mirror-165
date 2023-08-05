import boto3
import requests
import pandas as pd
import boto3.exceptions
import formulas
import random
import time
from importlib_metadata import version
import traceback


class TypeformExtractor:
    """
    Simple class to extract data from TypeForm Responses API, analyze text sentiments with Amazon Comprehend (AWS)
        and calculate metrics with the data

    AUTHORS:
        Daniel Vivas         - hello@danielvivas.com
        Julia Martinez Tapia - gmtcorreo@gmx.es
    """

    SUPPORTED_FUNCS_ES = ["CONTAR.SI", "SI.ERROR", "SI", "SUMA", "CONTAR", "REDONDEAR.MENOS"]

    credentials = None
    aws_client = None
    last_token = ''
    df = None
    metrics = None

    field_prefix = None
    page_size = None
    debug = None

    stats = {
        'total_items': 0,
        'extraction_time': 0.0,
        'metrics_time': 0.0
    }
    identifier = ''
    active_stats = True

    def __init__(self, credentials: dict, page_size: int = 500, field_prefix: str = 'field_', debug: bool = False):
        """
        :param credentials: AWS and TypeForm credentials to connect to their APIs
        :param page_size: How many results to get on each request
        :param field_prefix: Add a prefix to unnamed fields
        :param debug: If True, it will print debug annotations
        """

        if ('typeform_token' not in credentials.keys()):
            raise Exception('Typeform token is missing')

        self.credentials = credentials

        self.field_prefix = field_prefix
        self.page_size = page_size
        self.debug = debug
        self.metrics = []

        self.aws_client = boto3.client(service_name='comprehend', region_name='us-east-2',
                                       aws_access_key_id=self.credentials['aws_public_key'],
                                       aws_secret_access_key=self.credentials['aws_private_key'])

    def detect_sentiment(self, text: str) -> dict:
        """
        Connects to Amazon Comprehend API to analyze sentiment of given texts

        :param text: Text to analyze
        :return: Percentages of sentiments and sentiment label
        """
        sentiment = None

        try:
            result = self.aws_client.detect_sentiment(Text=text, LanguageCode='es')
            sentiment = result['SentimentScore']
            sentiment['Sentiment'] = result['Sentiment']
        except self.aws_client.exceptions.TextSizeLimitExceededException:
            if self.debug:
                print('Text size limit exceeded for sentiment analysis')

        return sentiment

    def __api_error_handling(self, data):
        if data.status_code == 403:
            raise Exception(f"""
            403 Error: Please check your Typeform token and try again\n
            {data.json()['code']} - {data.json()['description']}
            """)

    def set_identifier(self, identifier):
        self.identifier = identifier

        if self.debug:
            print(f"Identifier is now {identifier}")

    def deactivate_stats(self):
        self.active_stats = False

        if self.debug:
            print("Stats sending is now deactivated.")
            print(
                "Please, consider activating stats sending as it helps to the development os the package you are using.")

    def retrieve_data(self, form_id: str) -> dict:
        """
        Fetches form data from Typeform Responses API

        :param form_id: Form ID to get data from
        :return: JSON with fetched raw data
        """

        if self.debug:
            print("Fetching data from Typeform API...")

        url = f"https://api.typeform.com/forms/{form_id}/responses"
        params = {
            "page_size": self.page_size,
            'before': self.last_token
        }
        headers = {
            'Authorization': self.credentials['typeform_token']
        }
        data = requests.get(url, headers=headers, params=params)
        self.__api_error_handling(data)

        data = data.json()

        if self.stats['total_items'] == 0:
            self.stats['total_items'] = data['total_items']

        return data

    # Function to support get_field_names function
    def __recursive_search(self, data, dicc):
        if 'fields' in data.keys():
            for item in data['fields']:
                if 'fields' in item['properties'].keys():
                    self.__recursive_search(item['properties'], dicc)
                else:
                    key = self.field_prefix + item["id"]
                    dicc[key] = item["title"]

        return dicc

    def get_field_names(self, form_id: str) -> dict:
        """
        Fetches field names from Typeform API
        :param form_id: Form to get data from
        :return: Dict with keys as field ids and values as field names
        """

        if self.debug:
            print("Getting field names from Typeform API...")

        url = f"https://api.typeform.com/forms/{form_id}"

        headers = {
            'Authorization': self.credentials['typeform_token']
        }

        data = requests.get(url, headers=headers)
        self.__api_error_handling(data)

        data = data.json()

        dicc = self.__recursive_search(data, {})

        return dicc

    def generate_row(self, data: dict, fixed_fields: dict, sentiment: list):
        """
        Processes raw data to generate rows, gets the analysis sentiment and appends it to the dataframe

        :param data: Raw date fetched from Typeform API
        :param fixed_fields: Fixed columns to add to the dataframe
        :param sentiment: If not empty, it will analyze sentiments based on fields included on this list
        """
        for item in data['items']:

            if self.debug:
                print(f"Analyzing submission with ID {item['token']}")

            row = {}

            for key, value in fixed_fields.items():
                row[key] = value

            row['landing_id'] = item['landing_id']
            row['token'] = item['token']
            row['response_id'] = item['response_id']
            row['landed_at'] = item['landed_at']
            row['submitted_at'] = item['submitted_at']
            row['user_agent'] = item['metadata']['user_agent']

            texts = []

            for answer in item['answers']:

                field_id = answer['field']['id']
                field_type = answer['field']['type']

                if self.debug:
                    print(f"\tGenerating answer field with ID {field_id} ({field_type})")

                try:
                    if field_type in ["short_text", "long_text", "dropdown"]:
                        row[self.field_prefix + field_id] = answer['text']
                    elif field_type == "multiple_choice":
                        if 'choice' in answer.keys():
                            if 'label' in answer['choice'].keys():
                                row[self.field_prefix + field_id] = answer['choice']['label']
                        elif 'choices' in answer.keys():
                            row[self.field_prefix + field_id] = answer['choices']['labels']
                        else:
                            row[self.field_prefix + field_id] = None
                    elif field_type == "opinion_scale":
                        row[self.field_prefix + field_id] = answer['number']
                    elif field_type == "yes_no":
                        row[self.field_prefix + field_id] = answer['boolean']
                    elif field_type == "picture_choice":
                        row[self.field_prefix + field_id] = answer['choice']['label']
                    elif field_type == "email":
                        row[self.field_prefix + field_id] = answer['email']
                    elif field_type == "number":
                        row[self.field_prefix + field_id] = answer['number']
                    elif field_type == "phone_number":
                        row[self.field_prefix + field_id] = answer['phone_number']
                    elif field_type == "date":
                        row[self.field_prefix + field_id] = answer['date']
                    else:
                        row[self.field_prefix + field_id] = None
                        if self.debug:
                            print(f"Non recognized field type: {field_type}!")

                except:
                    row[self.field_prefix + field_id] = None

            self.df = pd.concat([self.df, pd.DataFrame.from_records([row])])

            # To get the last token for the next requests
            self.last_token = item['token']

    def get_fields(self, data: dict, fixed_columns: dict, sentiment: list) -> list:
        """
        Iterates over raw data and creates a list with fixed columns, submission details and distinct fields the form has

        :param data: Raw data fetched from Typeform API
        :param fixed_columns: Fixed columns to add to the dataframe
        :param sentiment: If not empty, it will analyze sentiments based on fields included on this list
        :return: Columns to be included in the dataframe with no translated names
        """

        columns = []
        fields = set()

        for key in fixed_columns.keys():
            columns.append(key)

        columns.extend(['landing_id', 'token', 'response_id', 'landed_at', 'submitted_at', 'user_agent'])

        for item in data['items']:
            for answer in item['answers']:
                name = self.field_prefix + answer['field']['id']
                fields.add(name)

        columns.extend(fields)

        return columns

    def translate_fields(self, field_names: dict):
        """
        Changes column names found in field_names

        :param field_names: Dict with field names to replace. Keys are the old values and values the new ones.
        """

        fields = self.df.columns

        for field in fields:
            if field in field_names:  # If it appears with prefix
                self.df.rename(columns={field: field_names[field]}, inplace=True)
            elif field.replace(self.field_prefix, '') in field_names:  # If it appears with NO prefix
                self.df.rename(columns={field: field_names[field.replace(self.field_prefix, '')]},
                               inplace=True)

    def test_all_forms(self, directory: str):
        """
        Fetches a list with all form IDs from the account and dumps a CSV file with each form

        :param directory: Path to store generated CSVs
        """
        forms = {}

        url = "https://api.typeform.com/forms"
        headers = {
            'Authorization': self.credentials['typeform_token']
        }
        params = {
            'page': 1
        }

        data = requests.get(url, headers=headers, params=params).json()

        total_pages = data['page_count']

        for item in data['items']:
            forms[item['id']] = item['title']

        while params['page'] <= total_pages:

            params['page'] += 1

            data = requests.get(url, headers=headers, params=params).json()

            for item in data['items']:
                print(f"------------------ ANALIZING {item['title']} ------------------")

                df = self.extract(form_id=item['id'])
                name = item['title'].replace('|', '')
                df.to_csv(f"{directory}\\{name}.csv")

                print(f"------------------- FINISHED {name} -------------------")

    def __fix_column_name(self, column):
        return column.replace(" ", "_").replace("\n", "").replace("/", "").replace("?", "") \
            .replace("¿", "").replace(",", "").replace("\"", "").replace(";", "").replace("=", "") \
            .replace("!", "").replace("¡", "").replace("%", "").replace(":", "").replace("(", "") \
            .replace(")", "").replace("º", "").replace("ª", "").replace("\\", "").replace("'", "") \
            .replace("-", "").replace("[", "").replace("]", "").replace("<", "").replace(">", "") \
            .replace("*", "").replace("&", "").replace("+", "").replace("‘", "").replace("’", "") \
            .replace("{", "").replace("}", "")

    def __fix_formula(self, formula: str):
        """
        Modifies formula according to calculation requirements

        :param formula: Metric formula
        """
        # 1. Translate functions
        translate = [
            {"old": "CONTAR.SI", "new": "COUNTIF"},
            {"old": "SI.ERROR", "new": "IFERROR"},
            {"old": "SI", "new": "IF"},
            {"old": "SUMA", "new": "SUM"},
            {"old": "CONTAR", "new": "COUNT"},
            {"old": "REDONDEAR.MENOS", "new": "ROUNDDOWN"}
        ]

        for item in translate:
            formula = formula.replace(f"{item['old']}(", f"{item['new']}(")

        # 2. Underscore blank spaces and remove trash in column names
        for column in list(self.df.columns):
            col_name = self.__fix_column_name(column)
            column = column.replace("\n", "")
            formula = formula.replace(column, col_name)

        # 3. Remove new lines and tabs
        formula = formula.replace("\n", "").replace("\t", "").replace(";", ",")

        # 3. Add = at the beggining
        if formula[0] != "=":
            formula = "=" + formula

        return formula

    def add_metric(self, name: str, formula: str):
        """
        Creates a new metric

        :param name: Metric name
        :param formula: Formula to calculate metric
        :return metric: Metric to add calculations to
        """
        self.metrics.append({
            'name': name, 'formula': formula
        })

    def __generate_arguments(self, inputs: list, row: dict):
        args = []
        for input in inputs:
            for column in row.keys():
                col_name = self.__fix_column_name(column.upper())
                if col_name == input:
                    args.append(row[column])

        return args

    def test_formula(self, formula: str, csv_path: str, nrow: int = None):
        """
        Checks if a given formula is valid

        :param formula: Formula to check.
        :param nrow: Row to test with. If None, a random one will be used.
        :param csv_path: Full csv path to load as dataframe.
        """

        # Temporary set df to be able to test formula
        self.df = pd.read_csv(csv_path)

        print('---------------- NEW FORMULA ----------------------')
        fixed_formula = self.__fix_formula(formula)
        print(fixed_formula, '\n')

        func = formulas.Parser().ast(fixed_formula)[1].compile()

        print('------------------- INPUTS -------------------------')
        form_inputs = list(func.inputs)
        print(form_inputs, '\n')

        if nrow is None:
            row = self.df.iloc[random.randint(0, self.df.shape[0])]
        else:
            row = self.df.iloc[nrow]

        print('----------------- ARGUMENTS => RESULT -----------------------')
        args = self.__generate_arguments(form_inputs, row)
        print('ARGUMENTS:', args)
        if len(args) > len(form_inputs):
            print("!!! POSSIBLE COLUMN DUPLICATION !!!")
        result = func(*args)
        print('RESULT: ', result)
        print('-------------------------------------------------------------')

        # Assuming the dataframe was empty
        self.df = None

    def __calculate_metric(self, metric: dict, row: dict):
        """
        Calculates a metric and returns its result

        :param metric: Metric to calculate
        :param row: Data to calculate metric
        """

        formula = self.__fix_formula(metric['formula'])

        func = formulas.Parser().ast(formula)[1].compile()

        params = self.__generate_arguments(list(func.inputs), row)

        return func(*params)

    def calculate_metrics(self):
        """
        Calculates all the metrics and concatenates a new column for each metric
        """
        for pos, metric in enumerate(self.metrics):
            if self.debug:
                print(f"Calculating metric {pos + 1}/{len(self.metrics)}: {metric['name']}")

            self.df[metric['name']] = self.df.apply(lambda x: self.__calculate_metric(metric, x), axis=1)

    def analyze_sentiment(self, columns: list):
        """
        Analyzes sentiment for all the columns provided

        :param columns: Columns to analyze
        """
        for column in columns:
            if self.debug:
                print(f"Analyzing sentiment for column {column}")

            self.df[f"sentiment_{column}"] = self.df.apply(lambda x: self.detect_sentiment(x[column])['Sentiment'],
                                                           axis=1)

    def supported_functions(self, lang: str = 'en'):
        """
        Get the supported functions

        :param lang: Lang of supported functions
        """

        if lang.lower() == 'en':
            return list(dict(formulas.get_functions()).keys())
        elif lang.lower() == 'es':
            return self.SUPPORTED_FUNCS_ES
        else:
            raise Exception(f"Lang {lang} not supported")

    def send_stats(self, sentiment, field_names, fixed_fields, auto_translate, error_msg):
        """
        Sends anonymous stats to help improve package development

        :param sentiment: Fields with analyzed sentiment
        """
        response = requests.post(url="https://pypkg.danielvivas.com/typeform-extractor/stats.php", data={
            'identifier': self.identifier,
            'version': version('typeform_extractor'),
            'n_regs': self.stats['total_items'],
            'extraction_time': round(self.stats['extraction_time']),
            'n_sentiment': len(sentiment),
            'sentiment_time': round(self.stats['sentiment_time']),
            'n_metrics': len(self.metrics),
            'metrics_time': round(self.stats['metrics_time']),
            'page_size': self.page_size,
            'debug': int(self.debug),
            'field_names': int(field_names is not None),
            'fixed_fields': len(fixed_fields),
            'auto_translate': int(auto_translate),
            'error': error_msg
        })

        print()

    def extract(self, form_id: str, field_names: dict = None, sentiment: list = [],
                fixed_fields: dict = {}, auto_translate: bool = True) -> pd.DataFrame:
        """
        Main function. Fetches the data, processes it and stores it inside the object

        :param form_id: Id of the form to get data from
        :param field_names: Dict with all column names to change
        :param sentiment: Columns to analyze with sentiment analysis. If empty, no analysis will be made
        :param fixed_fields: Constant columns to add to the Dataframe, Its value will be the same in all rows
        :param auto_translate: If True, it will fetch column names from the API. They may not be the names you want.
        :return: Structured dataframe with all translated fields
        """

        if self.debug:
            print("##################################################################################")
            print("#                              TYPEFORM EXTRACTOR                                #")
            print("#                                By Daniel Vivas                                 #")
            print("#                        Still in beta. Use with caution.                        #")
            print("#                        Contact: contact@danielvivas.com                        #")
            print("##################################################################################\n")

            print("STARTING EXTRACTION...")

        error_msg = ""

        try:
            # Time taken to extract
            time_start = time.perf_counter()

            # If sentiment analysis is activated, AWS credentials need to be set
            if (len(sentiment) != 0 and ('aws_public_key' not in self.credentials.keys() or self.credentials[
                'aws_public_key'] == '' or 'aws_private_key' not in self.credentials.keys() or self.credentials[
                                             'aws_private_key'] == '')):
                raise Exception('AWS credentials are malformed or missing')

            # Reset variables from previous results
            self.df = None
            self.last_token = ''

            form_id = str(form_id)

            # ------------------- First request -------------------#
            data = self.retrieve_data(form_id)

            # ---------------- Get distinct columns ---------------#
            columns = self.get_fields(data, fixed_fields, sentiment)

            self.df = pd.DataFrame(columns=columns)

            while len(data['items']) > 0:
                self.generate_row(data, fixed_fields, sentiment)
                data = self.retrieve_data(form_id)

            # Field names - First, translate manually inputted names
            if field_names is not None:
                self.translate_fields(field_names)

            # Field names - Then, auto translate fields
            if auto_translate:
                names = self.get_field_names(form_id)
                self.translate_fields(names)

            # Time taken to extract
            time_end = time.perf_counter()
            self.stats['extraction_time'] = time_end - time_start

            # Analyze sentiment
            if sentiment is not None:
                time_start = time.perf_counter()

                self.analyze_sentiment(sentiment)

                self.stats['sentiment_time'] = time.perf_counter() - time_start

            # Time taken to analyze sentiment
            time_start = time.perf_counter()

            # Calculate metric
            self.calculate_metrics()

            # Time taken to calculate metrics
            self.stats['metrics_time'] = time.perf_counter() - time_start

            if self.active_stats:
                self.send_stats(sentiment, field_names, fixed_fields, auto_translate, error_msg)

        except Exception as err:
            error_msg = traceback.format_exc()

            if self.active_stats:
                self.send_stats(sentiment, field_names, fixed_fields, auto_translate, error_msg)

            raise err

    def dataframe(self):
        return self.df
