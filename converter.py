import pandas as pd
import csv
import datetime
from pathlib import Path
import filenamer
import os


def txt_to_csv(*sap_download):
    if not sap_download:
        sap_download = filenamer.FileName.txt_file()

    full_file_aslist = open(sap_download, 'r').readlines()

    list_without_head = full_file_aslist[8:-5]
    list_without_head.insert(0, full_file_aslist[6])

    outfile_path = filenamer.FileName.path()
    beginning_time = datetime.datetime.now()
    csv_file_name = filenamer.FileName.date() + '2020Forecast.csv'
    csv_file = Path(outfile_path, csv_file_name)

    with open(csv_file, 'w', newline='\n') as outfile:
        a = 0

        out_writer = csv.writer(outfile, delimiter=';')

        clean_list = [list_without_head[0].split('\t')[4:]]
        clean_list[-1].insert(0, list_without_head[0].split('\t')[2])
        clean_list[0][2] = clean_list[0][2].lstrip()
        clean_list[0][3] = clean_list[0][3].rstrip('\n')
        
        out_writer.writerow(clean_list[-1])

        for i in range(1, len(list_without_head)):
            clean_list.append(list_without_head[i].split('\t')[4:])
            clean_list[-1].insert(0, list_without_head[i].split('\t')[2])
            clean_list[-1][2] = clean_list[-1][2].lstrip()
            clean_list[-1][3] = clean_list[-1][3].rstrip('\n')
            clean_list[-1][2] = clean_list[-1][2].replace('.', '')
            clean_list[-1][2] = clean_list[-1][2].replace(',', '.')

            out_writer.writerow(clean_list[-1])
            a += 1

    end_time = datetime.datetime.now()
    end_time = end_time - beginning_time

    print(f'{a:,} lines processed.')
    print(f'\nSuccessfully converted to {csv_file}')
    print(f'Processing time was {end_time.seconds} seconds')

    return csv_file


def from_csv_to_pivot_csv(csv_file):
    csv_file_path = Path(csv_file).parent
    beginning_time = datetime.datetime.now()
    csv_file_name = filenamer.FileName.date() + '2020Forecast-Pivot.csv'
    out_csv = Path(csv_file_path, csv_file_name)

    dataf = pd.read_csv(csv_file, sep=';', low_memory=False)

    os.remove(Path(csv_file))

    dataf['Reqmt Month'] = pd.to_datetime(dataf['Reqmt Date'],
                                          format='%d.%m.%Y').dt.to_period('M')
    dataf.drop('Reqmt Date', axis=1, inplace=True)
    # dataf.rename({'Reqmt Month':'Reqmt Date'},
    #             axis = 'columns', inplace = True)
    dataf['Reqmt Date'] = pd.PeriodIndex(dataf['Reqmt Month'], freq='M').to_timestamp()
    # .to_datetime(dataf['Reqmt Month'].assign(day=1),
    #                                     format='%d/%m/%Y')
    dataf.drop('Reqmt Month', axis=1, inplace=True)
    print('Column drop complete')
    dataf_piv = dataf.pivot_table(index='Material', columns='Reqmt Date',
                                  values='Reqmt Qty', aggfunc="sum")
    print('Pivot table complete')

    dataf = dataf.groupby(['Reqmt Date', 'Material', 'BUn'])['Reqmt Qty'].sum()
    print('Summing complete')

    monthly_csv_file = filenamer.FileName.date() + 'Monthly_list.csv'
    monthly_csv = Path(csv_file_path, monthly_csv_file)
    out_csv = Path(csv_file_path, csv_file_name)
    dataf.to_csv(monthly_csv, header=True, sep=';',
                 line_terminator='\n', decimal=',')
    print('CSV with monthly aggregates saved')

    pivot_csv = dataf_piv.to_csv(out_csv, index='Material', header=True,
                                 sep=';', line_terminator="\n", decimal=',')
    print('Pivot CSV saved')

    end_time = datetime.datetime.now()
    end_time = end_time - beginning_time

    print(csv_file, ' pivoted successfully!')
    print(f'Processing time was {end_time.seconds} seconds')


if __name__ == '__main__':
    # print('===Running preProcessSAPData===\n')
    # processed_txt = preProcessSAPData()
    print('\n===Running txt_to_csv===\n')
    csv_from_text = txt_to_csv()
    print('\n===Running from_csv_to_pivot_csv===\n')
    from_csv_to_pivot_csv(csv_from_text)