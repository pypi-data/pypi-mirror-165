from argparse import ArgumentParser
from pathlib import Path
import pandas as pd
import re
import inquirer

parser = ArgumentParser(
    description='Utilidad de python el analisis de los logs Passed Auth de Tacacs+',
    epilog='Author: Mr0rang3'
)

parser.add_argument(
    'path',
    type=Path,
)

parser.add_argument('userName', type=str)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def parserLogToDataFrame(path: Path) -> pd.DataFrame:
    data: pd.DataFrame

    if not path.is_dir():
        data = pd.read_csv(path)

    else:
        pathForOnlyCsv = path.glob('*.csv')
        data = pd.concat(
            (pd.read_csv(file)
             for file in pathForOnlyCsv),
            ignore_index=True,
            axis=0
        )

    return data


def extractLoginInfo(data: pd.DataFrame) -> pd.DataFrame:
    return data[['Date', 'Time', 'User-Name', 'Group-Name']]


def getUserNameList(data: pd.DataFrame) -> list[str]:
    return [info[0] for info in data.groupby('User-Name')]


def getStrCoincidencesInList(search: str, data: list) -> tuple[list[str], str]:

    if isinstance(search, str) and isinstance(data, list):
        search_pattern = re.compile(r'' + re.escape(search), re.IGNORECASE)
        result = list(filter(search_pattern.match, data))

        return (result, f'Se han encontrado {len(result)} coincidencias')

    return (list(), 'Invalid argument types')


def prompt_SelectOneCoincidence(coincidences: list[str], message: str, userName) -> tuple[bool, str]:
    name: str

    if len(coincidences) != 0:
        print(
            f'{bcolors.OKGREEN}[*]{bcolors.ENDC} {message} para el nombre {userName}')
        questions = [inquirer.List(
            name='choice', message='Por favor, elija uno: ', choices=coincidences)]
        answer = inquirer.prompt(questions)
        name = answer['choice']
        return (True, name)

    else:
        name = str()
        print(
            f'{bcolors.FAIL}[!]{bcolors.ENDC} No se ha encontrado ninguna coincidencia para el nombre {userName}')
        response = input(
            f'{bcolors.HEADER}[?]{bcolors.ENDC} ¿Desea buscar otro nombre? (y/n): ').lower()

        while response not in ['y', 'n']:
            response = input(
                f'{bcolors.HEADER}[?]{bcolors.ENDC} ¿Desea buscar otro nombre? (y/n): ').lower()

        if response == 'y':
            return (False, name)

        exit()


def main():
    args: dict = vars(parser.parse_args())
    path: Path = args['path']
    userName: str = args['userName'].strip('\'').strip('\"')

    print(f'{bcolors.OKBLUE}[-]{bcolors.ENDC} Cargando archivos de logs')
    logs = parserLogToDataFrame(path)

    print(
        f'{bcolors.OKBLUE}[-]{bcolors.ENDC} Extrayendo información de inicio de sesión')
    login_info: pd.DataFrame = extractLoginInfo(logs)

    users: list[str] = getUserNameList(login_info)

    name: str

    while True:
        coincidences, message = getStrCoincidencesInList(userName, users)
        can_break, name = prompt_SelectOneCoincidence(
            coincidences, message, userName)

        if can_break:
            break
        userName = input(
            f'{bcolors.OKCYAN}[+]{bcolors.ENDC} Nombre de usuario: ')

    objective_info = login_info.loc[login_info['User-Name']
                                    == name].sort_values(by='Date')

    objective_info['Date'] = pd.to_datetime(
        objective_info['Date'], format='%d/%m/%Y')

    start_date = objective_info.iloc[0]['Date']
    end_date = objective_info.iloc[-1]['Date']

    daysDF = objective_info.groupby(pd.to_datetime(objective_info['Date'], dayfirst=True)
                                    .dt.floor('d')).size().reset_index(name='count')

    daysInList = list(daysDF.itertuples(index=False, name=None))
    daysInStr = "".join('\n\t\t' + str(value.date()) + ' ---> ' + str(count)
                        for value, count in daysInList)

    meanOfDays = daysDF.mean(numeric_only=True)
    meanOfDays = meanOfDays['count']

    objective_info['Date'] = pd.to_datetime(
        objective_info['Date'] - pd.to_timedelta(7, unit='d'))

    weeksDF = objective_info.groupby(
        [pd.Grouper(key='Date', freq='W')]).size().reset_index(name='count')

    meanOfWeek = weeksDF.mean(numeric_only=True)
    meanOfWeek = meanOfWeek['count']

    print('----------------------------------------------------------------------')
    print(
        f'{bcolors.BOLD}Analisis de inicios de sesión en los logs para el usuario: {name}{bcolors.ENDC} \n\tPrimer inicio de sesión: {bcolors.BOLD}{start_date}{bcolors.ENDC}\n\tUltimo inicio de sesión: {bcolors.BOLD}{end_date}{bcolors.ENDC} \n\tConteo de conexión entre las fechas de inicio y fin: {bcolors.BOLD}{daysInStr}{bcolors.ENDC} \nPromedio de conexiones por día: {bcolors.BOLD}{meanOfDays}{bcolors.ENDC} \nPromedio de conexiones por semana: {bcolors.BOLD}{meanOfWeek}{bcolors.ENDC}')


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print(
            f'{bcolors.FAIL}[!]{bcolors.ENDC} Saliendo inesperadamente...')
        exit(1)
