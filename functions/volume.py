from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

words = ['one', 'two', 'three', 'four','five', 'six', 'seven', 'eight', 'nine', 'ten']
vals = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]

levels = ['one', 'two', 'three', 'four','five', 'six', 'seven', 'eight', 'nine', 'ten']
vals_dec = [-65.0, -50.0, -44.0, -38.0, -32.0, -26.0, -20.0, -14.0, -8.0, -2]


def mod_volume(query):
    # if 'up' in query or 'down' in query:
    #     num = 0
    #     for word in query:
    #         if word in words:
    #             num = vals[words.index(word)]
    #     modify_volume(num if 'up' in query else -num)
    # else:
        num = 0
        for word in query:
            if word == 'level':
                next_word = query[query.index(word) + 1] 
                num = vals_dec[levels.index(next_word)]
                # num = vals[words.index(word)]
            else:
                for word in query:
                    if word in levels:
                        num = levels[words.index(word)]
        set_volume(num)

def set_volume(new_vol):
    print("new volume level passed to function: ", new_vol)
    # devices = AudioUtilities.GetSpeakers()
    # interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
    # currVolume = interface.GetMasterVolumeLevelScalar()  # Volume is a float between 0.0 and 1.0
    # print(f"Current Volume: {currVolume * 100}%")  # Show volume as percentage

    # Set volume in scalar (0.0 to 1.0)
    if -65.0 <= new_vol <= 0.0:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevel(new_vol, None)
        print("Volume changed to:", new_vol , "%")
    else:
        print("Volume level out of range.")


def modify_volume(delta):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
    currVolume = interface.GetMasterVolumeLevelScalar()  # Volume is a float between 0.0 and 1.0
    print(f"Current Volume: {currVolume * 100}%")  # Show volume as percentage

    # Calculate new volume
    new_volume = currVolume + delta
    if 0.0 <= new_volume <= 1.0:  # Ensure new volume is within valid range
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        print("Volume changed to:", new_volume * 100, "%")
    else:
        print("Volume level out of range.")