import xmltodict
import requests
import os
import socket

IP = socket.gethostbyname(socket.gethostname())
namecheap_key = os.getenv('NAMECHEAP_KEY')
namecheap_username = os.getenv('NAMECHEAP_USERNAME')
URL = f"https://api.namecheap.com/xml.response?ApiUser={namecheap_username}&ApiKey={namecheap_key}&UserName={namecheap_username}&ClientIp={IP}"


def __filter_result(data: dict):
    return {key.replace("@", "").lower(): value for key, value in data.items()}


def get_list() -> dict:
    path = URL + f"&Command=namecheap.domains.getList"
    response = requests.get(path)
    data = xmltodict.parse(response.text)
    api_response = data['ApiResponse']
    if api_response['@Status'] != 'OK':
        raise Exception(f"{api_response['Errors']}")
    command_response = api_response['CommandResponse']
    list_result = command_response['DomainGetListResult']
    return [__filter_result(item) for item in list_result['Domain']]


def get_info(domain: str) -> dict:
    path = URL + f"&Command=namecheap.domains.getinfo&DomainName={domain}"
    response = requests.get(path)
    data = xmltodict.parse(response.text)
    api_response = data['ApiResponse']
    if api_response['@Status'] != 'OK':
        raise Exception(f"{api_response['Errors']}")
    command_response = api_response['CommandResponse']
    info_result = command_response['DomainGetInfoResult']
    return __filter_result(info_result)


class Host:
    __ID = 1
    def __init__(self, record_type=None, address=None, host_name=None, ttl=None):
        assert record_type in ["A",         # A Record
                               "AAAA",      # AAAA Record
                               "ALIAS",     # ALIAS Record
                               "CAA",       # CAA Record
                               "CNAME",     # CNAME Record
                               "MX",        # Masked? Record
                               "MXE",       # Masked? Record
                               "NS",        # NS Record
                               "TXT",       # TXT Record
                               "URL",       # URL Redirect Record
                               "URL301",    # Permanent URL Redirect Record
                               "FRAME"]
        assert host_name in ['@', 'www']
        self.id = Host.__ID
        Host.__ID += 1
        self.record_type = record_type
        self.address = address
        self.host_name = host_name
        self.ttl = ttl

    def __str__(self):
        path = f"&HostName{self.id}={self.host_name}"
        path += f"&RecordType{self.id}={self.record_type}"
        path += f"&Address{self.id}={self.address}"
        path += f"&TTL{self.id}={self.ttl}" if self.ttl else ''
        return path


def set_hosts(*args: Host, SLD='', TLD='') -> dict:
    names = [item['name'] for item in get_list()]
    assert f"{SLD}.{TLD}" in names, f"{SLD}.{TLD} is not in: {names}"

    path = URL
    path += f"&Command=namecheap.domains.dns.setHosts"
    path += f"&SLD={SLD}&TLD={TLD}"
    for host in args:
        path += f"{host}"

    response = requests.get(path)
    data = xmltodict.parse(response.text)
    api_response = data['ApiResponse']
    if api_response['@Status'] != 'OK':
        raise Exception(f"{api_response['Errors']}")
    command_response = api_response['CommandResponse']
    set_hosts_result = command_response['DomainDNSSetHostsResult']
    return __filter_result(set_hosts_result)


if __name__ == "__main__":
    host1 = Host(record_type='URL', host_name='@', address='http://ark-api.guru')
    host2 = Host(record_type='URL', host_name='www', address='http://ark-api.guru')
    response = set_hosts(host1, host2, SLD='ark-shop', TLD='guru')
    print(response)
