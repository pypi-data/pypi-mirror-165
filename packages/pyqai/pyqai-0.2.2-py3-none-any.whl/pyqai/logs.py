import requests
import json
import yaml
import argparse

# NOTE: returns a list of pod names.
# TODO: write this into a file, instead of printing to terminal. which is what k8s does, but we want to be better.
# TODO: make this error handling not shit.
def get_pod_logs(api_token, account_name, account_id, model_name, pod_name):
    get_podLogs_json = {"model_name":model_name, "pod_name":pod_name,"account_id":account_id,"api_token":api_token,"account_name":account_name}

    try:
        get_pod_logs = requests.post('https://get-pod-logs-fgkue36c2q-uc.a.run.app', json = get_podLogs_json, headers={'Authorization':api_token})
        get_podslogs_response = json.loads(get_pod_logs.text)
        get_podslogs_content = get_podslogs_response["response"]

        get_podslogs_content = get_podslogs_response["response"]
        return get_podslogs_content
    except Exception as e:
        print(f"ERROR. Unable to get pod names with exception: {e}")
        return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_token", help="Your pyq API token", required=True)
    parser.add_argument("--account_name", help="Your pyq account name", required=True)
    parser.add_argument("--account_id", help="Your pyq account ID", required=True)
    parser.add_argument("--model_name", help="The name of your deployed model", required=True)
    parser.add_argument("--pod_name", help="The name of your pod", required=True)

    args = parser.parse_args()

    print(get_pod_logs(args.api_token, args.account_name, args.account_id, args.model_name, args.pod_name))

    #python3 podLogs.py --api_token d6d988ed-f2e5-4bfc-a813-c55f58c9b4e7 --account_name emilys-account --account_id 3 --model_name numbaguessa --pod_name numbaguessa-v1-7cc5c49ddf-8wbff