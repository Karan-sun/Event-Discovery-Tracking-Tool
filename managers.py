import pandas as pd
import os
from datetime import datetime

FILE_NAME = "events.xlsx"

def save_events(events):
    if not events:
        print("No events to save.")
        return

    new_df = pd.DataFrame(events)
    
    if os.path.exists(FILE_NAME):
        try:
            existing_df = pd.read_excel(FILE_NAME)

            existing_dict = existing_df.set_index("url").to_dict("index")
            
            updated_rows = []
            
            for event in events:
                url = event["url"]
                if url in existing_dict:
                    existing_row = existing_dict[url]
                    existing_row.update(event)
                    updated_rows.append(existing_row)
                    del existing_dict[url] 
                else:
                    updated_rows.append(event) 
            
            for url, row in existing_dict.items():
                row['url'] = url
                updated_rows.append(row)
                
            final_df = pd.DataFrame(updated_rows)
            
        except Exception as e:
            print(f"Error reading existing file: {e}. Overwriting.")
            final_df = new_df
    else:
        final_df = new_df

    today = datetime.now().strftime("%Y-%m-%d")
    
    def check_expiry(row):
        try:
            if row['date'] < today:
                return "Expired"
            return row['status']
        except:
            return row['status']

    final_df['status'] = final_df.apply(check_expiry, axis=1)
    try:
        final_df.to_excel(FILE_NAME, index=False)
        print(f"Saved {len(final_df)} events to {FILE_NAME}")
    except PermissionError:
        raise PermissionError(f"Cannot save to {FILE_NAME}. Please close the file if it is open in Excel.")
    except Exception as e:
        raise Exception(f"Failed to save Excel file: {e}")

def get_all_events():
    if os.path.exists(FILE_NAME):
        return pd.read_excel(FILE_NAME).to_dict('records')
    return []
