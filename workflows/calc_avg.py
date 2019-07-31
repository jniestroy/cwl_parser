import click
import json


@click.command()
@click.argument('file_number', type=int)
def calc_avg(file_number):
    file_name = "/Users/justinniestroy-admin/Documents/Work/Randall Data/houlter data//BEA/UVA" + str(file_number).rjust(4, '0') + ".bea"
    with open(file_name) as f:
        data = f.read()
        data_list = data.split(' ')
        result = []
        for i in range(0,len(data.split(' '))):
            if data_list[i] == 'NORMAL':
                try:
                    result.append(int(data_list[i-2].replace('(N\n','').replace('\n','')))
                except:
                    continue
    click.echo(json.dumps({'answer': sum(result) / len(result)}))


if __name__ == '__main__':
    calc_avg()
