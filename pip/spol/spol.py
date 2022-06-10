from bs4 import BeautifulSoup
from pprint import pprint
import argparse
import requests
import sys

def check_complaint(complaint_number):
    #complaint_number=97939
    url=f'http://igpcms.sindhpolice.gov.pk/Complaint_Detail_For_Complainant.aspx?Complaint_Id={complaint_number}'

    res = requests.get(url)
    parsed = BeautifulSoup(res.text, 'html.parser')
    complaint = {
            'id':0,
            'cnic':'-',
            'date':'-',
            'time':'-',
            'name':'-',
        }

    print('\nSINDH POLICE COMPLAINT')
    print('----------------------')

    try:
        complaint['id'] = parsed.find('span', {'id': 'Label_Track'}).text
        complaint['date'] = parsed.find('span', {'id': 'Label_Date'}).text
        complaint['time'] = parsed.find('span', {'id': 'LabelTime'}).text
        complaint['cnic'] = parsed.find('span', {'id': 'LabelCNIC'}).text
        complaint['cname'] = parsed.find('span', {'id': 'Label_Complainent_Name'}).text
        complaint['fname'] = parsed.find('span', {'id': 'Label_Father_Namne'}).text
        complaint['deadline'] = parsed.find('span', {'id': 'LabelResponseDate'}).text
        complaint['status'] = parsed.find('div', {'class': 'middle_text'}).text
        complaint['comments'] = parsed.find('span', {'class': 'title'})
    except:
        print('ERROR: ', 'Failed to acquire complaint.')

    print('ID: ', complaint['id'])
    print('DATE: ', complaint['date'])
    print('TIME: ', complaint['time'])
    print('CNIC: ', complaint['cnic'])
    print('COMPLAINANT: ', complaint['cname'])
    print('FATHER: ', complaint['fname'])
    print('DEADLINE: ', complaint['deadline'])
    print('STATUS: ', complaint['status'].strip())
    if complaint['comments']:
        print('COMMENTS: ')
        c = complaint['comments']
        while True:
            c = c.nextSibling
            if c:
                pprint(c.text)
            else:
                break

unit_url='https://www.sindhpolice.gov.pk/caders/{}'
def list_units():
    rs = requests.get(unit_url.format('index.html'))
    bs = BeautifulSoup(rs.text, 'html.parser')
    #print(bs)
    div = bs.find('div', {'class': 'container_organ'})
    return div

def list_unit(un):
        print(f'\n\033[6mSINDH POLICE UNIT #{un:02}\033[0m')
        print('---------------------')
        units = list_units()
        #print(units)
        if units:
            units = units.find_all('p')
            u = units[un-1]
            ln = u.a['href'].split('/')[-1]
            #print(unit_url.format(ln))
            rs2 = requests.get(unit_url.format(ln))
            bs2 = BeautifulSoup(rs2.text, 'html.parser')
            #print(bs2)
            title = bs2.find('div', {'class': 'container_organ'}).h3.text
            tbl = bs2.body.div.table
            #print(tbl)
            print(f'\n\033[4mUNIT: {title.strip()}\033[0m\n')
            unit_resources = tbl.find_all('tr')
            problematic_units = [13, 17]
            for ur in unit_resources[1:]:
                if ur:
                    ud = ur.find_all('td')
                    #import ipdb; ipdb.set_trace()
                    idx = 0
                    try:
                        sn = int(''.join(filter(str.isdigit, ud[idx].text)))
                    except:
                        break;
                    print('\033[2mSerial#\033[0m ', sn)
                    idx = 1 if a.unit in problematic_units else 2
                    print('\033[3mDesignation\033[0m ', ud[idx].text.strip())
                    idx = 2 if a.unit in problematic_units else 4
                    print('\033[3mName\033[0m ', ud[idx].text.strip())
                    idx = 3 if a.unit in problematic_units else 6
                    print('\033[3mAppointment\033[0m ', ud[idx].text.strip())
                    print('--------')
                    continue

def list_hospitals():
    url = 'https://www.sindhpolice.gov.pk/welfare/police_hospitals.html'
    rs = requests.get(url)
    bs = BeautifulSoup(rs.text, 'html.parser')
    d = bs.find('div', {'class':'mainDiv'})
    hs = d.find_all('h3')

    idx = 1
    for h in hs:
        print(f'{idx:02}', h.text)
        idx = idx + 1

def list_helplines():
    url='https://www.sindhpolice.gov.pk/welfare/welfare_helpline.html'
    rs = requests.get(url)
    bs = BeautifulSoup(rs.text, 'html.parser')
    d = bs.find('div', {'class':'mainDiv'})
    hs = d.find_all('h3')

    idx = 1
    nidx = 0
    for h in hs:
        print('\033[4m')
        print(f'{idx:02}', h.text)
        print('\033[0m\033[2m')
        print(h.parent.find_all('p')[nidx].text)
        print('\033[0m')
        idx = idx + 1
        nidx = nidx+2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=' Pakistan Sind Police complaint status.')
    parser.add_argument('-c', '--complaint', required=False, help='Complaint number or ID of the complaint to check.')
    parser.add_argument('-l', '--list_units', required=False, action='store_true', help='List all Sindh Police units.')
    parser.add_argument('-m', '--medical_services', required=False, action='store_true', help='List all Sindh Police hospitals.')
    parser.add_argument('-p', '--helplines', required=False, action='store_true', help='List all Sindh Police welfare helplines.')
    parser.add_argument('-u', '--unit', type=int, required=False, help='Unit number to view.')
    a = parser.parse_args()

    if a.complaint:
        check_complaint(a.complaint)
    elif a.medical_services:
        list_hospitals()
    elif a.helplines:
        list_helplines()
    elif a.list_units:
        print('\nSINDH POLICE UNITS')
        print('------------------')
        units = list_units()
        #print(units)
        if units:
            units = units.find_all('p')
            i=0
            for u in units:
                i=i+1
                if u.a is not None:
                    print(f'{i:02}.', u.a.text.strip())
    elif a.unit:
        list_unit(a.unit)
