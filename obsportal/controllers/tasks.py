from celery import shared_task
from alpaca.telescope import Telescope
import time

@shared_task 
def telescope_demo():
    T = Telescope('localhost:32323', 0)
    print(T)
    try:
        T.Connected = True
        print(f'Connected to {T.Name}')
        print(T.Description)
        T.Tracking = True               # Needed for slewing (see below)
        print('Starting slew...')
        T.SlewToCoordinatesAsync(T.SiderealTime + 2, 50)    # 2 hrs east of meridian
        while(T.Slewing):
            time.sleep(5)               # What do a few seconds matter?
        print('... slew completed successfully.')
        print(f'RA={T.RightAscension} DE={T.Declination}')
        print('Turning off tracking then attempting to slew...')
        T.Tracking = False
        T.SlewToCoordinatesAsync(T.SiderealTime + 2, 55)    # 5 deg slew N
        # This will fail for tracking being off
        print("... you won't get here!")
    except Exception as e:              # Should catch specific InvalidOperationException
        print(f'Slew failed: {str(e)}')
    finally:                            # Assure that you disconnect
        print("Disconnecting...")
        T.Connected = False   
