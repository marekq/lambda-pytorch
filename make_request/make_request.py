import requests

apigw_url = 'https://x.execute-api.eu-west-1.amazonaws.com/'

inputstr = 'this is a sample text'

def do_inference(path):

    r = requests.post(apigw_url + path , data = inputstr, timeout = 31)
    print(str(r.elapsed)[5:10] + " sec \t " + path + "\t " + ''.join(r.text).strip() + '\n')

print('input \t\t ' + str(inputstr) + '\n')
do_inference('distilbert')
do_inference('t5large')
