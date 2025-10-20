import json
import requests

def check_urls(json_file):
    with open(json_file, 'r') as file:
        licenses = json.load(file)

    results = []
    for license in licenses:
        name = license.get('name')
        access_url = license.get('access_url')
        
        if not access_url:
            results.append({"name": name, "access_url": access_url, "status": "No URL provided"})
            continue

        try:
            response = requests.get(access_url, timeout=10)
            if response.status_code == 200:
                results.append({"name": name, "access_url": access_url, "status": "Accessible"})
            else:
                results.append({"name": name, "access_url": access_url, "status": f"Error: HTTP {response.status_code}"})
        except requests.exceptions.RequestException as e:
            results.append({"name": name, "access_url": access_url, "status": f"Error: {str(e)}"})

    return results

if __name__ == "__main__":
    # Replace with your actual JSON file path
    json_file = "./licenses.json"

    # Check URLs
    results = check_urls(json_file)

    # Print results
    for result in results:
        print(f"License Name: {result['name']}")
        print(f"Access URL: {result['access_url']}")
        print(f"Status: {result['status']}")
        print("-" * 40)

    # Optionally, save results to a file
    with open("url_check_results.json", "w") as output_file:
        json.dump(results, output_file, indent=4)