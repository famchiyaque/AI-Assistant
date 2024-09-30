import requests
import time
import webbrowser

def get_access_token():
    print("------get access token funcion-----")
    try:
        # Make a request to the local backend to get the access token
        response = requests.get("http://localhost:7664/api/token")
        time.sleep(3)
        
        # If the request was successful, check the token
        if response.status_code == 200:
            token = response.json()

            # If token is empty, initiate Spotify instance
            if token == '':
                print("No access token found, creating a new instance.")
                return ''
                # get_spot_instance()
            else:
                return token
        else:
            print("Failed to retrieve token from backend. Status code:", response.status_code)

    except requests.RequestException as e:
        print("Error occurred during the token request:", str(e))


def get_spot_instance():
    print("first checking backend for valid active session")
    result = get_access_token()
    if result != '':
        print("access token fetched from active session: " + result['access_token'])
        print("expires at from active session: ", result['expires_at'])
        return [result['access_token'], result['expires_at']]

    print("attempting to create a new instance and authorization/access token")
    print("starting authflow")
    authflow = requests.get('http://localhost:7664/auth/login', allow_redirects=False)
    time.sleep(3)
    if 'Location' in authflow.headers:
        redirect_url = authflow.headers['Location']
        print("following redirect URL: ", redirect_url)

        webbrowser.get("edge").open_new_tab(redirect_url)
        print("opening spotify auth, giving spotify time to authorize app")
        time.sleep(3)
    else:
        print("No redirect found")
        return ''

    print("attempting to retrieve newly made credentials")
    response = get_access_token()
    if response != '':
        print("new access token: " + response['access_token'])
        print("new expires at: ", response['expires_at'])
        return [response['access_token'], response['expires_at']]
    else:
        return ''
    


def open_spotify():
    webbrowser.get("edge").open_new("https://open.spotify.com")
    
def get_local_device(devices):
    for device in devices:
        if device['name'] == 'Web Player (Microsoft Edge)':
            return device
    return None

# def check_active_devices(devices):
#     for device in devices:
#         if device['is_active'] != True:


def check_local_playback(access_token):
    print("checking if spotify is open in browser")

    url = f'https://api.spotify.com/v1/me/player/devices'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        devices = response.json().get('devices', [])
        local_device = get_local_device(devices)
    else:
        return "problem with devices api"
    
    if local_device != None:
        return local_device
    else:
        return None


def transfer_playback(access_token, device_id):
    url = 'https://api.spotify.com/v1/me/player'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "device_ids": [device_id],
        "play": True
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 204:
        print(f"Playback transferred to device {device_id}")
        return True
    else:
        print(f"Failed to transfer playback. Status code: {response.status_code}")
        return False


def start_spotify(access_token):
    print("getting local device if there is one")
    localDevice = check_local_playback(access_token)
    if localDevice != None:
        device_id = localDevice['id']
        success = transfer_playback(access_token, device_id)
        if success == True:
            return "spotify now ready for playback api on this device"
        else:
            return "error transferring playback to this device"

    else:
        print("opening new spotify tab")
        open_spotify()
        time.sleep(3)
        return "error"        


     


    return "spotify ready for command"




def spotify_api(access_token, command):
    print("In Spotify API function with command:", command)

    # check_local_playback(access_token)

    url = f'https://api.spotify.com/v1/me/player/{command}'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = None

    try:
        if command == 'next' or command == 'previous':
            response = requests.post(url, headers=headers)
        elif command == 'devices':
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                devices = response.json().get('devices', [])
                if not devices:
                    print("No active devices found, opening spotify in browser")
                    # open_spotify()
                    # spotify_api(access_token, command)
                    return "no active devices"
                else:
                    print(f"Available devices: {devices}")
                    return devices

            else:
                print(f"Failed to get devices. Status code: {response.status_code}")
                return "problem with api"
        else:  # Assume other commands are PUT requests
            response = requests.put(url, headers=headers)
            print(f"Response Status Code: {response.status_code}")
            print("Response Content:", response.text)

        # Check for the status code
        if response is not None:
            if response.status_code == 204:
                return "Command executed successfully"
            elif response.status_code == 200:
                try:
                    data = response.json()
                    print("JSON response:", data)
                    return data
                except requests.exceptions.JSONDecodeError:
                    # If it's not JSON, handle it as a plain text response
                    print("Response is not JSON, returning raw text.")
                    return response.text
            else:
                print(f"Error: Received status code {response.status_code}")
                try:
                    # Attempt to decode JSON error message if available
                    error_message = response.json()
                    print("Error details:", error_message)
                except requests.exceptions.JSONDecodeError:
                    print("Error response could not be decoded as JSON.")

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

    return "Something broke"




# def spotify_api(access_token, command):
#     print("in spotify api function with command: " + command)
#     url = f'https://api.spotify.com/v1/me/player/{command}'
#     headers = {'Authorization': f'Bearer {access_token}'}
#     if command == 'next':
#         response = requests.post(url, headers=headers)
#     elif command == 'devices':
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             devices = response.json().get('devices', [])
#             if len(devices) == 0:
#                 print("No active devices found.")
#             else:
#                 print(f"Available devices: {devices}")
#             return devices
#         else:
#             print(f"Failed to get devices. Status code: {response.status_code}")
#             return []
#     else:
#         response = requests.put(url, headers=headers)

#     if response.status_code == 204:
#         return "command executed successfully"
#     else:
#         print("error: ", response.json())
#         return "something broke"