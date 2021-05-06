import requests, sys

apigw_url = 'https://x.execute-api.eu-west-1.amazonaws.com/'

# t5large inference
def t5large_inference(input_str):

    r = requests.post(apigw_url + 't5large', data = input_str, timeout = 31)

    print(str(r.elapsed)[5:10] + " sec - t5large - " + str(input_str)[:50] + "...\n\n" + ''.join(r.text).strip() + '\n\n')

# distilbert inference
def distilbert_inference(input_str):

    r = requests.post(apigw_url + 'distilbert', data = input_str, timeout = 31)

    print(str(r.elapsed)[5:10] + " sec - distilbert - " + str(input_str)[:50] + "..." + "\n\n" + ''.join(r.text).strip() + '\n\n')

def main():

    # get input document from argv $1
    input_doc = sys.argv[1]
    input_str = open(input_doc).read()

    # get inference mode from argv $2
    inference_mode = sys.argv[2]

    print('\nstarting inference...\n')

    # inference distilbert model
    if inference_mode == "d" or inference_mode == "distilbert":
        distilbert_inference(input_str)

    # inference t5large model
    elif inference_mode == "t" or inference_mode == "t5large":
        t5large_inference(input_str)

    # inference on both models
    else:
        distilbert_inference(input_str)
        t5large_inference(input_str)

main()
