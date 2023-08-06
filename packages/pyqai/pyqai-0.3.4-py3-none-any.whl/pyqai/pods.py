import requests
import json
import yaml
import argparse

# NOTE: returns a list of pod names.
# TODO: consider sending back the entire yaml? Maybe someone wants that? No status update here.
# TODO: make this error handling not shit.
def get_pod_ids(api_token, account_name, account_id, model_name):
    get_pods_json = {"model_name":model_name,"account_id":account_id,"api_token":api_token,"account_name":account_name}
    get_pods = requests.post('https://get-pods-fgkue36c2q-uc.a.run.app', json = get_pods_json, headers={'Authorization':api_token})
    get_pods_response = json.loads(get_pods.text)
    get_pods_content = get_pods_response["response"]
    get_pods_k8s = yaml.safe_load(get_pods_content)

    try:
        pod_names = []
        for i in get_pods_k8s["items"]:
            pod_names.append(i["metadata"]["name"])
    except Exception as e:
        print(f"ERROR. Unable to get pod names with exception: {e}")
        return

    return pod_names

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_token", help="Your pyq API token", required=True)
    parser.add_argument("--account_name", help="Your pyq account name", required=True)
    parser.add_argument("--account_id", help="Your pyq account ID", required=True)
    parser.add_argument("--model_name", help="The name of your deployed model", required=True)
    args = parser.parse_args()

    print(get_pod_ids(args.api_token, args.account_name, args.account_id, args.model_name))

    # python3 pods.py --api_token d6d988ed-f2e5-4bfc-a813-c55f58c9b4e7 --account_name emilys-account --account_id 3 --model_name numbaguessa